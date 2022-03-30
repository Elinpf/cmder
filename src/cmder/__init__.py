import os

from rich.prompt import Confirm
from rich_typer import Exit

from .config import Config
from .data import pypaths, pystrs
from .unit import Colored, update_database

__version__ = '2.0.0'


def generate_custom_file_path():
    """创建并返回用户配置文件夹"""
    if not os.path.exists(pypaths.custom_path):
        os.makedirs(pypaths.custom_path)

    if not os.path.exists(pypaths.custom_db_path):
        os.makedirs(pypaths.custom_db_path)

    if not os.path.exists(pypaths.history_path):
        open(pypaths.history_path, 'a').close()


def check_db():
    """检查数据库是否存在"""
    if not os.path.exists(pypaths.db_path):
        if not Confirm.ask(f'cmder database not found, do you want to create?', default=True):
            raise Exit()

        update_database()


generate_custom_file_path()

cool = Colored()

conf = Config(pystrs.config_file)
