from __future__ import annotations

import base64
import os
import platform
import re
import shlex
import subprocess
from contextlib import contextmanager
from typing import Iterator, List

import rich_typer as typer
from rich.panel import Panel

from .console import console
from .data import database_url, pyoptions, pypaths, pystrs


def is_windows():
    return platform.system() == 'Windows'


def is_linux():
    return platform.system() == 'Linux'


def encode_base64(string: str) -> str:
    """base64编码"""
    return str(base64.b64encode(string.encode('utf-8')))[2:-1]


def decode_base64(string: str) -> str:
    return str(base64.b64decode(string).decode('utf-8'))


def encode_multi_line_notes(string: str) -> str:
    """将多行注释编码为单行注释"""
    match = re.findall(pyoptions.multi_line_note_pattern, string)
    if match:
        for m in match:
            rep_str = "{}:{}".format(
                pyoptions.encode_flag, encode_base64(m))
            string = string.replace('"""{}"""'.format(m), rep_str)

    return string


def decode_multi_line_notes(encode_str: str) -> str:
    """将单行编码注释转换为多行注释"""
    encode_str = encode_str.replace(pyoptions.encode_flag + ':', '')
    decode_str = decode_base64(encode_str)
    return decode_str


def db_recursion_file(file_path: str) -> List[str]:
    """用于对指定的文件递归查询所有存在的__init__.xd文件,
    以及用户目录下自定义的文件
    返回List """

    relate_path = get_relate_path(file_path)

    if is_windows():
        path_split_list = relate_path.split(pyoptions.windows_separator)[
            1:]  # 去除db/的路径list
    else:
        path_split_list = relate_path.split(pyoptions.linux_separator)[1:]

    p = pypaths.db_path
    c = pypaths.custom_db_path
    list = []
    path_split_list.insert(0, '')  # 添加空字符串是为了让第一个路径为空
    for i in path_split_list:
        p = os.path.join(p, i)
        c = os.path.join(c, i)

        for init_path in [os.path.join(p, pystrs.init_file), os.path.join(c, pystrs.init_file)]:
            if not os.path.exists(init_path):
                continue

            list.append(init_path)

    # 判断是否文件是否存在, 并在list 中返回
    for file in get_db_path_list(path_split_list):
        if os.path.exists(file):
            list.append(file)

    return list


def get_relate_path(path: str) -> str:
    """获取相对路径"""
    relate_path = path.replace(pypaths.db_path, 'db')
    relate_path = relate_path.replace(pypaths.custom_db_path, 'db')
    return relate_path


def get_db_selected_path(dir_list: list, select: str) -> str:
    """获取选择的数据库文件, 判断是在仓库目录中还是用户目录中"""
    for p in get_db_path_list(dir_list):
        p_select = os.path.join(p, select)
        if os.path.exists(p_select):
            return p_select
    return ''


def get_db_path_list(dir_list: list) -> List[str, str]:
    """通过hisotry取得仓库数据库和用户目录下的数据库"""
    return [os.path.join(pypaths.db_path, *dir_list),
            os.path.join(pypaths.custom_db_path, *dir_list)]


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


def _print(style: str):
    """装饰器 通用打印方法"""
    def wrapper(func):
        def inner(message: str):
            if style == 'error':
                code = '[red]![/red]'
            elif style == 'info':
                code = '[dim]*[/dim]'
            elif style == 'success':
                code = '[green]✓[/green]'

            console.print("[dim][[/dim]{code}[dim]][/dim] {message}".format(
                code=code, message=message))
        return inner
    return wrapper


@_print('success')
def print_success(message: str):
    """打印成功信息"""


@_print('info')
def print_info(message: str):
    """打印信息"""


@_print('error')
def print_error(message: str):
    """打印错误"""


@contextmanager
def section(title: str) -> Iterator[list]:
    column_list = []
    yield column_list
    if column_list:
        columns = '\n'.join(column_list)
        console.print(Panel.fit(columns, title=title,
                                border_style='dim', title_align='center'))


def check_db():
    """检查数据库是否存在"""
    from rich.prompt import Confirm

    if not os.path.exists(pypaths.db_path):
        if Confirm.ask(f'cmder database not found, do you want to download?', default=True):
            update_database()


def update_database():
    import shutil
    import tempfile

    with console.status("[magenta]Updating database...", spinner='earth') as status:
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                subprocess.run(shlex.split(
                    f"git clone {database_url} --depth 1"), cwd=temp_dir, capture_output=True, check=True, timeout=10)
            except subprocess.TimeoutExpired:
                print_error("Download Timeout")
                raise typer.Exit()
            except subprocess.CalledProcessError:
                print_error("Download failed")
                raise typer.Exit()

            database_name = get_repository_name(database_url)
            if not os.path.exists(os.path.join(temp_dir, database_name, 'db')) and \
                    not os.path.exists(os.path.join(temp_dir, database_name, 'scripts')):
                print_error("Download failed with no Database Directory")
                raise typer.Exit()

            try:
                # 复制db文件夹
                if os.path.exists(pypaths.db_path):
                    shutil.rmtree(pypaths.db_path)
                shutil.copytree(os.path.join(
                    temp_dir, database_name, 'db'), pypaths.db_path)

                # 复制scripts文件夹,并添加运行权限
                if os.path.exists(pypaths.scripts_path):
                    shutil.rmtree(pypaths.scripts_path)
                shutil.copytree(os.path.join(
                    temp_dir, database_name, 'scripts'), pypaths.scripts_path)

                if is_linux():
                    subprocess.run(f"chmod +x {pypaths.scripts_path}/*",
                                   shell=True, capture_output=True, check=True)

            except subprocess.CalledProcessError:
                print_error(
                    "Running failed with [dim]chmod +x[/] command at scripts directory")

            except:
                print_error("Failed to copy database")
                raise typer.Exit()

    print_success("Update database success")


def get_repository_name(repository_url: str) -> str:
    """获取数据库名称"""
    return repository_url.split('/')[-1].replace('.git', '')
