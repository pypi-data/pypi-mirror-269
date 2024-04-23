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
    current_dir = os.path.dirname(__file__)
    shutil.copytree(os.path.join(current_dir, 'libs/'), os.path.join(project_name, 'libs'))
    template = Template(open(os.path.join(current_dir, 'libs', 'bootstrap', 'bootstrap.py')).read())
    boostrap_content = template.render(project_name=project_name)
    with open(os.path.join(project_name, 'libs', 'bootstrap', 'bootstrap.py'), 'w') as file:
        file.write(boostrap_content)
    shutil.copytree(os.path.join(current_dir, 'utils/'), os.path.join(project_name, 'utils'))
    os.makedirs(os.path.join(project_name, module_config.module_path))
    shutil.copytree(os.path.join(current_dir, 'modules/user/'), os.path.join(project_name, module_config.module_path, 'user'))
    shutil.copy(os.path.join(current_dir, 'config.py'), os.path.join(project_name, 'config.py'))
    shutil.copy(os.path.join(current_dir, 'main.py'), os.path.join(project_name, 'main.py'))
    shutil.copy(os.path.join(current_dir, 'app.py'), os.path.join(project_name, 'app.py'))
    if not os.path.isfile(os.path.join(current_dir, '.env')):
        with open('.env', 'w') as file:
            file.write('')
    with open('.env', 'a') as file:
        template = Template(open(os.path.join(current_dir, '.env')).read())
        content = template.render(project_name=project_name)
        file.write(f'\n{content}')
    print(f'Please, install the packages: fastapi pyjwt argon2-cffi sqlalchemy python-dotenv')

def new_module(module_name: str):
    ...