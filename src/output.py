# -*- coding: UTF-8 -*-
from src import conf

from colorama import Fore, Style
from src.command import Command, SplitLine


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
          " "*pad_index + desc + Style.RESET_ALL + cmd.cmd[0])

    for cmd in cmd.cmd[1:]:
        print(" "*pad + cmd)

    print()


def print_cmds(cmdlist):
    idx = 1
    for cmd in cmdlist:
        if type(cmd) == Command:
            print_cmd(idx, cmd)
            idx += 1
        elif type(cmd) == SplitLine:
            print(cmd.to_s(Fore.BLUE + Style.BRIGHT))
            print()


def print_info(cmd):
    print("PATH: " + conf.latest_select)
    for note in cmd.notes:
        print(f'# {note}')

    print()

    print(Fore.BLUE + Style.BRIGHT + cmd.desc + Style.RESET_ALL)

    for c in cmd.cmd:
        print(Style.BRIGHT + c + Style.RESET_ALL)

    if cmd.vars:
        print()
        print(Fore.BLUE + Style.BRIGHT + 'Variable List:' +
              Style.RESET_ALL)
        for v in cmd.vars.list:
            desc = cmd.vars.list[v].desc
            if desc:
                print("  %s: %s" % (v, desc))
            else:
                print(f"  {v}")

    print()
    for r in cmd.refer:
        print(f'refer: {r}')
