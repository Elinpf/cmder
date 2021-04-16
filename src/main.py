import os

from colorama import Style
from src.menu import menu_select_file, menu_select_cmd_var
import argparse
import src
from src.parse import Parse
from src.output import print_cmds, print_info
from src.variable import VariableList


def get_options():
    parser = argparse.ArgumentParser(
        description='Generate a pentesting command')
    parser.set_defaults(func=menu)

    subparsers = parser.add_subparsers(help='sub-command help')
    parser_show = subparsers.add_parser(
        'show', help='show the latest table')
    parser_show.set_defaults(func=show)

    parser_search = subparsers.add_parser(
        'search', help='Search tools in the database')
    parser_search.add_argument(
        'tool_name', type=str, metavar='string', help='tool name')
    parser_search.set_defaults(func=search)

    parser_history = subparsers.add_parser(
        'history', help='Get history')
    parser_history.add_argument(
        '-u', '--use', metavar='NUM', type=int, help='use the history cmd')
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
        '-l', '--one_line', action='store_true', help='output shell in one line')
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


def menu(args):
    """默认情况下呼出菜单, 并存储选择的文件"""
    try:
        select_file_path = menu_select_file(src.db_path)
    except TypeError:
        exit()
    except Exception as e:
        print(f"[-] {repr(e)}")
        exit()
    src.conf.latest_select = select_file_path
    parse = parse_files(select_file_path)
    print_cmds(parse.cmdlist)


def search(args):
    """查找工具命令"""
    print(f'this is search: {args.tool_name}')


def history(args):
    """历史命令"""
    if args.size:
        src.conf.history_size = args.size
        exit()

    history_file = os.path.join(src.custom_file_path, 'history')

    if args.use:
        if args.use < 1:
            return

        import linecache
        line = linecache.getline(history_file, args.use)
        print(line)

        os.system(line)
        exit()

    with open(history_file, 'r', encoding='UTF-8') as f:
        index = 1
        for line in f.readlines():
            print(format(" %-3s %s" % (index, line.rstrip())))
            index += 1


def show(args):
    """浏览最近一次的命令列表"""
    if not src.conf.latest_select:
        return

    parse = parse_files(src.conf.latest_select)
    print_cmds(parse.cmdlist)


def use(args):
    """使用命令, 并存储到历史记录中"""
    parse = parse_files(src.conf.latest_select)

    try:
        cmd = parse.cmdlist[args.index - 1]
    except:
        print("[-] Error input of index")
        exit()

    merge_varlist(cmd, parse)

    menu_select_cmd_var(cmd)

    shell = cmd.to_shell(one_line=args.one_line)

    if args.daemon:
        shell = format("%s &" % shell)

    print()
    print(Style.BRIGHT + shell + Style.RESET_ALL)

    if args.output:
        with open(args.output, 'w') as fi:
            fi.write(shell)

        print()
        print(f"file output to {args.output}")

    # 写入history 并当超过长度长度时删除首行
    history_file = os.path.join(src.custom_file_path, 'history')
    with open(history_file, "a+") as f:
        f.seek(0)
        d = f.readlines()
        if src.conf.history_size < len(d):
            f.seek(0)
            for i in d[1:]:
                f.write(i)
            f.write(shell + "\n")
            f.truncate()
        else:
            f.write(shell + "\n")

    if args.run:
        shell = src.unit.escap_chars(shell)
        os.system(shell)


def info(args):
    """使用命令, 并存储到历史记录中"""
    parse = parse_files(src.conf.latest_select)

    try:
        cmd = parse.cmdlist[args.index - 1]
    except:
        print("[-] Error input of index")
        exit()

    merge_varlist(cmd, parse)
    cmd.merge_notes(parse.notes)
    cmd.merge_refers(parse.refers)
    print_info(cmd)


def workspace(args):
    if args.new:
        src.conf.add_workspace(args.new)

    elif args.delete:
        src.conf.del_workspace(args.delete)

    elif args.unset:
        src.conf.workspace_unset_var(args.unset)

    elif args.set:
        key, val = args.set.split('=', 2)
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


def merge_varlist(cmd, parse):
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

    cmd.merge_var(parse.g_varlist)
    cmd.merge_var(config_varlist)
    cmd.merge_var(custom_varlist)
