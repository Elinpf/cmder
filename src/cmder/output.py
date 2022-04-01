# -*- coding: UTF-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from rich import print
from rich.text import Text

from .command import Command, SplitLine
from .console import cmd_highlighter, console, bright_blue, dim, bright_yellow
from .data import pyoptions
from .unit import decode_multi_line_notes, section

if TYPE_CHECKING:
    from .command import CommandList


def _display_cmd(index: int, cmd: Command) -> str:
    nitems = []
    pad = 5
    index = "[{}]".format(index)
    pad_index = pad - len(index)
    if pad_index < 0:
        pad_index = 0

    desc = cmd.desc + " " if cmd.desc else ''

    nitems.append(bright_blue(index+" "*pad_index+desc) + cmd.cmd[0])
    for cmd in cmd.cmd[1:]:
        nitems.append(" "*pad + cmd)

    return "\n".join(nitems)


def display_cmds(cmdlist: CommandList) -> None:
    """显示命令列表"""
    idx = 1
    for cmd in cmdlist:
        if type(cmd) == Command:
            cmd = Text.from_markup(_display_cmd(idx, cmd) + "\n")
            console.print(cmd_highlighter(cmd))
            idx += 1
        elif type(cmd) == SplitLine:
            print(str(cmd) + "\n")


def _get_cmd_notes(cmd: Command) -> list:
    """取命令中的注释"""
    notes = []
    for note in cmd.notes:
        if pyoptions.encode_flag in note:
            notes.extend(decode_multi_line_notes(note).splitlines())
        else:
            notes.append(note)

    return notes


def display_cmd_info(cmd: Command) -> None:
    """显示命令的详细信息"""
    with section('description') as columns:
        for note in _get_cmd_notes(cmd):
            columns.append(dim(note))

    with section('path') as columns:
        columns.append(cmd.path)

    print(bright_blue(cmd.desc))
    for c in cmd.cmd:
        c = bright_yellow(c)
        console.print(cmd_highlighter(Text.from_markup(c)))

    with section('variables') as columns:
        for v in cmd.vars.list:
            desc = cmd.vars.list[v].desc
            columns.append(f"{v}: {desc}" if desc else f"{v}")

    with section('references') as columns:
        for ref in cmd.refer:
            columns.append(ref)

    with section('link to db') as columns:
        for link in cmd.links:
            columns.append(link)
