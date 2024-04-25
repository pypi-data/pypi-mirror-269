import os
import subprocess
from subprocess import PIPE
from dataclasses import dataclass, field
from typing import Literal

import questionary
from mako.template import Template
from questionary import Choice


@dataclass
class DatabaseConfig:
    orm: Literal['sqlalchemy', 'sqlmodel'] = field(default='sqlalchemy')
    use_alembic: bool = field(default=True)


@dataclass
class UserConfig:
    create_module: bool = field(default=True)
    store_jwt: Literal['headers', 'cookie', 'both', None] = field(
        default='headers'
    )


@dataclass
class ModuleConfig:
    module_path: str = field(default='modules/')


@dataclass
class ProjectConfig:
    structure: str = field(default='default')


def configure_database() -> DatabaseConfig:
    """
    Ask database configuration
    """
    orm = questionary.select(
        '💾 Do you want use Sqlalchemy or Sqlmodel?',
        choices=[
            Choice('Sqlalchemy', 'Sqlmodel'),
            Choice('Sqlmodel', 'sqlmodel'),
        ],
    ).ask()

    alembic = questionary.select(
        '📝 Do you want use alembic?',
        choices=[Choice('Yes', True), Choice('No', False)],
    ).ask()

    database_config = DatabaseConfig(orm, alembic)
    return database_config


def configure_user() -> UserConfig:
    """
    Ask user configuration
    """
    print(' ')
    create_user_module: bool = questionary.select(
        '👤 Create a user module?',
        choices=[Choice('Yes', True), Choice('No', False)],
    ).ask()
    if not create_user_module:
        return UserConfig(False, None)
    store_jwt: Literal['headers', 'cookie', 'both'] = questionary.select(
        '🔐 Where you want to get JWT token?',
        choices=[
            Choice('Headers', 'headers'),
            Choice('Cookies', 'cookies'),
            Choice('Both', 'both'),
        ],
    ).ask()
    user_config = UserConfig(create_user_module, store_jwt)
    return user_config


def configure_module() -> ModuleConfig:
    """
    Ask user configuration
    """
    print(' ')

    module_path: str = questionary.select(
        '📁 Where you want store modules?', choices=['modules/', 'modules/api/']
    ).ask()
    module_config = ModuleConfig(module_path)
    return module_config


def configure_project() -> ProjectConfig:
    """
    Ask project structure
    """
    print(' ')

    project_config: str = questionary.select(
        '🗄️ Select project structure', choices=['default']
    ).ask()
    structure_config = ProjectConfig(project_config)
    return structure_config


def create_bife_config(modules_path: str, project_structure: str):
    current_dir = os.path.dirname(__file__)
    with open(os.path.join(current_dir, 'config.template'), 'r') as file:
        template_content = file.read()
    bife_config_content = Template(template_content).render(
        modules_path=modules_path, project_structure=project_structure
    )
    with open('bife.config', 'w') as file:
        file.write(bife_config_content)


def install_packages(dependencies: list[str]):
    while True:
        print(' ')
        tool = questionary.select(
            '🪛 Do you use pip or poetry?',
            choices=[
                Choice('Poetry', 'poetry'),
                Choice('Pip', 'pip'),
                Choice('Other', 'other'),
            ],
        ).ask()

        if tool == 'poetry':
            try:
                subprocess.check_output(['poetry', 'add', *dependencies])
                print("😎 ALL DONE!")
                break
            except:
                print("Error using poetry\n")
                retry = questionary.confirm("🧐 Did you want use pip?").ask()
                if not retry:
                    print(f'Install the packages using your tool: {" ".join(dependencies)}')
                    break
        elif tool == 'pip':
            subprocess.run(['pip', 'install', *dependencies], check=True)
            print("😎 ALL DONE!")
            break
        else:
            print(f'Install the packages using your tool: {" ".join(dependencies)}')