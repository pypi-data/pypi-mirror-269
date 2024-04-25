import os
import shutil
import sys
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

def new_module(module_name: str):
    current_dir = os.path.dirname(__file__)
    # full_path = os.path.abspath(path)

    # if not os.path.isdir(full_path):
    #     print(f'Invalid path: {full_path}')
    #     sys.exit(1)

    # module_path = os.path.join(full_path, module_name)
    
    # if os.path.isdir(module_path):
    #     print(f'Path {module_path} already exists')
    #     sys.exit(1)

    # os.makedirs(module_path)

    # templates_dir = os.path.join(current_dir, 'general')
    # templates = {
    #     'controller': 'controller.template',
    #     'models': 'models.template',
    #     'repository': 'repository.template',
    #     'schemas': 'schemas.template'
    # }

    # for template_name, template_file in templates.items():
    #     template_content = Template(open(os.path.join(templates_dir, template_file)).read()).render(
    #         module_name=module_name,
    #         module_name_capital=module_name.capitalize()
    #     )
    #     with open(os.path.join(module_path, f'{template_name}.py'), 'w') as file:
    #         file.write(template_content)