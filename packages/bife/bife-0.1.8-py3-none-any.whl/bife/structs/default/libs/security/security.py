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
    config = get_config()
    database_handler = DatabaseHandler()

    def __init__(self) -> None:
        self.JWT_SECRET_KEY = self.config.JWT_SECRET_KEY
        self.JWT_REFRESH_SECRET_KEY = self.config.JWT_REFRESH_SECRET_KEY
        self.JWT_ALGORITHM = self.config.JWT_ALGORITHM
        self.ACCESS_TOKEN_EXPIRE_MINUTES = (
            self.config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        self.REFRESH_TOKEN_EXPIRE_MINUTES = (
            self.config.REFRESH_TOKEN_EXPIRE_MINUTES
        )

    def crypt_password(self, password: str) -> str:
        encrypted_password = self.argon.hash(password)
        return encrypted_password

    def verify_password(self, hash: str, password: str) -> bool:
        return self._verify_password(hash, password)

    @cache
    def _verify_password(self, hash: str, password: str) -> bool:
        try:
            self.argon.verify(hash, password)
        except (VerifyMismatchError, InvalidHashError):
            return False
        return True

    def _generate_jwt(self, subject: str, expires: datetime) -> str:
        to_encode = {'exp': expires, 'sub': str(subject)}
        enconded_jwt = jwt.encode(
            to_encode, self.JWT_SECRET_KEY, self.JWT_ALGORITHM
        )
        return enconded_jwt

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
                status.HTTP_400_BAD_REQUEST, 'token not provided'
            )
        try:
            payload = self.decode_jwt(tokens['access_token'])
        except (jwt.PyJWKError, ValidationError, jwt.DecodeError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Could not validate credentials',
                headers={'WWW-Authenticate': 'Bearer'},
            )
        except ExpiredSignatureError:
            try:
                payload = self.decode_jwt(tokens['refresh_access_token'])
                access_token = self._renew_access_token_from_refresh(payload)
                response.set_cookie('access_token', access_token)
            except ExpiredSignatureError:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='JWT signature has expired',
                    headers={'WWW-Authenticate': 'Bearer'},
                )
        if current_user := self._get_user_model_by_uuid_subject(
            payload['sub']
        ):
            if not current_user:
                raise HTTPException(
                    status.HTTP_403_FORBIDDEN, 'User not found'
                )

        return current_user

    def _get_user_model_by_uuid_subject(
        self, uuid: str
    ) -> Optional[UserModel]:
        with self.database_handler as session:
            query = select(UserModel).where(UserModel.uuid == uuid)
            current_user = session.scalar(query)
        return current_user

    def _get_access_token(self, request: Request) -> Optional[AccessTokenDict]:
        if 'access_token' in request.cookies.keys():
            return {
                'access_token': request.cookies.get('access_token'),
                'refresh_access_token': request.cookies.get(
                    'refresh_access_token'
                ),
            }
        elif 'access_token' in request.headers.keys():
            return {
                'access_token': request.headers.get('access_token'),
                'refresh_access_token': request.headers.get(
                    'refresh_access_token'
                ),
            }

    def _renew_access_token_from_refresh(self, refresh_token: _Payload) -> str:
        return self.create_access_token(refresh_token['sub'])
