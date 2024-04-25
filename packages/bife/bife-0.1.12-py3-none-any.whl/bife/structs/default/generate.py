import os
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
    os.makedirs(project_name)
    copy_file_to_project(['app.py', 'main.py', 'config.py'], project_name)
    copy_directorys_to_project(['libs', 'utils'], project_name)
    copy_directorys_to_project(
        [os.path.join('modules', 'user')],
        os.path.join(project_name, module_config.module_path),
    )
    update_env_file(project_name)
    generate_bootstrap(project_name)

def update_env_file(project_name: str):
    current_dir = os.path.dirname(__file__)
    env_file_template = os.path.join(current_dir, '.env.template')

    if not os.path.isfile('.env'):
        with open('.env', 'w') as file:
            file.write('')

    
    with open(env_file_template, 'r') as file:
        template = Template(file.read())
        content = template.render(project_name=project_name)
    
    with open('.env', 'a') as file:
        file.write(f'\n{content}')
            
def create_required_directorys(prefix: str, paths: list[str]):
    for path in paths:
        os.makedirs(os.path.join(prefix, path))


def copy_file_to_project(files: list[str], path: str):
    current_dir = os.path.dirname(__file__)
    for file in files:
        shutil.copy(os.path.join(current_dir, file), path)


def copy_directorys_to_project(directorys: list[str], path: str):
    current_dir = os.path.dirname(__file__)
    for directory in directorys:
        print(
            f'copy {os.path.join(current_dir, directory)} to {os.path.join(path, directory)}'
        )
        shutil.copytree(
            os.path.join(current_dir, directory), os.path.join(path, directory.split('/')[-1])
        )

def generate_bootstrap(project_name: str):
    current_dir = os.path.dirname(__file__)
    template = Template(
        open(
            os.path.join(current_dir, 'libs', 'bootstrap', 'bootstrap.py')
        ).read()
    )
    boostrap_content = template.render(project_name=project_name)
    with open(
        os.path.join(project_name, 'libs', 'bootstrap', 'bootstrap.py'), 'w'
    ) as file:
        file.write(boostrap_content)