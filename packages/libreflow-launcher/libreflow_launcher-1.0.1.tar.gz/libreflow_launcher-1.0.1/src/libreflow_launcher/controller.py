from pprint import pprint
from collections import OrderedDict
import os
import shutil
import requests
import pathlib
import unicodedata
import json
import platform
import subprocess
import toml
import re


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


class Controller():

    BASE_URL = 'http://0.0.0.0:0000'
    
    server_name = None
    server_uid = None
    
    current_user = None
    
    CONFIG = {'headers': None}
    
    poetry_path = None

    def __init__(self, servers, projects, settings):
        self._servers = servers
        self._projects = projects
        self._settings = settings

    def api_get(self, route, json):
        resp = requests.get(
            self.BASE_URL + route, json=json,
            headers=self.CONFIG['headers']
        )
        resp.raise_for_status()
        return resp.json()

    def api_post(self, route, json):
        resp = requests.post(
            self.BASE_URL + route, json=json,
            headers=self.CONFIG['headers']
        )
        resp.raise_for_status()
        return resp.json()

    def api_patch(self, route, json):
        resp = requests.patch(
            self.BASE_URL + route, json=json,
            headers=self.CONFIG['headers']
        )
        resp.raise_for_status()
        return resp.json()

    def get_token(self, data: dict) -> str:
        resp = requests.post(self.BASE_URL + '/token', data=data)
        resp.raise_for_status()
        return resp.json()


    def set_current_host(self, uid=None):
        user_settings_folder = self.user_settings_folder()
        if not os.path.exists(user_settings_folder):
            os.makedirs(user_settings_folder)

        restore = False
        if uid is None:
            try:
                f = open(f"{user_settings_folder}/current_host.json", "r")
            except IOError:
                return
            else:
                data = json.load(f)
                uid = data['uid']
                restore = True

        server = self._servers.fetch_server(uid)

        self.BASE_URL = f'http://{server["api_host"]}:{server["api_port"]}'
        self.server_name = server["display_name"]
        self.server_uid = uid

        if user_settings_folder is not None and restore is False:
            with open(f"{user_settings_folder}/current_host.json", 'w+') as f:
                json.dump(dict(
                    uid=self.server_uid
                ), f)

    def log_in(self, login, password):
        token = self.get_token({'username': login, 'password': password})

        if 'detail' in token and token['detail'] == "invalid-auth":
            print(f'ERROR: Authentification invalid to {self.server_name} server, {self.BASE_URL}')
            return False

        self.CONFIG['headers'] = {
            'Authorization': 'Bearer {}'.format(token['access_token'])}

        user_settings_folder = self.user_settings_folder()
        if not os.path.exists(user_settings_folder):
            os.makedirs(user_settings_folder)

        server_folder = f"{user_settings_folder}/servers/{self.server_uid}"
        if not os.path.exists(server_folder):
            os.makedirs(server_folder)

        config = dict(
            name=login,
            access_token=token['access_token'],
            token_type=token['token_type']
        )

        if server_folder is not None:
            with open(f"{server_folder}/current_user.json", 'w+') as f:
                json.dump(config, f)
        
        print(f'INFO: Connected to {self.server_name} server, {self.BASE_URL}')

        return True

    def log_out(self):
        self.CONFIG = {'headers': None}
        
        user_path = f"{self.user_settings_folder()}/servers/{self.server_uid}/current_user.json"
        if os.path.exists(user_path):
            os.remove(user_path)
        
        print('INFO: Logged out')

    def check_log_in(self):
        logged_in = True
        try:
            f = open(f"{self.user_settings_folder()}/servers/{self.server_uid}/current_user.json", "r")
        except IOError:
            logged_in = False
        else:
            config = json.load(f)
            self.CONFIG['headers'] = {
                'Authorization': 'Bearer {}'.format(config['access_token'])
            }

            test_command = self.api_get('/versions', json={})
            if test_command[0] == 'Not authenticated':
                logged_in = False
                print(f'INFO: Token expired for {self.server_name} server, {self.BASE_URL}')
            else:
                self.current_user = config['name']

        if logged_in:
            print(f'INFO: Connected to {self.server_name} server, {self.BASE_URL}')

        return logged_in

    def fetch_user_name(self, uid):
        try:
            f = open(f"{self.user_settings_folder()}/servers/{uid}/current_user.json", "r")
        except IOError:
            return None
        else:
            config = json.load(f)
            return config['name']


    def fetch_servers(self):
        return self._servers.fetch_servers()
    
    def update_server(self, data, uid=None):
        return self._servers.update_server(data, uid)

    def remove_server(self, uid):
        self._servers.remove_server(uid)
              
        if self.server_uid == uid:
            self.log_out()
            os.remove(f"{self.user_settings_folder()}/current_host.json")
            self.BASE_URL = 'http://0.0.0.0:0000'
            self.server_uid = None

        server_folder = f"{self.user_settings_folder()}/servers/{uid}"
        if os.path.exists(server_folder):
            shutil.rmtree(server_folder)

    def update_servers_order(self, data):
        user_settings_folder = self.user_settings_folder()

        with open(f"{user_settings_folder}/user_servers_order.json", 'w+') as f:
            json.dump(dict(uid_list=data), f)


    def fetch_projects(self):
        data = self.api_get('/projects', json={})
        # TODO: Filter projects if current site and user have been assigned
        return self._projects.fetch_projects(data, self.server_uid)

    def check_project_has_site(self, project_name):
        pass

    def check_project_has_user(self, project_name):
        return self.api_get(f'/project-check-has-user?project={project_name}&user={self.current_user}', json={})

    def update_project(self, uid):
        data = self.api_get(f'/projects/{uid}', json={})
        return self._projects.update_project(data)

    
    def update_project_env(self, project_name, project_uid, site_name='LFS'):
        # Check site name argument
        if os.environ['LF_LAUNCHER_SITE_NAME']:
            site_name = os.environ['LF_LAUNCHER_SITE_NAME']
        
        # Fetch poetry exec path
        self.fetch_poetry_path()

        # Get user config
        data_resolve = self.api_get(f'/project-resolve?project={project_name}&site={site_name}&user={self.current_user}', json={})
        data_resolve['extensions'] = sorted(data_resolve['extensions'], key=lambda x: x['name'])

        # Set env folder
        env_folder = f"{self.user_settings_folder()}/projects/{project_uid}/env"
        if not os.path.exists(env_folder):
            os.makedirs(env_folder)
        
        toml_config_path = f"{env_folder}/pyproject.toml"

        # Prepare extensions (dependencies) list
        main_dependencies = {}
        extensions_dependencies = {}

        for extension in data_resolve['extensions']:
            if not extension['version']['is_enabled']:
                continue

            # Use correct dict depend on dependencies type
            deps_dict = None

            if 'main' in extension['categories']:
                deps_dict = main_dependencies
            else:
                deps_dict = extensions_dependencies
            
            version = extension['version']

            if version['service'] == "pypi":
                # Using a specific version
                if '==' in version["pypi"]:
                    name, number = version["pypi"].split("==")
                    name = re.sub('[._+]', '-', name)
                    deps_dict[name] = number
                # Using any version
                else:
                    name = re.sub('[._+]', '-', version["pypi"])
                    deps_dict[name] = {"version": "*"}
                    
                    if "--pre" in version["pip_deps"]:
                        deps_dict[name]["allow-prereleases"] = "true"
            
            elif version['service'] == "gitlab":
                name = re.sub('[._+]', '-', extension['name'])

                if version['url']:
                    deps_dict[name] = {"git": version['url']}
                else:
                    git_url = f'https://gitlab.com/{version["repo_group"]}/{version["repo_project"]}.git'
                    deps_dict[name] = {"git": git_url}
                
                if version['repo_ref_type'] == "branch":
                    deps_dict[name]["branch"] = version['repo_ref']
                elif version['repo_ref_type'] == "commit":
                    deps_dict[name]["rev"] = version['repo_ref']
            
            elif version['service'] == "gitlab-url":
                name = re.sub('[._+]', '-', extension['name'])
                deps_dict[name] = {"git": version['url']}

        # Format for toml config
        main_dependencies_string = """"""
        for name, options in main_dependencies.items():
            main_dependencies_string += f"{name} = "
            if type(options) is not dict:
                main_dependencies_string += f'"{options}"\n'
            else:
                for i, (option_name, option_value) in enumerate(main_dependencies[name].items()):
                    if i > 0:
                        if option_name == "allow-prereleases":
                            main_dependencies_string += ', {name} = {value}'.format(name=option_name, value=option_value)
                        else:
                            main_dependencies_string += ', {name} = "{value}"'.format(name=option_name, value=option_value)
                    else:
                        main_dependencies_string += '{{ {name} = "{value}"'.format(name=option_name, value=option_value)
                    
                    if i == len(main_dependencies[name].items())-1:
                        main_dependencies_string += ' }'
                    
                main_dependencies_string += "\n"
        
        extensions_dependencies_string = """"""
        if len(extensions_dependencies) > 0:
            for name, options in extensions_dependencies.items():
                extensions_dependencies_string += f"{name} = "
                if type(options) is not dict:
                    extensions_dependencies_string += f'"{name}"\n'
                else:
                    for i, (option_name, option_value) in enumerate(extensions_dependencies[name].items()):
                        if i > 0:
                            extensions_dependencies_string += ', {name} = "{value}"'.format(name=option_name, value=option_value)
                        else:
                            extensions_dependencies_string += '{{ {name} = "{value}"'.format(name=option_name, value=option_value)
                        
                        if i == len(extensions_dependencies[name].items())-1:
                            extensions_dependencies_string += ' }'
                        
                    extensions_dependencies_string += "\n"
            
        # Create toml content
        toml_content = """
            [tool.poetry]
            name = "{project_name}-poetry"
            version = "0.1.0"
            description = ""
            authors = ["Les Fees Speciales <voeu@les-fees-speciales.coop>"]

            [tool.poetry.dependencies]
            python = "{python_version}"
            {main_list}
            [tool.poetry.group.extensions.dependencies]
            {extensions_list}
            
            [build-system]
            requires = ["poetry-core"]
            build-backend = "poetry.core.masonry.api"
        """.format(
            project_name=project_name,
            python_version=self._settings.fetch_key('python_version'),
            main_list=main_dependencies_string,
            extensions_list=extensions_dependencies_string
        )
        
        # Move current process to env folder
        store_base_path = os.getcwd()
        os.chdir(env_folder)

        update = True
        if not os.path.exists(toml_config_path):
            update = False

        with open(toml_config_path, "w") as f:
            f.write(toml_content)
            f.close()

        # If config exists, we use update command
        if update:
            subprocess.call([self.poetry_path, "update"])
        # Or we make the first install
        else:
            subprocess.call([self.poetry_path, "install"])
        
        os.chdir(store_base_path)

        return data_resolve, env_folder

    def start_project(self, project_uid, data_resolve=None):
        env_folder = f"{self.user_settings_folder()}/projects/{project_uid}/env"
        
        # Move current process to env folder
        store_base_path = os.getcwd()
        os.chdir(env_folder)
        
        update = False
        if data_resolve:
            update = True

            # Format Kabaret Flow Extensions argument
            extensions = []
            for extension in data_resolve['extensions']:
                if 'extension' in extension['categories']:
                    extensions.append(f'libreflow.extensions.{extension["name"]}:install_extensions')
            
            extensions = f'set KABARET_FLOW_EXT_INSTALLERS={";".join(extensions)}'

            # Format launch command with arguments
            cmd = [
                self.poetry_path,
                "run",
                "python",
                "-m",
                "libreflow.flows.gui",
                "--host",
                data_resolve['redis_url'],
                "--port",
                str(data_resolve['redis_port']),
                "--db",
                str(data_resolve['redis_db']),
                "--cluster",
                data_resolve['redis_cluster'],
                "--session",
                "libreflow",
                "--site",
                "lfs",
                "--password",
                data_resolve['redis_password'],
                "--search-index-uri",
                data_resolve["mongo_url"],
            ]
        
        if platform.system() == "Windows":
            exec_path = f"{env_folder}/libreflow.bat"
            if update:
                with open(exec_path, 'w+') as f:
                    cmd.append('\npause')
                    f.write('@echo off\n\n')
                    f.write(extensions)
                    f.write('\n\n')
                    f.write(' '.join(cmd))

            subprocess.Popen(exec_path, creationflags=subprocess.CREATE_NEW_CONSOLE)
        
        elif platform.system() == "Linux":
            # TODO
            pass
        
        os.chdir(store_base_path)


    def fetch_settings(self):
        return self._settings.fetch_settings()
    
    def update_settings(self, data):
        return self._settings.update_settings(data)
    
    def fetch_python_versions(self):
        versions = []

        if platform.system() == "Windows":
            list_paths = subprocess.Popen("py --list-paths", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            list_paths = list_paths.communicate()[0].decode().splitlines()
            for p in list_paths:
                path = p.split(' ')[-1]
                if path:
                    version_number = subprocess.check_output(f"{path} --version").decode()
                    versions.append(dict(
                        version=re.findall(r'(?:(\d+\.(?:\d+\.)*\d+))', version_number)[0],
                        path=path
                    ))
        elif platform.system() == "Linux":
            list_paths = subprocess.Popen(['whereis', 'python'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            list_paths = list_paths.communicate()[0].decode()[8:-1].split(' ')
            for path in list_paths:
                if path.endswith('config'):
                    continue
                try:
                    version_number = subprocess.Popen([path, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    if version_number.communicate()[1].decode() == "":
                        version_number = re.findall(r'(?:(\d+\.(?:\d+\.)*\d+))', version_number.communicate()[0].decode())[0]
                    else:
                        version_number = re.findall(r'(?:(\d+\.(?:\d+\.)*\d+))', version_number.communicate()[1].decode())[0]
                    
                    added = False
                    for v in versions:
                        if v['version'] == version_number:
                            added = True
                            break
                    
                    if not added:
                        versions.append(dict(
                            version=version_number,
                            path=path
                        ))
                except IOError as e:
                    continue
        
        return sorted(versions, key=lambda d: d['version'])

    def fetch_poetry_path(self):
        if platform.system() == "Windows":
            self.poetry_path = f"{pathlib.Path.home()}/AppData/Roaming/Python/Scripts/poetry"
        elif platform.system() == "Linux":
            self.poetry_path = f"{pathlib.Path.home()}/.local/bin/poetry"

    def user_settings_folder(self):
        return os.path.join(pathlib.Path.home(), '.libreflow_launcher')

    def resolve_value(self, value, project={}):
        resolved = value.format(
            user_settings=self.user_settings_folder(),
            project_uid=project
        )

        return resolved
