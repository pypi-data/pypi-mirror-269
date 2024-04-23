import sys

from pick import pick

from .config import DatabaseConfig, ModuleConfig, UserConfig
from .structs.default.run import new_module, run


class BifeCreateProject:
    def run(self):
        if len(sys.argv) == 1:
            print('Please, tell me the name of your project!')
            sys.exit(1)
        title = 'Welcome to BIFE, do you want use database?'
        database = self.database_config()
        user = self.setup_user_module()
        modules = self.setup_modules()
        run(sys.argv[3], modules, user, database)

    def database_config(self) -> DatabaseConfig:
        config = DatabaseConfig()
        _, selected_orm = pick(
            ['Sqlalchemy'],
            'Do you want use sqlalchemy or sqlmodel?',
            '=>',
        )
        config.orm = str(selected_orm).lower()
        _, use_alembic = pick(
            [
                'Yes, i want use alembic to manage migrations',
                "No, I don' want alembic",
            ],
            'Do you want use alembic to manage your database migrations?',
            '=>',
        )
        config.use_alembic = use_alembic == 0
        return config

    def setup_user_module(self):
        config = UserConfig()
        _, create_usermodel = pick(
            ['Yes, create user module', "I don' waht user module"],
            'Create a user module?',
            '=>',
        )
        if create_usermodel == 0:
            config.create_module = True
            _, jwt_store = pick(
                ['Headers', 'Cookies', 'Both'],
                'Where you want to get JWT token?',
                '=>',
            )
            config.store_jwt = str(jwt_store).lower()

            _, create_auth_system = pick(
                ['Yes, create auth system', 'No'],
                'Do you want create auth system?',
                '=>',
            )
            config.auth = create_auth_system == 0

        return config

    def setup_modules(self) -> ModuleConfig:
        config = ModuleConfig()
        path, _ = pick(
            ['modules/', 'modules/api/'], 'Where you want store modules?', '=>'
        )
        config.module_path = path
        return config


def cli():
    if len(sys.argv) < 3:
        print('Please tell a valid option ["new app", "new module"]')
    if sys.argv[1] == 'new':
        if sys.argv[2] == 'app':
            if len(sys.argv) == 4:

                bife = BifeCreateProject()
                bife.run()
            else:
                print('Error, tell a application name')
                sys.exit(1)
        elif sys.argv[2] == 'module':
            new_module(sys.argv[3], sys.argv[4])
