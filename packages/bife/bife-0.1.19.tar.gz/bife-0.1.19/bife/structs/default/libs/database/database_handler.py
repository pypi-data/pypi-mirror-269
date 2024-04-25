from typing import Optional, Type

from config import get_config
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


class DatabaseHandler:

    instance: Optional['DatabaseHandler'] = None
    config = get_config()

    def __init__(self) -> None:
        self._engine = create_engine(
            self.config.DATABASE_CONNECTION, max_overflow=-1
        )
        self.session_manger = sessionmaker(self._engine)

    def __new__(cls: Type['DatabaseHandler']) -> 'DatabaseHandler':
        if cls.instance is None:
            cls.instance = super(DatabaseHandler, cls).__new__(cls)
        return cls.instance

    def get_engine(self) -> Engine:
        return self._engine

    def get_session(self) -> Session:
        return self.session_manger()

    def __enter__(self):
        return self.session_manger()

    def __exit__(self, exc_type, exc_value, traceback):
        ...
