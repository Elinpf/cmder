from cmder.menu import menu_select_file, menu_select_cmd_var
import argparse
import cmder
from cmder.parse import Parse
from cmder.output import print_cmds
from cmder.variable import VariableList


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
    parser_use.set_defaults(func=use)

    parser_workspace = subparsers.add_parser(
        'workspace', help='workspace config')
    parser_workspace.add_argument(
        '-n', '--new', metavar='name', help='add a new workspace')
    parser_workspace.add_argument(
        '-d', '--delete', metavar='name', help='delete a workspace')
    parser_workspace.add_argument(
        '-s', '--set', help='set a Variable eg: RHOST=192.168.0.1')
    parser_workspace.add_argument('-g', '--get', help='get all config')
    parser_workspace.add_argument(
        '-c', '--change', metavar='name', help='change to new')
    parser_workspace.set_defaults(func=workspace)

    return parser.parse_args()


def menu(args):
    """默认情况下呼出菜单, 并存储选择的文件"""
    try:
        select_file_path = menu_select_file(cmder.db_path)
    except TypeError:
        exit()
    except Exception as e:
        print(f"[-] {repr(e)}")
        exit()
    cmder.conf.latest_select = select_file_path
    parse = parse_files(select_file_path)
    print_cmds(parse.cmdlist)


def search(args):
    """查找工具命令"""
    print(f'this is search: {args.tool_name}')


def show(args):
    """浏览最近一次的命令列表"""
    if not cmder.conf.latest_select:
        return

    parse = parse_files(cmder.conf.latest_select)
    print_cmds(parse.cmdlist)


def use(args):
    """使用命令, 并存储到历史记录中"""
    parse = parse_files(cmder.conf.latest_select)

    try:
        cmd = parse.cmdlist[args.index - 1]
    except:
        print("[-] Error input of index")
        exit()

    merge_varlist(cmd, parse)

    menu_select_cmd_var(cmd)
    if args.one_line:
        shell = cmd.to_shell(one_line=True)
    else:
        shell = cmd.to_shell()

    print()
    print(shell)


def info(args):
    print(f'this is info: {args.index}')


def workspace(args):
    if args.new:
        cmder.conf.add_workspace(args.new)

    elif args.delete:
        cmder.conf.del_workspace(args.delete)

    elif args.set:
        key, val = args.set.split('=', 2)
        cmder.conf.workspace_set_var(key, val)

    elif args.get:
        if args.get == 'all':
            for key in cmder.conf.workspace_get_var_keys():
                val = cmder.conf.workspace_get_var(key)
                print(f"{key}={val}")
            return

        val = cmder.conf.workspace_get_var(args.get)
        print(f"{args.get}={val}")

    elif args.change:
        cmder.conf.workspace_change(args.change)

    else:
        now = cmder.conf.workspace_now()
        for name in cmder.conf.workspaces_name():
            if name == now:
                print(f" * {name}")
            else:
                print(f"   {name}")


def parse_files(select_file_path):
    """解析选择的文件"""
    file_list = cmder.unit.db_recursion_file(select_file_path)
    parse = Parse()
    parse.parse_files(file_list)
    return parse


def merge_varlist(cmd, parse):
    """合并包括config文件中variables"""
    config_varlist = VariableList()
    custom_varlist = VariableList()

    for key, val in cmder.conf.workspace_var_key_with_val():
        config_varlist.append(key)
        _ = {"name": key, "func": "recommend", "value": val}
        config_varlist.set(_)

    for key, val in cmder.conf.workspace_custom_key_with_val():
        custom_varlist.append(key)
        _ = {"name": key, "func": "recommend", "value": val}
        custom_varlist.set(_)

    cmd.merge_var(parse.g_varlist)
    cmd.merge_var(config_varlist)
    cmd.merge_var(custom_varlist)
