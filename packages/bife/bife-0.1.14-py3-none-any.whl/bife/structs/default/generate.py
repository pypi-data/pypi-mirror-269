import os
import shutil
import sys

from mako.template import Template

from ...config import DatabaseConfig, ModuleConfig, UserConfig

DEPENDENCIES = [
    'fastapi',
    'pyjwt',
    'argon2-cffi',
    'sqlalchemy',
    'python-dotenv',
    'uvicorn',
]


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
            os.path.join(current_dir, directory),
            os.path.join(path, directory.split('/')[-1]),
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


import os
import subprocess

import toml

# def check_is_poetry():
#     if not os.path.isfile('pyproject.toml'):
#         print('pyproject.toml not found')
#         return False
#     try:
#         with open('pyproject.toml', 'r') as file:
#             toml_content = toml.load(file)
#         if 'tool' in toml_content and 'poetry' in toml_content['tool']:
#             dependencies = toml_content['tool']['poetry'].get('dependencies', None)
#             if dependencies:
#                 packages = ' '.join([f"{package}{version}" for package, version in dependencies.items()])
#                 subprocess.run(['poetry', 'add', packages], check=True)
#                 print("Dependências adicionadas com sucesso usando Poetry.")
#                 return

#         raise ValueError("Arquivo 'pyproject.toml' não parece ser do Poetry.")

#     except Exception as e:
#         print(f"Erro ao processar 'pyproject.toml': {e}")
#         print("Instalando dependências usando pip...")
#         subprocess.run(['pip', 'install', '-r', 'requirements.txt'], check=True)
#         print("Dependências instaladas com sucesso usando pip.")


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
