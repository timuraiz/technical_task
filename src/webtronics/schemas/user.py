from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    username: str
    email: EmailStr


class UserCreate(BaseUser):
    password: str


class User(BaseUser):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
