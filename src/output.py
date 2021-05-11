# -*- coding: UTF-8 -*-
from src import conf, cool
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

    print(cool.blue_bright(index+" "*pad_index+desc) + cmd.cmd[0])

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
            print(cmd.to_s())
            print()


def print_info(cmd):
    print("PATH: " + cmd.path)
    for note in cmd.notes:
        print(f'# {note}')

    print()

    print(cool.blue_bright(cmd.desc))

    for c in cmd.cmd:
        print(cool.yellow_bright(c))

    if cmd.vars:
        print()
        print(cool.blue_bright('Variable List:'))
        for v in cmd.vars.list:
            desc = cmd.vars.list[v].desc
            if desc:
                print("  %s: %s" % (v, desc))
            else:
                print(f"  {v}")

    if cmd.refer:
        print()
        print(cool.blue_bright('Reference List:'))

        for r in cmd.refer:
            print(r)

    if cmd.links:
        print()
        print(cool.blue_bright('Link List:'))

        for l in cmd.links:
            print(l)
