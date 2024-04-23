import os

from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel

load_dotenv(find_dotenv())


class Config(BaseModel):
    # API
    API_PORT: int = int(os.getenv('API_PORT', 8000))
    API_HOST: str = os.getenv('API_HOST', '0.0.0.0')

    # Database
    DATABASE_CONNECTION: str = os.getenv(
        'DATABASE_CONNECTION', 'sqlite:///database.sqlite'
    )

    # JWt
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY', 'secret')
    JWT_REFRESH_SECRET_KEY: str = os.getenv('JWT_REFRESH_SECRET_KEY', 'secret')
    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM', 'HS256')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', default=30)
    )  # 30 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES', default=10080)
    )  # 7 days


def get_config() -> Config:
    return Config()
