import os
import cmder.unit as unit
from cmder.config import Config


root_path = unit.get_root_path()

db_path = unit.get_db_path()


def generate_custom_file_path():
    """创建并返回用户配置文件夹"""
    user_path = os.path.expanduser('~')
    custom_cmder_path = os.path.join(user_path, '.cmder')
    if not os.path.exists(custom_cmder_path):
        os.makedirs(custom_cmder_path)

    custom_db_path = os.path.join(custom_cmder_path, 'db')
    if not os.path.exists(custom_db_path):
        os.makedirs(custom_db_path)

    return custom_cmder_path


custom_file_path = generate_custom_file_path()

conf = Config('config.json')
