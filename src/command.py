import re
import wcwidth
from src.variable import VariableList
from colorama import Style


class Command():
    def __init__(self, line):
        self.cmd = [line]
        self.refer = []
        self.notes = []
        self.links = []
        self.desc = ""
        self.vars = VariableList()

    def __repr__(self):
        return "<cmd:" + self.cmd[0] + ">"

    def to_shell(self, one_line=False):
        if one_line:
            str = ";".join(self.cmd)
        else:
            str = "\n".join(self.cmd)

        for key, val in self.vars.key_with_var():
            str = str.replace("#{"+key+"}", val.select)

        return str

    def add_note(self, line, reverse=0):

        if re.match(r"^\s*desc\s*:", line):
            self.desc = line.split(':', 1)[1].strip()

        elif re.match(r"^\s*refer\s*:", line):
            self.add_refer(line.split(':', 1)[1].strip())

        elif re.match(r"^\s*link\s*:", line):
            self.add_link(line.split(':', 1)[1].strip())

        else:
            if reverse:  # 当是全局note的时候，放在前面
                self.notes.insert(len(self.notes)-reverse, line)
            else:
                self.notes.append(line)

    def add_refer(self, line):
        self.refer.append(line)

    def add_cmd(self, line):
        self.cmd.append(line)

    def add_link(self, line):
        self.links.append(line)

    def merge_var(self, g_varlist):
        return self.vars.merge(g_varlist)

    def merge_notes(self, notes):
        # 合并的notes放在前面
        ln = len(notes)
        for note in notes:
            self.add_note(note, reverse=ln)

        return self.notes

    def parse(self):
        """在添加完了命令后使用, 分析里面的变量"""
        var_list = []
        for c in self.cmd:
            var_list += (re.findall(r"#{(.*?)}", c))

        for v in var_list:
            self.vars.append(v)


class CommandList():
    def __init__(self):
        self.list = []

    def append(self, cmd: Command):
        self.list.append(cmd)

    def __iter__(self):
        return self.list.__iter__()

    def __next__(self):
        return next(self.list)

    def __getitem__(self, index: int):
        return self.get_cmd_list()[index]
        # return self.list[index]

    def get_cmd_list(self):
        """只包含command类"""
        cmds = []
        for c in self.list:
            if type(c) == Command:
                cmds.append(c)

        return cmds


class SplitLine():
    """分割行"""

    def __init__(self, desc):
        self.desc = desc

    def to_s(self, style=''):
        total_len = 60
        lc = total_len - wcwidth.wcswidth(self.desc) - 2
        llc = int(lc / 2)
        rlc = llc
        if lc % 2 == 1:
            rlc += 1

        _ = ("-"*llc + ' ' + style + self.desc +
             Style.RESET_ALL + ' ' + "-"*rlc)

        return _
