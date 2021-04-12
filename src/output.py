# -*- coding: UTF-8 -*-
from src.unit import is_windows

if not is_windows():
    from colorama import Fore, Style


def print_cmd(index, cmd):
    pad = 5
    index = "[{}]".format(index)
    pad_index = pad - len(index)
    if pad_index < 0:
        pad_index = 0

    desc = ''

    if cmd.desc:
        desc = cmd.desc + " "

    if is_windows():
        print(index + " "*pad_index + desc + cmd.cmd[0])

    else:
        print(Fore.BLUE + Style.BRIGHT + index +
              " "*pad_index + desc + Fore.RESET + cmd.cmd[0])

    for cmd in cmd.cmd[1:]:
        print(" "*pad + cmd)

    print()


def print_cmds(cmdlist):
    idx = 1
    for cmd in cmdlist:
        print_cmd(idx, cmd)
        idx += 1
