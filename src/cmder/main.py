import os
import pickle
import re
import shlex
import subprocess
from typing import TYPE_CHECKING, Optional, Tuple

import rich
import rich_typer as typer

from . import __version__, conf
from .command import CommandList
from .data import banner, pyoptions, pypaths, repository_url
from .decorator import load
from .menu import menu, menu_select_cmd_var, menu_select_file
from .output import display_cmd_info, display_cmds
from .parse import Parse
from .unit import (db_recursion_file, get_relate_path, print_error, print_info,
                   print_success)
from .variable import VariableList
from .console import console

if TYPE_CHECKING:
    from .command import Command

app = typer.RichTyper(add_completion=False)


def dis_banner(display: bool):
    if display:
        rich.print(banner.format(version=__version__, url=repository_url))
        raise typer.Exit()


def update_db(update: bool) -> None:
    """更新数据库"""
    import shutil
    import tempfile
    if update:
        with console.status("[magenta]Updating database...", spinner='earth') as status:
            with tempfile.TemporaryDirectory() as temp_dir:
                try:
                    subprocess.run(shlex.split(
                        f"git clone {repository_url} --depth 1"), cwd=temp_dir, capture_output=True, check=True, timeout=10)
                except subprocess.TimeoutExpired:
                    print_error("Download Timeout")
                    raise typer.Exit()
                except subprocess.CalledProcessError:
                    print_error("Download failed")
                    raise typer.Exit()

                if not os.path.exists(os.path.join(temp_dir, 'cmder', 'db')):
                    print_error("Download failed with no Database Directory")
                    raise typer.Exit()

                shutil.rmtree(pypaths.db_path)
                shutil.copytree(os.path.join(
                    temp_dir, 'cmder', 'db'), pypaths.db_path)

        print_success("Update database success")
        raise typer.Exit()


@app.callback(invoke_without_command=True, epilog=repository_url)
def main(
    ctx: typer.Context,
    link: str = typer.Option(None, "--link", "-l",
                             help="Display the link file"),
    banner: bool = typer.Option(
        False, "--banner", help="Show banner", is_eager=True, callback=dis_banner),
    update: bool = typer.Option(
        False, "--update", help="Update Database 🎂", is_eager=True, callback=update_db)
):
    """Generate a pentesting command 👹"""
    file = ''
    if link:
        fp = os.path.join(pypaths.root_path, link)
        fcp = os.path.join(pypaths.custom_path, link)
        if os.path.exists(fp):
            file = fp
        elif os.path.exists(fcp):
            file = fcp
        else:
            print_error(f"file [u][bold red]{link}[/][/u] is not exsits")
            raise typer.Exit()

    if ctx.invoked_subcommand is None:
        file = file or menu_select_file(pypaths.db_path)
        conf.latest_select = file
        pyoptions.cmd_list = _parse_files(file).cmdlist
        display_cmds(pyoptions.cmd_list)
        _dump()


@app.command(epilog=repository_url)
@load
def show(
    ctx: typer.Context,
    history: bool = typer.Option(
        False, "--history", "-h", help="Show history"),
):
    """Show Commands"""
    if history:
        hs = conf.history_select
        hs = [x.replace(pypaths.db_path, 'db') for x in hs]
        hs = [x.replace(pypaths.custom_db_path, 'db')
              for x in hs]
        idx = menu('History Select:', hs)
        file = conf.history_select[idx]
        conf.latest_select = file
        pyoptions.cmd_list = _parse_files(file).cmdlist
        _dump()

    display_cmds(pyoptions.cmd_list)


@app.command(epilog=repository_url)
def search(
    ctx: typer.Context,
    string: str = typer.Argument(..., help="Search string"),
):
    """Search string"""
    file_list = []
    for root, _, files in os.walk(pypaths.db_path):
        for file in files:
            if os.path.splitext(file)[1] == pyoptions.db_file_suffix:
                file_path = os.path.join(root, file)
                file_obj = open(file_path, 'rU')
                for line in file_obj:
                    if string in line:
                        file_list.append(get_relate_path(file_path))
                        break

    for root, _, files in os.walk(pypaths.custom_db_path):
        for file in files:
            if os.path.splitext(file)[1] == pyoptions.db_file_suffix:
                file_path = os.path.join(root, file)
                relate_path = get_relate_path(file_path)
                if not relate_path in files:
                    file_obj = open(file_path, 'rU')
                    for line in file_obj:
                        if string in line:
                            file_list.append(relate_path)
                            break

    pyoptions.cmd_list = CommandList()
    for file in file_list:
        parse = _parse_files(file)
        pyoptions.cmd_list.append(parse.cmdlist.filter(string))

    display_cmds(pyoptions.cmd_list)
    _dump()


@app.command(epilog=repository_url)
def history(
    ctx: typer.Context,
    use: int = typer.Option(None, "--use", "-u",
                            help="Use history command"),
    size: int = typer.Option(None, "--size", "-s",
                             help="Set history size", min=0, max=2000, clamp=True),
):
    """Commands history"""

    if size:
        old_size = conf.history_size
        if size <= 0:
            conf.history_size = 0
            print_success(
                f"history size set from [dim]{old_size}[/dim] to [green]0[/green]")
        else:
            conf.history_size = size
            print_success(
                f"history size set from [dim]{old_size}[/dim] to [green]{conf.history_size}[/green]")
        raise typer.Exit()

    if use:
        import linecache
        line = linecache.getline(pypaths.history_path, use)
        print(line)

        os.system(line)
        raise typer.Exit()

    with open(pypaths.history_path, 'r', encoding='UTF-8') as f:
        index = 1
        for line in f.readlines():
            print(format(" %-3s %s" % (index, line.rstrip())))
            index += 1


@app.command(epilog=repository_url)
@load
def info(
    ctx: typer.Context,
    index: int = typer.Argument(..., help="Index of command", min=1),
):
    """Show info of command"""
    cmd = pyoptions.cmd_list[index - 1]

    _merge_varlist(cmd)
    display_cmd_info(cmd)


@app.command(epilog=repository_url)
@load
def use(
    ctx: typer.Context,
    index: int = typer.Argument(..., help="Index of command"),
    info: bool = typer.Option(False, "--info", "-i", help="Show info"),
    run: bool = typer.Option(False, "--run", "-r", help="Run command"),
    daemon: bool = typer.Option(False, "--daemon", "-d", help="Run as daemon"),
    link: bool = typer.Option(False, "--link", "-l",
                              help="Display the link cmd"),
    output: typer.FileText = typer.Option(None, "--output", "-o", mode='w',
                                          help="Output file"),
    one_line: bool = typer.Option(
        False, "--one-line", "-1", help="One line output"),
):
    """Use command"""
    cmd = pyoptions.cmd_list[index - 1]
    _merge_varlist(cmd)

    if link:
        _select_link(cmd)
        raise typer.Exit()

    if info:
        display_cmd_info(cmd)
        raise typer.Exit()

    menu_select_cmd_var(cmd)

    shell = cmd.to_shell(one_line=one_line)
    print(shell + "\n")

    # 写入history 并当超过长度长度时删除首行
    with open(pypaths.history_path, "r+") as f:
        d = f.readlines()
        if conf.history_size <= len(d):
            f.seek(0)
            for i in d[1:conf.history_size]:
                f.write(i)
            f.write(shell + "\n")
            f.truncate()
        else:
            f.write(shell + "\n")

    if run or daemon:
        if daemon:
            shell = format("nohup %s &" % shell)

        try:
            subprocess.run(shlex.split(shell),
                           stdout=output if output else None,
                           stderr=output if output else None)
        except FileNotFoundError as e:
            f = re.search(r"\'(.*?)\'", str(e)).group(1)
            print_error(
                f"failed to run command '[bright_red]{f}[/bright_red]': No such file or directory")
            raise typer.Exit()

        if output:
            output.write(shell + "\n")
            rich.print(
                "Command output has been written to [u]%s[/u]" % output.name)
            output.close()


@app.command(epilog=repository_url)
def workspace(
    ctx: typer.Context,
    add: str = typer.Option(None, "--add", "-a", help="Add a new workspace"),
    remove: str = typer.Option(None, "--remove",
                               help="Remove a workspace"),
    set: Tuple[str, str] = typer.Option(None, "--set", "-s",
                                        help='Set the value of current workspace variable'),
    unset: str = typer.Option(None, "--unset",
                              help="Unset a workspace variable"),
    get: Optional[str] = typer.Option(None, "--get", "-g",
                                      help="Get a workspace variable"),
    change: str = typer.Option(None, "--change", "-c",
                               help="Change the other workspace"),
):
    """Workspace"""
    if add:
        if add in conf.workspaces_name():
            print_info(f"Workspace [cyan]{add}[/cyan] already exists")
        else:
            conf.add_workspace(add)
            print_success(f"Add a new workspace [cyan]{add}[/cyan]")

        conf.workspace_change(add)
        print_info(f"Change to workspace: [cyan]{add}[/cyan]")

    elif remove:
        try:
            conf.del_workspace(remove)
            print_success(f"Remove the workspace: [cyan]{remove}[/cyan]")
        except ValueError as e:
            print_error(str(e))

    elif set:
        key, val = set
        conf.workspace_set_var(key, val)
        print_success(
            f"Set the value of current workspace variable [yellow]{key}[/yellow] to [green]{val}[/green]")

    elif unset:
        try:
            conf.workspace_unset_var(unset)
            print_success(
                f"Unset a workspace variable [yellow]{unset}[/yellow]")
        except KeyError:
            print_error(
                f"[yellow]{unset}[/yellow] variable does not exist in current workspace")

    elif get:
        if get == 'all':
            for key in conf.workspace_get_var_keys():
                val = conf.workspace_get_var(key)
                for v in val:
                    rich.print(f"[yellow]{key}[/yellow] = [green]{v}[/green]")
        else:
            val = conf.workspace_get_var(get)
            for v in val:
                rich.print(f"[yellow]{get}[/yellow] = [green]{v}[/green]")

    elif change:
        conf.workspace_change(change)
        print_success(f"Change to workspace: [cyan]{change}[/cyan]")

    else:
        now = conf.workspace_now()
        for name in conf.workspaces_name():
            if name == now:
                rich.print(f" [bold red]*[/bold red] {name}")
            else:
                rich.print(f"   {name}")


def _parse_files(select_file_path: str) -> Parse:
    """解析选择的文件"""
    file_list = db_recursion_file(select_file_path)
    parse = Parse()
    parse.parse_files(file_list)
    return parse


def _merge_varlist(cmd: "Command") -> None:
    """合并包括config文件中variables"""
    config_varlist = VariableList()
    custom_varlist = VariableList()

    for key, val in conf.workspace_var_key_with_val():
        config_varlist.append(key)
        _ = {"name": key, "func": "recommend", "value": val}
        config_varlist.set(_)

    for key, val in conf.workspace_custom_key_with_val():
        custom_varlist.append(key)
        _ = {"name": key, "func": "recommend", "value": val}
        custom_varlist.set(_)

    cmd.merge_var(config_varlist)
    cmd.merge_var(custom_varlist)


def _select_link(cmd: "Command") -> None:
    if not cmd.links:
        print_error("This command no link found")
        return
    idx = menu('select link to:', cmd.links)
    file = cmd.links[idx]
    parse = _parse_files(file)
    conf.latest_select = file
    display_cmds(parse.cmdlist)


def _dump() -> None:
    """将获取的命令列表序列化后保存"""
    f = open(pypaths.sequence_path, 'wb')
    pickle.dump(pyoptions.cmd_list, f)


if __name__ == '__main__':
    app(["--help"])
