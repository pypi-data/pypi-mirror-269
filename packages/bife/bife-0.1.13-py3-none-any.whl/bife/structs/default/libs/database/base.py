from pydantic.dataclasses import dataclass
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class Base(MappedAsDataclass, DeclarativeBase, dataclass_callable=dataclass):
    pass
