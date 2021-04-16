import os
import json
import src


class Config():

    def __init__(self, config_path):
        self.conf = {}
        self.config_abspath = None
        self.load(config_path)

    def load(self, config_path):
        """加载配置文件, 如果没有则创建"""
        self.config_abspath = src.unit.custom_abspath(config_path)
        if os.path.exists(self.config_abspath):
            json_str = open(self.config_abspath, 'r').read()
            self.conf = json.loads(json_str)
        else:
            self.generate_conf()

    def save(self):
        """保存config文件"""
        json_str = json.dumps(self.conf, indent=4,
                              sort_keys=True, separators=(',', ': '))
        with open(self.config_abspath, 'w') as fi:
            fi.write(json_str)

    def generate_conf(self):
        self.conf = {
            'workspace_select': 'default',
            'workspaces': {
                'default': {
                    'variable': {},
                    'custom_input': {}
                }
            },
            'latest_select': '',
            'extend_dir': ['.git'],
            'history_size': 50
        }
        self.save()

    @property
    def extend_dir(self):
        return self.conf['extend_dir']

    @property
    def history_size(self):
        return self.conf['history_size']

    @history_size.setter
    def history_size(self, v: int):
        if v < 0:
            self.conf['history_size'] = 0
        else:
            self.conf['history_size'] = v
        self.save()

    def add_workspace(self, name):
        """添加工作区"""
        self.conf['workspaces'][name] = {'variable': {}, 'custom_input': {}}
        self.conf['workspace_select'] = name
        self.save()

    def del_workspace(self, name):
        """删除工作区"""
        if not name in self.workspaces_name():
            raise ValueError(f"{name} not in workspace.")

        if self.conf['workspace_select'] == name:
            raise ValueError(f"{name} is current workspace, can't delete.")

        self.conf['workspaces'].pop(name)
        self.save()

    def workspaces_name(self):
        """返回所有工作区名称"""
        return self.conf['workspaces'].keys()

    def workspace_now(self):
        """返回现在工作区名称"""
        return self.conf['workspace_select']

    def workspace_change(self, name):
        """切换工作区"""
        if name in self.workspaces_name():
            self.conf['workspace_select'] = name
            self.save()

    def workspace_set(self, key, val):
        """设置配置"""
        now = self.workspace_now()
        workspace = self.conf['workspaces'][now]
        workspace[key] = val
        self.save()

    def workspace_get(self, key):
        """获取配置"""
        now = self.workspace_now()
        workspace = self.conf['workspaces'][now]
        return workspace[key]

    def workspace_set_var(self, key, val):
        """设置工作区变量信息"""
        workspace_var = self.workspace_get('variable')
        if key in workspace_var:
            workspace_var[key].append(val)
        else:
            workspace_var[key] = [val]
        self.save()

    def workspace_get_var(self, key):
        """获取工作区变量信息 return List"""
        workspace_var = self.workspace_get('variable')
        return workspace_var[key]

    def workspace_unset_var(self, key):
        workspace_var = self.workspace_get('variable')
        del workspace_var[key]
        self.save()

    def workspace_get_var_keys(self):
        """获取工作区变量的keys"""
        workspace_var = self.workspace_get('variable')
        return workspace_var.keys()

    def workspace_var_key_with_val(self):
        """获取变量的key和val"""
        for key in self.workspace_get_var_keys():
            val = self.workspace_get_var(key)
            for v in val:
                yield (key, v)

    def workspace_set_custom_input(self, key, val):
        """设置用户最近一次输入的变量"""
        workspace_custom = self.workspace_get('custom_input')
        workspace_custom[key] = val
        self.save()

    def workspace_get_custom_input(self, key):
        """获取用户最近一次的变量输入"""
        workspace_custom = self.workspace_get('custom_input')
        return workspace_custom[key]

    def workspace_get_custom_input_keys(self):
        """获取用户输入的keys"""
        return self.workspace_get('custom_input').keys()

    def workspace_custom_key_with_val(self):
        """获取用户输入的key和val"""
        for key in self.workspace_get_custom_input_keys():
            val = self.workspace_get_custom_input(key)
            yield (key, val)

    @property
    def latest_select(self):
        return self.conf['latest_select']

    @latest_select.setter
    def latest_select(self, string):
        self.conf['latest_select'] = string
        self.save()
