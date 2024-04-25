from typing import Literal

import typer

from .config import (
    configure_database,
    configure_module,
    configure_project,
    configure_user,
    create_bife_config,
    install_packages,
    read_bife_config,
)

typer_app = typer.Typer()
new = typer.Typer()
typer_app.add_typer(new, name='new')


@new.command()
def module(name: str):
    """
    Create a new module inside your fastapi project
    """
    data = read_bife_config()
    if data['project_structure'] == 'default':
        from .structs.default.generate import new_module
        new_module(data['project_name'], name, data['module_path'])

@new.command()
def app(project_name: str):
    """
    Create a new app with FastAPI!
    """
    database_config = configure_database()
    project_config = configure_project()
    user_config = configure_user()
    module_config = configure_module()
    create_bife_config(project_name, module_config.module_path, project_config.structure)
    if project_config.structure == 'default':
        from .structs.default.generate import DEPENDENCIES, run

        run(project_name, module_config, user_config, database_config)
        install_packages(DEPENDENCIES)


def start():
    typer_app()
