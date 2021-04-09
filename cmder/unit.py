import os
import sys
import platform
import cmder


def get_root_path():
    return os.path.split(os.path.abspath(sys.argv[0]))[0]


def get_db_path():
    return os.path.join(get_root_path(), 'db')


def is_windows():
    return platform.system() == 'Windows'


def db_recursion_file(file_path):
    """用于对指定的文件递归查询所有存在的__init__.xd文件,
    以及用户目录下自定义的文件
    返回List """

    relate_path = get_relate_path(file_path)

    if is_windows():
        path_split_list = relate_path.split('\\')
    else:
        path_split_list = relate_path.split('/')

    p = cmder.root_path
    c = cmder.custom_file_path  # 用户文件夹
    list = []
    for i in path_split_list:
        p = os.path.join(p, i)
        c = os.path.join(c, i)

        for init_path in [os.path.join(p, '__init__.xd'), os.path.join(c, '__init__.xd')]:
            if not os.path.exists(init_path):
                continue

            list.append(init_path)

    # 判断是否文件是否存在, 并在list 中返回
    for file in get_path_list(file_path):
        if os.path.exists(file):
            list.append(file)

    return list


def get_select_path(path, select):
    """获取选择的文件，如果在软件目录中不存在，就返回用户目录的路径"""
    for p in get_path_list(path):
        p_select = os.path.join(p, select)
        if os.path.exists(p_select):
            return p_select


def get_relate_path(path):
    """获取相对路径"""
    relate_path = path.replace(cmder.root_path, '')
    relate_path = relate_path.replace(cmder.custom_file_path, '')
    return relate_path[1:]


def get_path_list(path):
    """取软件目录与用户目录的list"""
    relate_path = get_relate_path(path)
    root_path = os.path.join(cmder.root_path, relate_path)
    custom_path = os.path.join(cmder.custom_file_path, relate_path)
    return [root_path, custom_path]


def store_file(file_relate_path, string):
    """用于存储文件, 
    file_relate_path 是相对与用户目录下的文件路径"""
    fi = open_custom_file(file_relate_path, 'w')
    fi.write(string)
    fi.close()


def open_custom_file(file_relate_path, mode):
    """打开用户目录中的文件"""
    file_path = custom_abspath(file_relate_path)
    fi = open(file_path, mode)
    return fi


def custom_abspath(file_relate_path):
    """返回用户目录绝对路径"""
    return os.path.join(cmder.custom_file_path, file_relate_path)
