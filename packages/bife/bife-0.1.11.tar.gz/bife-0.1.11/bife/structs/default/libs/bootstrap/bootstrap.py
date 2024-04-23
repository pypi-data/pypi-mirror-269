import importlib
import os
from typing import Optional

from config import get_config
from fastapi import APIRouter
from fastapi.routing import Mount
from fastapi.staticfiles import StaticFiles
from libs.api.api_handler import ApiHandler

config = get_config()


class Bootstrap:
    def __init__(self) -> None:
        self.controllers = []
        self.current_path: str = os.path.join(
            os.path.relpath(os.path.join(os.getcwd())), '${project_name}'
        )
        path = self.get_project_path()
        modules_path = self.get_module_path(path)
        for root, _, files in os.walk(modules_path):
            for file in files:
                if 'controller' in file.lower() and file.endswith('.py'):
                    module_path = (
                        root.replace('/', '.')[2:]
                        + '.'
                        + file.replace('.py', '')
                    )
                    module_path = '.'.join(module_path.split('.')[1:])
                    modules = importlib.import_module(module_path)

                    for d in dir(modules):
                        router = getattr(modules, d)
                        if isinstance(router, APIRouter):
                            self.controllers.append(router)

    def get_project_path(self) -> Optional[str]:
        for root, dirs, _ in os.walk(self.current_path):
            if root.startswith('./.') or root.endswith('.'):
                continue
            if 'modules' in dirs:
                return root

    def get_module_path(self, path: str) -> Optional[str]:
        for root, dirs, files in os.walk(path):
            if (
                '__pycache__' in dirs
                or '__pycache__' in root
                or 'modules' not in root
            ):
                continue
            return root

    def setup_fastapi_app(self, app: ApiHandler):
        for controller in self.controllers:
            app.add_router(controller)
