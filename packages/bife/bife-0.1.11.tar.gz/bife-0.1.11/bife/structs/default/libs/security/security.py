from datetime import datetime, timedelta
from functools import cache
from typing import Optional, TypedDict

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError
from config import get_config
from fastapi import HTTPException, Request, Response, status
from jwt.exceptions import ExpiredSignatureError
from libs.database.database_handler import DatabaseHandler
from modules.user.models import UserModel
from pydantic import ValidationError
from sqlalchemy import select


class AccessTokenDict(TypedDict):
    access_token: str
    refresh_access_token: str


class _Payload(TypedDict):
    exp: str
    sub: str


class Security:

    argon = PasswordHasher()
    database_handler = DatabaseHandler()
    JWT_ALGORITHM = get_config().JWT_ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES = get_config().ACCESS_TOKEN_EXPIRE_MINUTES
    REFRESH_TOKEN_EXPIRE_MINUTES = get_config().REFRESH_TOKEN_EXPIRE_MINUTES

    def __init__(self) -> None:
        self.JWT_SECRET_KEY = get_config().JWT_SECRET_KEY
        self.JWT_REFRESH_SECRET_KEY = get_config().JWT_REFRESH_SECRET_KEY

    # Argon 2
    def crypt_password(self, password: str) -> str:
        return self.argon.hash(password)

    def verify_password(self, hash: str, password: str) -> bool:
        try:
            return self.argon.verify(hash, password)
        except (VerifyMismatchError, InvalidHashError):
            return False

    @cache
    def _generate_jwt(self, subject: str, expires: datetime) -> str:
        to_encode = {'exp': expires, 'sub': subject}
        return jwt.encode(
            to_encode, self.JWT_SECRET_KEY, algorithm=self.JWT_ALGORITHM
        )

    def create_access_token(self, subject: str) -> str:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        return self._generate_jwt(subject, expires_delta)

    def create_refresh_access_token(self, subject: str) -> str:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=self.REFRESH_TOKEN_EXPIRE_MINUTES
        )
        return self._generate_jwt(subject, expires_delta)

    def decode_jwt(self, token: str) -> _Payload:
        return jwt.decode(
            token, self.JWT_SECRET_KEY, algorithms=[self.JWT_ALGORITHM]
        )

    def get_current_user(
        self, request: Request, response: Response
    ) -> UserModel:
        if not (tokens := self._get_access_token(request)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Token not provided',
            )

        try:
            payload = self.decode_jwt(tokens['access_token'])
        except (
            jwt.PyJWKError,
            ValidationError,
            jwt.DecodeError,
            ExpiredSignatureError,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Could not validate credentials',
            )

        user = self._get_user_model_by_uuid_subject(payload['sub'])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail='User not found'
            )

        return user

    def _get_user_model_by_uuid_subject(
        self, uuid: str
    ) -> Optional[UserModel]:
        with self.database_handler as session:
            query = select(UserModel).where(UserModel.uuid == uuid)
            return session.scalar(query)

    def _get_access_token(self, request: Request) -> Optional[AccessTokenDict]:
        if 'access_token' in request.cookies:
            return {
                'access_token': request.cookies['access_token'],
                'refresh_access_token': request.cookies.get(
                    'refresh_access_token', ''
                ),
            }
        elif 'access_token' in request.headers:
            return {
                'access_token': request.headers['access_token'],
                'refresh_access_token': request.headers.get(
                    'refresh_access_token', ''
                ),
            }
        return None

    def _renew_access_token_from_refresh(self, refresh_token: _Payload) -> str:
        return self.create_access_token(refresh_token['sub'])
