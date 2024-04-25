import configparser
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
    generate_security_module(project_name, module_config.module_path)


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


def generate_security_module(project_name: str, module_path: str):
    security_path_template = os.path.join(
        project_name, 'libs', 'security', 'security.template'
    )
    security_path_py = os.path.join(
        project_name, 'libs', 'security', 'security.py'
    )
    with open(security_path_template, 'r') as file:
        template = file.read()
    import_string = module_path.replace('/', '.')
    if import_string.endswith('.'):
        import_string = import_string[:-1]
    security_module = Template(template).render(module_path=import_string)
    with open(security_path_template, 'w') as file:
        file.write(security_module)
    os.rename(security_path_template, security_path_py)


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


def new_module(project_name: str, module_name: str, module_path: str):
    current_dir = os.path.dirname(__file__)
    general_module_path = os.path.join(current_dir, 'general')
    full_path_module = os.path.abspath(os.path.join(project_name,module_path, module_name))
    if os.path.isdir(full_path_module):
        print(f'{full_path_module} already exists')
    
    os.makedirs(full_path_module)
    print('gen files')
    for current_file in ['controller', 'models', 'repository', 'schemas']:
        with open(os.path.join(general_module_path, f'{current_file}.template'), 'r') as file:
            template = Template(file.read())
            module_path_python = module_path.replace('/', '.')
            if module_path_python.endswith('.'):
                module_path_python = module_path_python[:-1]
            file_content = template.render(module_name=module_name, module_name_capital=module_name.capitalize(), module_path=module_path_python)
            with open(os.path.join(full_path_module, f'{current_file}.py'), 'w') as python_file:
                python_file.write(file_content)
    force_uvicorn_reload(project_name)
    print('done')

def force_uvicorn_reload(project_name: str):
    with open(f'{project_name}/main.py', 'a+') as file:
    # Posicionar o cursor no início do arquivo
        file.seek(0)

        # Ler o conteúdo existente, se houver
        content = file.read()

        # Adicionar novo conteúdo ao arquivo


        # Se o arquivo já tiver conteúdo, adicione uma quebra de linha antes do novo conteúdo
        if content:
            file.write('\n')

        # Escrever o conteúdo anterior de volta para o arquivo (para não perdê-lo)
        file.write(content)