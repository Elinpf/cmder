import os
import re

import src
from src.unit import is_windows
from colorama import Fore, Style

if not is_windows():
    from simple_term_menu import TerminalMenu


def menu_select_file(path):
    """用于递归做文件的选择"""

    menu_list = []
    back_title = '(Back)'

    for p in src.unit.get_path_list(path):  # 软件与用户目录的两次循环
        if not os.path.exists(p):
            continue

        for f in os.listdir(p):  # 取目录下的文件名
            f_path = os.path.join(p, f)
            if os.path.isdir(f_path):  # 如果是目录
                if f in src.conf.extend_dir:
                    continue

                if is_empty_dir(f_path):  # 并且目录内不为空
                    continue

                if f not in menu_list:  # 并且菜单列表中没有文件名称
                    menu_list.append(f)  # 则添加

            else:
                if f not in menu_list:
                    if os.path.splitext(f)[1] == '.xd':  # 后缀为.xd的
                        menu_list.append(f)

    # 排序
    menu_list = sorted(menu_list, key=str2int)

    # 美化，并呼出菜单
    b_list = beautify_list(filter_files(menu_list))
    b_list.append(back_title)
    menu_list.append(back_title)
    idx = menu(path, b_list)

    select = menu_list[idx]

    # 递归菜单
    if select == back_title:
        back_path = os.path.split(path)[0]
        if len(back_path) < len(src.db_path):
            back_path = src.db_path
        return menu_select_file(back_path)

    select_path = src.unit.get_select_path(path, select)
    if os.path.isdir(select_path):
        return menu_select_file(select_path)

    elif os.path.isfile(select_path):
        return select_path


def tryint(s):
    try:
        return int(s)
    except:
        return s


def str2int(v_str):
    return [tryint(s) for s in v_str.split("_", 2)]


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


def beautify_list(menu_list):
    """将文件名转化为固定格式的标题
    eg: 139_445_smb_client.xd => Smb Client (139 445)"""
    b_list = []
    ports = ''
    for b in menu_list:
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


def menu(title, menu_list):
    """显示菜单，并返回选择的index"""
    if is_windows():
        idx = menu_windows(title, menu_list)
        return idx
    else:
        menu = TerminalMenu(menu_list, title=title)
        return menu.show()


def menu_windows(title, menu_list):
    """windows 的菜单选项"""
    print(title)
    index = 1
    for e in menu_list:
        print(f'{index}: {e}')
        index += 1

    return int(input_custom(title)) - 1


def input_custom(title):
    """自定义输入，并且保存到config中"""
    print(f'(custom) {title}')
    try:
        selection = input(Fore.RED + Style.BRIGHT + '> ' + Style.RESET_ALL)
    except (InterruptedError, KeyboardInterrupt):
        exit()

    return selection


def menu_select_cmd_var(cmd):
    for _, var in cmd.vars.items():
        list = var.get_recomm()

        if var.desc:
            title = f'{var.name}: {var.desc}'
        else:
            title = var.name

        select = menu_with_custom_choice(title, list)
        src.conf.workspace_set_custom_input(var.name, select)
        var.select = select


def menu_with_custom_choice(title, menu_list):
    if not menu_list:
        return input_custom(title)

    menu_list.append('(Custom)')
    idx = menu(title, menu_list)
    selection = menu_list[idx]
    if selection == '(Custom)':
        return input_custom(title)
    else:
        return selection.split('(')[0].strip()
