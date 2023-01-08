from datetime import (
    datetime,
    timedelta,
)

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from jose import (
    JWTError,
    jwt,
)
from passlib.hash import bcrypt
from pydantic import ValidationError
from sqlalchemy.orm import Session
import sqlalchemy

from .. import (
    schemas,
    tables,
)
from ..database import get_session
from ..settings import settings
from aiohttp import ClientSession


class AuthService:

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    async def verify_email(cls, user_data: schemas.UserCreate):
        client = ClientSession()
        async with client.get(
                url='https://api.hunter.io/v2/email-verifier?'
                    f'email={user_data.email}&'
                    f'api_key={settings.API_KEY}',
                raise_for_status=True
        ) as the_response:
            result = await the_response.json()
        if result['data']['status'] == 'invalid':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Email is not valid',
            )

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def verify_token(cls, token: str) -> schemas.User:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        try:
            payload = jwt.decode(
                token,
                settings.SECRET,
                algorithms=[settings.ALGORITHM],
            )
        except JWTError:
            raise exception from None

        user_data = payload.get('user')

        try:
            user = schemas.User.parse_obj(user_data)
        except ValidationError:
            raise exception from None

        return user

    @classmethod
    def create_token(cls, user: tables.User) -> schemas.Token:
        user_data = schemas.User.from_orm(user)
        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=settings.EXPIRES),
            'sub': str(user_data.id),
            'user': user_data.dict(),
        }
        token = jwt.encode(
            payload,
            settings.SECRET,
            algorithm=settings.ALGORITHM,
        )
        return schemas.Token(access_token=token)

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_new_user(
            self,
            user_data: schemas.UserCreate,
    ) -> schemas.Token:
        try:
            user = tables.User(
                email=user_data.email,
                username=user_data.username,
                hashed_password=self.hash_password(user_data.password),
            )
            self.session.add(user)
            self.session.commit()
        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User with such email or username already exist',
            )
        return self.create_token(user)

    def authenticate_user(
            self,
            username: str,
            password: str,
    ) -> schemas.Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

        user = (
            self.session
            .query(tables.User)
            .filter(tables.User.username == username)
            .first()
        )

        if not user:
            raise exception

        if not self.verify_password(password, user.hashed_password):
            raise exception

        return self.create_token(user)
