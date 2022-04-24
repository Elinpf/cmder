import os

from .config import Config
from .data import pypaths, pystrs
from .unit import custom_abspath

__version__ = '2.2.2'


def generate_custom_file_path():
    """创建并返回用户配置文件夹"""
    if not os.path.exists(pypaths.custom_path):
        os.makedirs(pypaths.custom_path)

    if not os.path.exists(pypaths.custom_db_path):
        os.makedirs(pypaths.custom_db_path)

    if not os.path.exists(pypaths.custom_script_path):
        os.makedirs(pypaths.custom_script_path)

    if not os.path.exists(pypaths.history_path):
        open(pypaths.history_path, 'a').close()


generate_custom_file_path()

conf = Config(custom_abspath(pystrs.config_file))
