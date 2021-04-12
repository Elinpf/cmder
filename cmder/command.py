import re

from cmder.variable import VariableList


class Command():
    def __init__(self, line):
        self.cmd = [line]
        self.refer = []
        self.notes = []
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

    def add_note(self, line):
        self.notes.append(line)

    def add_refer(self, line):
        self.refer.append(line)

    def add_cmd(self, line):
        self.cmd.append(line)

    def merge_var(self, g_varlist):
        return self.vars.merge(g_varlist)

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
        return self.list[index]
