from dataclasses import dataclass, field
from typing import Literal


@dataclass
class DatabaseConfig:
    orm: Literal['sqlalchemy', 'sqlmodel'] = field(default='sqlalchemy')
    use_alembic: bool = field(default=True)


@dataclass
class UserConfig:
    create_module: bool = field(default=True)
    store_jwt: Literal['headers', 'cookie', 'both'] = field(default='headers')
    auth: bool = field(default=True)


@dataclass
class ModuleConfig:
    module_path: str = field(default='modules/')
