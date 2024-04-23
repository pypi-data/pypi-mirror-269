from libs.security import Security
from sqlalchemy import event
from sqlalchemy.engine.base import Connection
from sqlalchemy.orm.mapper import Mapper

from .models import UserModel


class UserEvents:
    @staticmethod
    @event.listens_for(UserModel, 'before_insert', propagate=True)
    def my_listener_function(
        mapper: Mapper, connection: Connection, target: UserModel
    ):
        target.password = Security().crypt_password(target.password)
