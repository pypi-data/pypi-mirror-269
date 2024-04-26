import sys
import os
import json
import pprint
import pathlib
import re
import unicodedata
import uuid


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')

def user_settings_folder():
    return os.path.join(pathlib.Path.home(), '.libreflow_launcher')


class Servers():

    def __init__(self):
        self._servers = []
        self.servers_dir = os.path.dirname(__file__)+'/data/servers'

    def fetch_servers(self):
        self._servers = []

        for server in os.listdir(self.servers_dir):
            uid, ext = os.path.splitext(server)
            if ext == '.json':
                config_path = os.path.join(self.servers_dir, server)
                with open(config_path, "r") as f:
                    data = json.loads(f.read())

                self._servers.append(data)
        
        try:
            f = open(f"{user_settings_folder()}/user_servers_order.json", "r")
        except IOError:
            pass
        else:
            user_data = json.load(f)['uid_list']
            self._servers = sorted(self._servers, key=lambda s: user_data.index(s['uid']))

        print(f'INFO: Fetch {len(self._servers)} servers')
        return self._servers

    def fetch_server(self, uid):
        item = [s for s in self._servers if s['uid'] == uid]
        return item[0]

    def update_server(self, data, uid=None):
        config_path = os.path.join(self.servers_dir, '{uid}.json')

        if not uid:
            uid = str(uuid.uuid4())
            data.update(dict(
                code=''.join([x[0].upper() for x in data['display_name'].split(' ')]),
                uid=uid,
            ))
        else:
            for i, s in enumerate(self._servers):
                if s['uid'] == uid:
                    for key in data:
                        if key == 'display_name':
                            self._servers[i]['code'] = ''.join([x[0].upper() for x in data[key].split(' ')])
                        self._servers[i][key] = data[key]
                    data = self._servers[i]

        config_path = config_path.format(uid=uid)
        with open(config_path, 'w') as f:
            json.dump(data, f)
        
        return uid

    def remove_server(self, uid):
        for server in os.listdir(self.servers_dir):
            local_uid, ext = os.path.splitext(server)
            if local_uid == uid and ext == '.json':
                config_path = os.path.join(self.servers_dir, server)
                os.remove(config_path)

                for i, s in enumerate(self._servers):
                    if s['uid'] == uid:
                        self._servers.pop(i)
                        break


class Projects():

    def __init__(self):
        self._projects = []
        self.projects_dir = f'{user_settings_folder()}/projects'

    def fetch_projects(self, data_remote, server_uid):
        if not os.path.exists(self.projects_dir):
            os.makedirs(self.projects_dir)
        
        # Clear all projects loaded
        self._projects = [loaded_data for loaded_data in self._projects if loaded_data['server_uid'] != server_uid]

        for remote in data_remote:
            status = True
            data = remote

            local_path = f'{self.projects_dir}/{remote["uid"]}'
            config_path = os.path.join(local_path, 'config.json')

            # Check if remote has changed
            if os.path.exists(config_path):
                with open(config_path, "r") as f:
                    local = json.loads(f.read())
                    data = local

                if local != remote:
                    status = False
                
            else:
                os.makedirs(local_path)
                with open(config_path, 'w') as f:
                    json.dump(remote, f)
            
            # Check if there is a env
            env_folder = os.path.join(local_path, 'env')
            if not os.path.exists(env_folder):
                status = None

            self._projects.append(dict(server_uid=server_uid, updated=status, data=data))
        
        print(f'INFO: Fetch {len(data_remote)} projects')
       
        return self._projects

    def update_project(self, data_remote):
        local_path = f'{self.projects_dir}/{data_remote["uid"]}'
        config_path = os.path.join(local_path, 'config.json')

        for i, loaded_data in enumerate(self._projects):
            if loaded_data['data']['uid'] == data_remote['uid']:
                with open(config_path, 'w') as f:
                    json.dump(data_remote, f)

                self._projects[i]['data'] = data_remote
                self._projects[i]['updated'] = True
                break
        
        return self._projects[i]


class Settings():

    def __init__(self):
        self._settings = {}
        self.settings_path = os.path.join(user_settings_folder(), 'user_settings.json')
        self.fetch_settings()

    def fetch_settings(self):
        if os.path.exists(self.settings_path):
            with open(self.settings_path, "r") as f:
                local = json.loads(f.read())
                self._settings.update(local)
        else:
            if not os.path.exists(user_settings_folder()):
                os.makedirs(user_settings_folder())
            
            with open(self.settings_path, 'w') as f:
                default_data = dict(
                    install_dir="{user_settings}/projects/{project_uid}/env",
                    python_path=sys.executable,
                    python_version=re.match(r"([^\s]+)", sys.version).group(1)
                )
                json.dump(default_data, f)
                self._settings.update(default_data)
        
        return self._settings
    
    def fetch_key(self, key):
        return self._settings[key]
    
    def update_settings(self, data):
        for key in data:
            self._settings[key] = data[key]

        with open(self.settings_path, 'w') as f:
            json.dump(self._settings, f)
