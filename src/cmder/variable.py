from __future__ import annotations

from collections import OrderedDict
from typing import Generator, Iterator, Tuple


class Variable:
    def __init__(self, name: str):
        self.name = ""  # 变量名称
        self.desc = ""  # 简短的描述，用于选择的时候给出标题
        self.recommend = []  # 推荐参数
        self.recommend_cmd = []  # 推荐参数，可以作为shell命令传入
        self.if_has = ""  # 当有if_has的使用，有选项值会将if_has带入进去替换
        self._select = ""  # 在选择后填入选项值
        self.refresh_tag = False
        self.key = ""  # #{} 中整个的字符串，用于替换
        self.parse(name)

    def parse(self, name: str) -> None:
        if "[" in name:
            self.name = name.split(']')[1].split('[')[0].strip()
            if_has = name.replace(self.name, '%s')
            if_has = if_has.replace('[', '')
            if_has = if_has.replace(']', '')
            self.if_has = if_has
        else:
            self.name = name.strip()

        self.key = name

    def append_recommend(self, string: str) -> None:
        if string in self.recommend:
            return

        self.recommend.append(string)

    def append_recommend_cmd(self, string: str) -> None:
        self.recommend_cmd.append(string)

    def refresh(self) -> None:
        self.recommend.clear()
        self.recommend_cmd.clear()
        self.refresh_tag = True

    def set(self, info: dict) -> None:
        """info = {"func": function, "value": value}"""
        if info["func"] == "desc":
            if info["value"]:
                self.desc = info["value"]
        elif info["func"] == "refresh":
            self.refresh()
        elif info["func"] == "recommend":
            if info["value"]:
                self.append_recommend(info["value"])
        elif info["func"] == "recommend_cmd":
            if info["value"]:
                self.append_recommend_cmd(info["value"])
        elif info["func"] == "if_has":
            if info["value"]:
                self.if_has = info["value"]

    def merge(self, other_var: "Variable") -> None:
        if not self.desc:
            self.desc = other_var.desc

        if not self.if_has:
            self.if_has = other_var.if_has

        if not self.refresh_tag:
            for o in other_var.recommend:
                if o not in self.recommend:
                    self.recommend.append(o)

                # self.recommend_cmd += other_var.recommend_cmd

    @property
    def select(self) -> str:
        # ! 这个判断可以去掉
        if not self._select:
            return ""

        if self.if_has:
            return self.if_has.replace('%s', self._select)

        return self._select

    @select.setter
    def select(self, str: str):
        self._select = str.strip()

    def get_recommend(self) -> list:
        """获取所有推荐选项，返回数组"""
        list = []
        for c in self.recommend_cmd:
            # TODO 增加 bash 语句生成推荐项的支持
            list.append(c)

        list += self.recommend
        return list


class VariableList:
    """这个需要是数组，有顺序"""

    def __init__(self):
        self.list = OrderedDict()

    def append(self, var: Variable | str) -> None:
        if type(var) == Variable:
            if var.name not in self:
                self.list[var.name] = var
        else:
            if var not in self:
                var = Variable(var)
                self.list[var.name] = var

    def items(self) -> Iterator[Tuple[str, Variable]]:
        return self.list.items()

    def key_with_var(self) -> Generator[Tuple[str, Variable], None, None]:
        for _, var in self.items():
            yield (var.key, var)

    def __getitem__(self, key: str) -> Variable:
        return self.list[key]

    def __len__(self) -> int:
        return self.list.__len__()

    def has_key(self, key: str) -> bool:
        return key in self.list

    def __iter__(self) -> Generator[Tuple[str, Variable], None, None]:
        for _, var in self.items():
            yield (var.key, var)

    def __contains__(self, key: str) -> bool:
        return key in self.list

    def set(self, info: dict):
        """info = {"name": variables_name, "func": function, "value": value}"""
        if info['name'] not in self:
            self.append(info["name"])

        var = self.list[info["name"]]
        var.set(info)

    def merge(self, other_varlist: "VariableList") -> list:
        """合并，当原来的列表中有相应的变量才会合并"""
        for key, var in self.list.items():
            if key not in other_varlist:
                continue

            var.merge(other_varlist[key])

        return self.list

    def __bool__(self) -> bool:
        return bool(self.list)
