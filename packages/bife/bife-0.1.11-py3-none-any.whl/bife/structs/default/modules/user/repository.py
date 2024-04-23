from libs.database import DatabaseHandler
from libs.security import Security

from .ext import (
    InvalidPassword,
    InvalidUserLogin,
    UserAlreadyExists,
    UserNotFound,
)
from .models import UserModel
from .schemas import LoginUserRequest, RegisterUserRequest
from .service import UserService


class UserRepository:

    database_handler = DatabaseHandler()
    service = UserService()
    secutiry = Security()

    def login_user(self, data: LoginUserRequest) -> UserModel:
        if len(data.user) < 4:
            raise InvalidUserLogin('Login user not provided')
        self.service.validate_password(data.password)

        user = self.service.get_user_by_email_or_username(data.user, data.user)
        if not user:
            raise UserNotFound('User not found')
        if not self.secutiry.verify_password(user.password, data.password):
            raise InvalidPassword('Password Wrong')

        return user

    def register_user(self, data: RegisterUserRequest) -> UserModel:
        self.service.validate_register_data(data)
        if any(self.service.valid_email_or_username_in_use(data).values()):
            raise UserAlreadyExists('User already exists')
        with self.database_handler as session:
            gender = self.service.get_gender_by_name(data.gender)
            new_user = UserModel(gender_id=gender.id, **data.model_dump())
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return new_user
