import os
import pickle

from src.menu import menu_select_file, menu_select_cmd_var, menu
import argparse
import src
from src.parse import Parse
from src.output import print_cmds, print_info
from src.variable import VariableList
from src.data import pypaths, pyoptions
from src.decorator import load
from src import cool


def get_options():
    parser = argparse.ArgumentParser(
        description='Generate a pentesting command')
    parser.add_argument(
        '-l', '--link', metavar='path', help='show the link file')
    parser.set_defaults(func=default_menu)

    subparsers = parser.add_subparsers(help='sub-command help')
    parser_show = subparsers.add_parser(
        'show', help='show the latest table')
    parser_show.add_argument(
        '-s', '--history', action='store_true', help='show the history')
    parser_show.set_defaults(func=show)

    parser_search = subparsers.add_parser(
        'search', help='Search tools in the database')
    parser_search.add_argument(
        'tool_name', type=str, metavar='string', help='tool name')
    parser_search.set_defaults(func=search)

    parser_history = subparsers.add_parser(
        'history', help='Get history')
    parser_history.add_argument(
        '-u', '--use', metavar='index', type=int, help='use the history cmd')
    parser_history.add_argument(
        '--size', metavar='NUM', type=int, help='set history size')
    parser_history.set_defaults(func=history)

    parser_info = subparsers.add_parser(
        'info', help='show command information')
    parser_info.add_argument(
        'index', type=int, help='index of the lastest list')
    parser_info.set_defaults(func=info)

    parser_use = subparsers.add_parser('use', help='use command')
    parser_use.add_argument(
        'index', type=int, help='index of the lastest list')
    parser_use.add_argument(
        '-i', '--info', action='store_true', help='show the cmd information')
    parser_use.add_argument(
        '--one-line', action='store_true', help='output shell in one line')
    parser_use.add_argument(
        '-l', '--link', action='store_true', help='select the command link path')
    parser_use.add_argument(
        '-r', '--run', action='store_true', help="running the select command."
    )
    parser_use.add_argument(
        '-d', '--daemon', action='store_true', help='daemon running')
    parser_use.add_argument(
        '-o', '--output', type=str, help="output the command to a file"
    )
    parser_use.set_defaults(func=use)

    parser_workspace = subparsers.add_parser(
        'workspace', help='workspace config')
    parser_workspace.add_argument(
        '-n', '--new', metavar='name', help='add a new workspace')
    parser_workspace.add_argument(
        '-d', '--delete', metavar='name', help='delete a workspace')
    parser_workspace.add_argument(
        '-s', '--set', metavar='key=val', help='set a variable eg: RHOST=192.168.0.1')
    parser_workspace.add_argument(
        '-u', '--unset', metavar='key', help='unset variable')
    parser_workspace.add_argument(
        '-g', '--get', action='store_true', help='get all config')
    parser_workspace.add_argument(
        '-c', '--change', metavar='name', help='change to new')
    parser_workspace.set_defaults(func=workspace)

    return parser.parse_args()


def default_menu(args):
    """默认情况下呼出菜单, 并存储选择的文件"""
    try:
        if args.link:
            fp = os.path.join(pypaths.root_path, args.link)
            fcp = os.path.join(pypaths.custom_path, args.link)
            if os.path.exists(fp):
                file = fp
            elif os.path.exists(fcp):
                file = fcp
            else:
                raise ValueError("Can't find file")

        else:
            file = menu_select_file(pypaths.db_path)
    except TypeError:
        exit()
    except Exception as e:
        print(f"[-] {repr(e)}")
        exit()
    src.conf.latest_select = file
    pyoptions.cmd_list = parse_files(file).cmdlist
    print_cmds(pyoptions.cmd_list)
    f = open(pypaths.sequence_path, 'wb')
    pickle.dump(pyoptions.cmd_list, f)


def search(args):
    """查找工具命令"""
    print(f'this is search: {args.tool_name}')


def history(args):
    """历史命令"""
    if args.size:
        src.conf.history_size = args.size
        exit()

    if args.use:
        if args.use < 1:
            return

        import linecache
        line = linecache.getline(pypaths.history_path, args.use)
        print(line)

        os.system(line)
        exit()

    with open(pypaths.history_path, 'r', encoding='UTF-8') as f:
        index = 1
        for line in f.readlines():
            print(format(" %-3s %s" % (index, line.rstrip())))
            index += 1


@load
def show(args):
    if args.history:
        hs = src.conf.history_select
        hs = [x.replace(pypaths.db_path, 'db') for x in hs]
        hs = [x.replace(pypaths.custom_db_path, 'db')
              for x in hs]
        idx = menu('History Select:', hs)
        file = src.conf.history_select[idx]
        src.conf.latest_select = file
        pyoptions.cmd_list = parse_files(file).cmdlist
        f = open(pypaths.sequence_path, 'wb')
        pickle.dump(pyoptions.cmd_list, f)

    print_cmds(pyoptions.cmd_list)


@load
def use(args):
    """使用命令, 并存储到历史记录中"""

    cmd = pyoptions.cmd_list[args.index - 1]
    merge_varlist(cmd)

    if args.link:
        select_link(cmd)
        return

    if args.info:
        print_info(cmd)
        return

    menu_select_cmd_var(cmd)

    shell = cmd.to_shell(one_line=args.one_line)

    if args.daemon:
        shell = format("%s &" % shell)

    print()
    print(cool.white_bright(shell))

    if args.output:
        with open(args.output, 'w') as fi:
            fi.write(shell)

        print()
        print(f"file output to {args.output}")

    # 写入history 并当超过长度长度时删除首行
    with open(pypaths.history_path, "r+") as f:
        d = f.readlines()
        if src.conf.history_size <= len(d):
            f.seek(0)
            for i in d[1:src.conf.history_size]:
                f.write(i)
            f.write(shell + "\n")
            f.truncate()
        else:
            f.write(shell + "\n")

    if args.run:
        shell = src.unit.escap_chars(shell)
        os.system(shell)


@load
def info(args):
    cmd = pyoptions.cmd_list[args.index - 1]

    merge_varlist(cmd)
    print_info(cmd)


def workspace(args):
    if args.new:
        src.conf.add_workspace(args.new)

    elif args.delete:
        src.conf.del_workspace(args.delete)

    elif args.unset:
        src.conf.workspace_unset_var(args.unset)

    elif args.set:
        key, val = args.set.split('=', 1)
        src.conf.workspace_set_var(key, val)

    elif args.get:
        for key in src.conf.workspace_get_var_keys():
            val = src.conf.workspace_get_var(key)
            for v in val:
                print(f"{key}={v}")

    elif args.change:
        src.conf.workspace_change(args.change)

    else:
        now = src.conf.workspace_now()
        for name in src.conf.workspaces_name():
            if name == now:
                print(f" * {name}")
            else:
                print(f"   {name}")


def parse_files(select_file_path):
    """解析选择的文件"""
    file_list = src.unit.db_recursion_file(select_file_path)
    parse = Parse()
    parse.parse_files(file_list)
    return parse


def merge_varlist(cmd):
    """合并包括config文件中variables"""
    config_varlist = VariableList()
    custom_varlist = VariableList()

    for key, val in src.conf.workspace_var_key_with_val():
        config_varlist.append(key)
        _ = {"name": key, "func": "recommend", "value": val}
        config_varlist.set(_)

    for key, val in src.conf.workspace_custom_key_with_val():
        custom_varlist.append(key)
        _ = {"name": key, "func": "recommend", "value": val}
        custom_varlist.set(_)

    cmd.merge_var(config_varlist)
    cmd.merge_var(custom_varlist)


def select_link(cmd):
    idx = menu('select link to:', cmd.links)
    file = cmd.links[idx]
    parse = parse_files(file)
    src.conf.latest_select = file
    print_cmds(parse.cmdlist)
