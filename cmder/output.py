# -*- coding: UTF-8 -*-
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
