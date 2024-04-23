import os
import pathlib
import shutil

from mako.template import Template

from ...config import DatabaseConfig, ModuleConfig, UserConfig


def run(
    project_name: str,
    module_config: ModuleConfig,
    user_config: UserConfig,
    database_config: DatabaseConfig,
):
    shutil.copytree('bife/structs/default/libs/', f'{project_name}/libs')
    shutil.copytree('bife/structs/default/utils/', f'{project_name}/utils')
    os.makedirs(f'{project_name}/{module_config.module_path}')
    shutil.copytree('bife/structs/default/modules/user/', f'{project_name}/{module_config.module_path}/user')
    shutil.copy('bife/structs/default/config.py', f'{project_name}/config.py')
    shutil.copy('bife/structs/default/main.py', f'{project_name}/main.py')
    shutil.copy('bife/structs/default/app.py', f'{project_name}/app.py')
    if not os.path.isfile('.env'):
        with open('.env', 'w') as file:
            file.write('')
    with open(f'.env', 'a') as file:
        template = Template(open('bife/structs/default/.env').read())
        content = template.render(project_name=project_name)
        file.write(f'\n{content}')


def new_module():
    ...
