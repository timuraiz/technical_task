from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from .schemas import User
from .services.auth import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/sign-in/')


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    return AuthService.verify_token(token)



