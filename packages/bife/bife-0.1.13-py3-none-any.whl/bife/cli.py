from typing import Literal

import typer

from .config import (
    configure_database,
    configure_module,
    configure_project,
    configure_user,
    create_bife_config,
)

typer_app = typer.Typer()
new = typer.Typer()
typer_app.add_typer(new, name='new')


@new.command()
def module(name: str):
    """
    Create a new module inside your fastapi project
    """
    print(f'Hello {name}')


@new.command()
def app(project_name: str):
    """
    Create a new app with FastAPI!
    """
    database_config = configure_database()
    project_config = configure_project()
    user_config = configure_user()
    module_config = configure_module()
    create_bife_config(module_config.module_path, project_config.structure)
    if project_config.structure == 'default':
        from .structs.default.generate import run

        run(project_name, module_config, user_config, database_config)


def start():
    typer_app()
