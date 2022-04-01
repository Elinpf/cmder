from __future__ import annotations

import re
from typing import TYPE_CHECKING, List

import wcwidth

from .data import pyoptions
from .unit import get_relate_path
from .variable import VariableList
from .console import bright_magenta

if TYPE_CHECKING:
    from .variable import Variable


class Command():
    def __init__(self, line: str):
        self.cmd = [line]
        self.refer = []
        self.notes = []
        self.links = []
        self.desc = ""
        self.vars = VariableList()
        self._path = ""

    def __repr__(self) -> str:
        return "<cmd:" + self.cmd[0] + ">"

    def to_shell(self, one_line: bool = False) -> str:
        if one_line:
            str = " && ".join(self.cmd)
        else:
            str = "\n".join(self.cmd)

        for key, val in self.vars.key_with_var():
            str = str.replace("#{"+key+"}", val.select)

        return str

    def add_note(self, line: str, reverse: int = 0) -> None:

        if re.match(pyoptions.note_desc_pattern, line):
            self.desc = line.split(pyoptions.note_separator, 1)[1].strip()

        elif re.match(pyoptions.note_refer_pattern, line):
            self.add_refer(line.split(pyoptions.note_separator, 1)[1].strip())

        elif re.match(pyoptions.note_link_pattern, line):
            self.add_link(line.split(pyoptions.note_separator, 1)[1].strip())

        else:
            if reverse:  # 当是全局note的时候，放在前面
                self.notes.insert(len(self.notes)-reverse, line)
            else:
                self.notes.append(line)

    def add_refer(self, line: str) -> None:
        self.refer.append(line)

    def add_cmd(self, line: str) -> None:
        self.cmd.append(line)

    def add_link(self, line: str) -> None:
        self.links.append(line)

    def merge_var(self, g_varlist: VariableList) -> List["Variable"]:
        return self.vars.merge(g_varlist)

    def merge_notes(self, notes: list) -> List[str]:
        # 合并的notes放在前面
        ln = len(notes)
        for note in notes:
            self.add_note(note, reverse=ln)

        return self.notes

    def parse(self) -> None:
        """在添加完了命令后使用, 分析里面的变量"""
        var_list = []
        for c in self.cmd:
            var_list += (re.findall(pyoptions.variable_pattern, c))

        for v in var_list:
            self.vars.append(v)

    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, file: str) -> None:
        self._path = get_relate_path(file)


class CommandList():
    # TODO 这里将SplitLine 和 Command 混在一起了，后面分开
    def __init__(self):
        self.list = []

    def append(self, cmd: Command | SplitLine | List[Command | SplitLine]):
        if isinstance(cmd, list):
            self.list.extend(cmd)
        else:
            self.list.append(cmd)

    def __len__(self) -> int:
        return len(self.get_cmd_list())

    def __iter__(self) -> Command | SplitLine:
        return self.list.__iter__()

    def __next__(self) -> Command:
        return next(self.list)

    def __getitem__(self, index: int) -> Command:
        try:
            return self.get_cmd_list()[index]
        except:
            print("[-] Error input of index")
            exit()

    def get_cmd_list(self) -> List[Command]:
        """只包含command类"""
        cmds = []
        for c in self.list:
            if type(c) == Command:
                cmds.append(c)

        return cmds

    def filter(self, string: str) -> List[Command]:
        """筛选cmd"""
        cmds = []
        for cmd in self.get_cmd_list():
            if string in cmd.to_shell():
                cmds.append(cmd)

        return cmds


class SplitLine():
    """分割行"""

    def __init__(self, desc: str):
        self.desc = desc

    def __str__(self) -> str:
        total_len = 60
        lc = total_len - wcwidth.wcswidth(self.desc) - 2
        llc = int(lc / 2)
        rlc = llc
        if lc % 2 == 1:
            rlc += 1

        _ = (pyoptions.splitline_char*llc + ' ' +
             bright_magenta(self.desc) + ' ' + pyoptions.splitline_char*rlc)

        return _

    def merge_var(self, key): ...
    def merge_notes(self, key): ...
