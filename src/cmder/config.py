import json
import os
from typing import Generator, Tuple

from . import unit


class Config():

    def __init__(self, config_path: str):
        self.conf = {}
        self.config_abspath = config_path
        self.load()

    def load(self) -> None:
        """加载配置文件, 如果没有则创建"""
        if os.path.exists(self.config_abspath):
            json_str = open(self.config_abspath, 'r').read()
            self.conf = json.loads(json_str)
        else:
            self.generate_conf()

    def save(self) -> None:
        """保存config文件"""
        json_str = json.dumps(self.conf, indent=4,
                              sort_keys=True, separators=(',', ': '))
        with open(self.config_abspath, 'w') as fi:
            fi.write(json_str)

    def init_config(self) -> None:
        """初始化配置"""
        self.generate_conf()

    def generate_conf(self) -> None:
        self.conf = {
            'workspace_select': 'default',
            'workspaces': {
                'default': {
                    'variable': {},
                    'custom_input': {}
                }
            },
            'history_select': [],
            'extend_dir': ['.git'],
            'history_size': 50,
            'global_config': {}
        }
        self.save()

    @property
    def extend_dir(self) -> list:
        return self.conf['extend_dir']

    @property
    def history_size(self) -> int:
        return self.conf['history_size']

    @history_size.setter
    def history_size(self, v: int) -> None:
        if v < 0:
            self.conf['history_size'] = 0
        else:
            self.conf['history_size'] = v
        self.save()

    @property
    def global_config(self) -> dict:
        self.check_global_config()
        return self.conf['global_config']

    def init_global_config(self) -> None:
        """初始化全局配置"""
        self.conf['global_config'] = {}
        self.save()

    def set_global_config(self, conf: Tuple[str, str]) -> None:
        """设置全局配置中的一个配置"""
        key, val = conf
        self.global_config[key] = val
        self.save()

    def get_global_config(self, key) -> str:
        """获取全局配置中的一个配置"""
        if key in self.global_config:
            return self.global_config[key]

    def del_global_config(self, key) -> None:
        """删除一个全局配置"""
        if key in self.global_config:
            self.global_config.pop(key)
            self.save()

    def check_global_config(self) -> None:
        """检查是否有全局配置，低版本兼容"""
        if 'global_config' not in self.conf:
            self.init_global_config()

    def add_workspace(self, name: str) -> None:
        """添加工作区"""
        self.conf['workspaces'][name] = {'variable': {}, 'custom_input': {}}
        self.conf['workspace_select'] = name
        self.save()

    def del_workspace(self, name: str) -> None:
        """删除工作区"""
        if not name in self.workspaces_name():
            raise ValueError(f"[cyan]{name}[/cyan] not in workspace.")

        if self.conf['workspace_select'] == name:
            raise ValueError(
                f"[cyan]{name}[/cyan] is current workspace, can't delete.")

        self.conf['workspaces'].pop(name)
        self.save()

    def workspaces_name(self) -> str:
        """返回所有工作区名称"""
        return self.conf['workspaces'].keys()

    def workspace_now(self) -> str:
        """返回现在工作区名称"""
        return self.conf['workspace_select']

    def workspace_change(self, name):
        """切换工作区"""
        if name in self.workspaces_name():
            self.conf['workspace_select'] = name
            self.save()

    def workspace_set(self, key: str, val: str) -> None:
        """设置配置"""
        now = self.workspace_now()
        workspace = self.conf['workspaces'][now]
        workspace[key] = val
        self.save()

    def workspace_get(self, key: str) -> dict:
        """获取配置"""
        now = self.workspace_now()
        workspace = self.conf['workspaces'][now]
        return workspace[key]

    def workspace_set_var(self, key: str, val: str) -> None:
        """设置工作区变量信息"""
        workspace_var = self.workspace_get('variable')
        if key in workspace_var:
            if val not in workspace_var[key]:
                workspace_var[key].append(val)
        else:
            workspace_var[key] = [val]
        self.save()

    def workspace_get_var(self, key: str) -> list:
        """获取工作区变量信息 return List"""
        workspace_var = self.workspace_get('variable')
        return workspace_var[key]

    def workspace_unset_var(self, key: str) -> None:
        workspace_var = self.workspace_get('variable')
        del workspace_var[key]
        self.save()

    def workspace_get_var_keys(self) -> list:
        """获取工作区变量的keys"""
        workspace_var = self.workspace_get('variable')
        return workspace_var.keys()

    def workspace_var_key_with_val(self) -> Generator[Tuple[str, str], None, None]:
        """获取变量的key和val"""
        for key in self.workspace_get_var_keys():
            val = self.workspace_get_var(key)
            for v in val:
                yield (key, v)

    def workspace_set_custom_input(self, key: str, val: str) -> None:
        """设置用户最近一次输入的变量"""
        workspace_custom = self.workspace_get('custom_input')
        if val:
            workspace_custom[key] = val
            self.save()

    def workspace_get_custom_input(self, key: str) -> str:
        """获取用户最近一次的变量输入"""
        workspace_custom = self.workspace_get('custom_input')
        return workspace_custom[key]

    def workspace_get_custom_input_keys(self) -> list:
        """获取用户输入的keys"""
        return self.workspace_get('custom_input').keys()

    def workspace_custom_key_with_val(self) -> Generator[Tuple[str, str], None, None]:
        """获取用户输入的key和val"""
        for key in self.workspace_get_custom_input_keys():
            val = self.workspace_get_custom_input(key)
            yield (key, val)

    @property
    def latest_select(self) -> str:
        if len(self.history_select) == 0:
            return ''

        return self.history_select[0]

    @latest_select.setter
    def latest_select(self, string: str) -> None:
        if self.latest_select == string:
            return

        self.history_select = unit.get_relate_path(string)

    @property
    def history_select(self) -> list:
        return self.conf['history_select']

    @history_select.setter
    def history_select(self, string: str) -> None:
        tmp = self.conf['history_select']
        tmp.insert(0, string)
        self.conf['history_select'] = tmp[:5]
        self.save()
