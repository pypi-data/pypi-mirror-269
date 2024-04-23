from typing import Optional, TypedDict

from libs.database import DatabaseHandler
from libs.security.security import AccessTokenDict, Security
from sqlalchemy import or_, select
from utils import is_email_valid

from .ext import (
    InvalidEmail,
    InvalidGender,
    InvalidName,
    InvalidPassword,
    InvalidUsername,
)
from .models import UserModel
from .schemas import RegisterUserRequest


class UserInUseFields(TypedDict):
    username: bool
    email: bool


class UserService:

    database_handler = DatabaseHandler()
    security = Security()

    def validate_register_data(self, data: RegisterUserRequest) -> bool:
        # Valid name
        if len(data.fullname) <= 0:
            raise InvalidName('Name is empty')

        # Valid username
        if len(data.username) < 4:
            raise InvalidUsername('Username too short')
        if len(data.username) > 15:
            raise InvalidUsername('Username too long')

        # Email validate
        if not is_email_valid(data.email):
            raise InvalidEmail('Invalid email')

        # Password validate
        self.validate_password(data.password)

        # Gender validate
        if not self.get_gender_by_name(data.gender):
            raise InvalidGender('Gender not found')

        return True

    def validate_password(self, password: str) -> bool:
        if len(password) < 8:
            raise InvalidPassword('Password to short, min 8 characters')
        if len(password) > 25:
            raise InvalidPassword('Password to long, max 25 characters')

    def get_user_by_email_or_username(
        self, username: str = '', email: str = ''
    ) -> Optional[UserModel]:
        with self.database_handler as session:
            query = select(UserModel).where(
                or_(UserModel.email == email, UserModel.username == username)
            )
            user = session.scalar(query)
        return user

    def valid_email_or_username_in_use(
        self, data: RegisterUserRequest
    ) -> UserInUseFields:
        result: UserInUseFields = {'email': False, 'username': False}
        user = self.get_user_by_email_or_username(data.username, data.email)
        if user:
            result['email'] = user.email == data.email
            result['username'] = user.username == data.username
        return result

    def generate_access_token(self, sub) -> AccessTokenDict:
        return {
            'access_token': self.security.create_access_token(sub),
            'refresh_access_token': self.security.create_refresh_access_token(
                sub
            ),
        }
