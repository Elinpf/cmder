from __future__ import annotations

import os
import re
from typing import TYPE_CHECKING

import rich
from rich.prompt import Prompt
from rich.text import Text

from . import conf
from .data import pyoptions, pystrs
from .unit import get_db_path_list, get_db_selected_path, is_windows

if TYPE_CHECKING:
    from .command import Command

if not is_windows():
    from simple_term_menu import TerminalMenu


def menu_select_file(history: list = []) -> None:
    """递归选择数据库文件"""
    menu_list = []

    for path in get_db_path_list(history):
        if not os.path.exists(path):  # 如果不存在
            continue

        for e in os.listdir(path):
            e_path = os.path.join(path, e)
            if os.path.isdir(e_path):  # 如果为目录
                if e in conf.extend_dir or \
                        is_empty_dir(e_path) or \
                        e in menu_list:
                    continue
                menu_list.append(e)

            if os.path.isfile(e_path):
                if e in menu_list or e == pystrs.init_file:  # 是否为 __init__.xd 文件
                    continue
                if os.path.splitext(e)[1] == pyoptions.db_file_suffix:  # 是否为数据库文件
                    menu_list.append(e)

    # 排序
    menu_list = sorted(menu_list, key=str2int)
    blist = beautify_list(menu_list)
    for l in [menu_list, blist]:  # 添加返回
        l.append(pystrs.menu_back_str)

    # 呼出菜单
    idx = menu(os.path.join('db', *history), blist)
    selected = menu_list[idx]

    # 递归菜单
    if selected == pystrs.menu_back_str:  # 选择返回时
        if history:
            history.pop()
        return menu_select_file(history)

    # 选择文件
    selected_path = get_db_selected_path(history, selected)

    if os.path.isfile(selected_path):
        return selected_path
    else:
        history.append(selected)
        return menu_select_file(history)


def str2int(v_str):
    """排序使用"""
    s = v_str.split('_', 1)[0]

    if not s:
        return 0xffff

    if s.isdigit():
        return int(s)

    fc = s[0].lower()
    if fc.isalpha():
        return (ord(fc) + 0xff)
    else:
        return 0xffff


def is_empty_dir(path):
    """判断目录是否为空"""
    if os.listdir(path):
        return False

    return True


def filter_files(files):
    """过滤文件"""
    init = "__init__.xd"

    if init in files:
        files.remove(init)

    return files


def beautify_list(menu_list: list) -> list:
    """将文件名转化为固定格式的标题
    eg: 139_445_smb_client.xd => Smb Client (139 445)"""
    b_list = []
    for b in menu_list:
        ports = ''
        if re.match(r"^\d+_", b):
            ports = ' '.join(re.findall(r"(\d+)_", b))
            _ = re.match(r"^(\d+_)+", b).span()[1]
            b = b[_:]

        b = b.replace('.xd', '')
        b = b.replace('_', ' ')
        b = b.title()

        if ports:
            b += f' ({ports})'

        b_list.append(b)

    return b_list


def menu(title: Text | str, menu_list: list) -> int:
    """显示菜单，并返回选择的index"""
    if isinstance(title, str):
        title = Text.from_markup(title)

    if is_windows():
        idx = menu_windows(title, menu_list)
        return idx
    else:
        menu = TerminalMenu(menu_list, title=title.plain)
        return menu.show()


def menu_windows(title: Text, menu_list: list) -> int:
    """windows 的菜单选项"""
    rich.print(title)
    index = 1
    for e in menu_list:
        rich.print(f'{index}: {e}')
        index += 1

    return int(input_custom(title)) - 1


def input_custom(title: Text) -> str:
    """自定义输入，并且保存到config中"""
    selection = Prompt.ask(f":bone: [dim](custom)[/] {title.markup}")

    return selection


def menu_select_cmd_var(cmd: "Command") -> None:
    for _, var in cmd.vars.items():
        list = var.get_recommend()

        title = Text.from_markup(
            f'{var.name} [cyan][{var.desc}][/]' if var.desc else var.name)

        select = menu_with_custom_choice(title, list)
        conf.workspace_set_custom_input(var.name, select)
        var.select = select


def menu_with_custom_choice(title: Text, menu_list: list) -> str:
    if not menu_list:
        return input_custom(title)

    menu_list.append(pystrs.menu_custom_str)
    idx = menu(title, menu_list)
    selection = menu_list[idx]
    if selection == pystrs.menu_custom_str:
        return input_custom(title)
    else:
        return selection.split('(')[0].strip()
