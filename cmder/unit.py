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


def db_recursion_init_file(file_path):
    """用于对指定的文件递归查询所有存在的__init__.xd文件
    返回List """

    relate_path = file_path.replace(get_root_path(), '')

    if is_windows():
        path_split_list = relate_path.split('\\')
    else:
        path_split_list = relate_path.split('/')

    p = get_root_path()
    list = []
    for i in path_split_list:
        p = os.path.join(p, i)
        init_path = os.path.join(p, '__init__.xd')

        if not os.path.exists(init_path):
            continue

        list.append(init_path)

    return list


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
