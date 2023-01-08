from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, status

from ..schemas.user import (
    User,
    UserCreate,
    Token,
)
from ..services.auth import AuthService
from ..dependencies import get_current_user

router = InferringRouter()


@cbv(router)
class User:
    @router.post(
        '/sign-up',
        response_model=Token,
        status_code=status.HTTP_201_CREATED,
    )
    async def sign_up(
            self,
            user_data: UserCreate,
            auth_service: AuthService = Depends(),
    ):
        '''
        - Registration of new user using emailhunter.co for verifying email existence.
        - After all validations and savings to db endpoint returns a Token.
        \f
        :param user_data:
        :param auth_service:
        :return:
        '''
        await auth_service.verify_email(user_data=user_data)
        return auth_service.register_new_user(user_data)

    @router.post(
        '/sign-in',
        response_model=Token,
    )
    def sign_in(
            self,
            auth_data: OAuth2PasswordRequestForm = Depends(),
            auth_service: AuthService = Depends(),
    ):
        '''
        - Sign in section allows to user log in using own username and password.
        - Form was created using OAuth2.
        - After all validations endpoint returns a Token.
        \f
        :param auth_data:
        :param auth_service:
        :return:
        '''
        return auth_service.authenticate_user(
            auth_data.username,
            auth_data.password,
        )

    @router.get(
        '/user',
        response_model=User,
    )
    def get_user(self, user: User = Depends(get_current_user)):
        '''
        - Returns data of the current user(who called this method).
        \f
        :param user:
        :return:
        '''
        return user
