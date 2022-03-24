from __future__ import annotations

import re
from typing import List

from .command import Command, CommandList, SplitLine
from .unit import encode_multi_line_notes
from .variable import Variable, VariableList


class Parse():
    """分割文本区域，分析命令"""

    def __init__(self):
        self.file_path = None
        self.g_varlist = VariableList()
        self.cmdlist = CommandList()
        self.notes = []
        self.refers = []

    def parse_file(self, file_path: str) -> None:
        """设置解析的文件"""
        self.file_path = file_path
        self._split_area(file_path)

    def parse_files(self, files: list) -> None:
        for f in files:
            self.parse_file(f)

        for cmd in self.cmdlist:
            cmd.merge_var(self.g_varlist)
            cmd.merge_notes(self.notes)
            cmd.path = files[-1]

    def _split_area(self, file_path: str) -> None:
        """已空行为界线进行分割区域"""
        new_area = []  # type: List[str]
        file_string = open(
            file_path, 'r', encoding='UTF-8').read()  # type: str

        file_string = encode_multi_line_notes(file_string)
        for line in file_string.splitlines():
            line = line.rstrip()
            if line == '':
                if len(new_area):
                    self._parse_area(new_area)
                    new_area = []
                continue

            new_area.append(line)

        if len(new_area):
            self._parse_area(new_area)

    def _parse_area(self, area: list) -> None:
        """分析区域"""
        cmd = None
        for line in area:  # first loop to find cmd
            if line.strip()[0] != '#' and line.strip()[0] != '@':
                if cmd:
                    cmd.add_cmd(line)
                else:
                    sl = re.match(r'---(.*)', line)
                    if sl:     # is split line
                        self.cmdlist.append(SplitLine(sl[1].strip()))
                    else:
                        cmd = Command(line)

        if cmd:
            self.cmdlist.append(self._parse_cmd_area(cmd, area))

        else:
            self._parse_normal_area(area)

    def _parse_cmd_area(self, cmd: Command, area: list) -> Command:
        """命令区域的解析"""
        cmd.parse()
        for line in area:
            line = line.strip()
            if line[0] == '#':
                cmd.add_note(line[1:].strip())

            elif line[0] == '@':
                res = re.match(r"^@(.*?)\.(.*?)\((.*)\)", line)
                try:
                    var = cmd.vars[res[1]]  # type: Variable
                except (KeyError, TypeError):
                    print(
                        format("[-] (%s) file various write error: #{%s}" % (self.file_path, line)))
                    exit()
                info = {"func": res[2], "value": res[3]}
                var.set(info)

        return cmd

    def _parse_normal_area(self, area: list) -> None:
        """对普通区域进行解析"""
        for line in area:
            line = line.strip()

            if line[0] == '@':
                res = re.match(r"^@(.*?)\.(.*?)\((.*)\)", line)
                try:

                    info = {"name": res[1], "func": res[2], "value": res[3]}
                except:
                    print(
                        format("[-] %s file grammatical errors: \n %s" % (self.file_path, line)))
                    exit()

                self.g_varlist.set(info)

            if line[0] == '#':
                self.notes.append(line[1:].strip())
