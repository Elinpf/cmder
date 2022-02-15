import os
import platform
from colorama import Fore, Style
from typing import List
from .data import pypaths, pystrs, pyoptions


def is_windows():
    return platform.system() == 'Windows'


def is_linux():
    return platform.system() == 'Linux'


def db_recursion_file(file_path: str) -> List[str]:
    """用于对指定的文件递归查询所有存在的__init__.xd文件,
    以及用户目录下自定义的文件
    返回List """

    relate_path = get_relate_path(file_path)

    if is_windows():
        path_split_list = relate_path.split(pyoptions.windows_separator)
    else:
        path_split_list = relate_path.split(pyoptions.linux_separator)

    p = pypaths.root_path
    c = pypaths.custom_path
    list = []
    for i in path_split_list:
        p = os.path.join(p, i)
        c = os.path.join(c, i)

        for init_path in [os.path.join(p, pystrs.init_file), os.path.join(c, pystrs.init_file)]:
            if not os.path.exists(init_path):
                continue

            list.append(init_path)

    # 判断是否文件是否存在, 并在list 中返回
    for file in get_path_list(file_path):
        if os.path.exists(file):
            list.append(file)

    return list


def get_select_path(path: str, select: str) -> str:
    """获取选择的文件，如果在软件目录中不存在，就返回用户目录的路径"""
    for p in get_path_list(path):
        p_select = os.path.join(p, select)
        if os.path.exists(p_select):
            return p_select
    return ''


def get_relate_path(path: str) -> str:
    """获取相对路径"""
    relate_path = path.replace(pypaths.db_path, 'db')
    relate_path = relate_path.replace(pypaths.custom_db_path, 'db')
    return relate_path


def get_path_list(path: str) -> List[str, str]:
    """取软件目录与用户目录的list"""
    relate_path = get_relate_path(path)
    root_path = os.path.join(pypaths.root_path, relate_path)
    custom_path = os.path.join(pypaths.custom_path, relate_path)
    return [root_path, custom_path]


def store_file(file_relate_path: str, string: str):
    """用于存储文件, 
    file_relate_path 是相对与用户目录下的文件路径"""
    fi = open_custom_file(file_relate_path, 'w')
    fi.write(string)
    fi.close()


def open_custom_file(file_relate_path: str, mode: str) -> object:
    """打开用户目录中的文件"""
    file_path = custom_abspath(file_relate_path)
    fi = open(file_path, mode)
    return fi


def custom_abspath(file_relate_path: str) -> str:
    """返回用户目录绝对路径"""
    return os.path.join(pypaths.custom_path, file_relate_path)


def escap_chars(string: str) -> str:
    """转义一些字符"""
    if is_linux():
        string = string.replace('\\', '\\\\')
        string = string.replace('!', '\!')

    return string


class Colored():
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    ORANGE = '\033[0;33;1m'
    BLUE = Fore.BLUE
    FUCHSIA = '\033[35m'
    WHITE = Fore.WHITE

    def color_str(self, color: str, s: str, bright: bool = False) -> str:

        if bright:
            return '{}{}{}'.format(getattr(self, color) + Style.BRIGHT, s, Style.RESET_ALL)
        else:
            return '{}{}{}'.format(getattr(self, color), s, Style.RESET_ALL)

    def red(self, s):
        return self.color_str('RED', s)

    def green(self, s):
        return self.color_str('GREEN', s)

    def yellow(self, s):
        return self.color_str('YELLOW', s)

    def orange(self, s):
        return self.color_str('ORANGE', s)

    def blue(self, s):
        return self.color_str('BLUE', s)

    def fuchsia(self, s):
        return self.color_str('FUCHSIA', s)

    def white(self, s):
        return self.color_str('WHITE', s)

    def red_bright(self, s):
        return self.color_str('RED', s, True)

    def green_bright(self, s):
        return self.color_str('GREEN', s, True)

    def yellow_bright(self, s):
        return self.color_str('YELLOW', s, True)

    def orange_bright(self, s):
        return self.color_str('ORANGE', s, True)

    def blue_bright(self, s):
        return self.color_str('BLUE', s, True)

    def fuchsia_bright(self, s):
        return self.color_str('FUCHSIA', s, True)

    def white_bright(self, s):
        return self.color_str('WHITE', s, True)
