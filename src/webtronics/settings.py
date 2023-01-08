from pydantic import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv('../.env')


class Settings(BaseSettings):
    POSTGRES_USER: str = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_SERVER: str = os.getenv('POSTGRES_SERVER')
    POSTGRES_PORT: str = os.getenv('POSTGRES_PORT', 5432)
    POSTGRES_DB: str = os.getenv('POSTGRES_DB')
    DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}'

    SECRET: str = os.getenv('jwt_secret')
    ALGORITHM: str = 'HS256'
    EXPIRES: int = 3600

    API_KEY: str = os.getenv('API_KEY')


settings = Settings(
    _env_file='../.env',
    _env_file_encoding='utf-8'
)
