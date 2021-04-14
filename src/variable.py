from collections import OrderedDict


class Variable:
    def __init__(self, name):
        self.name = ""  # 变量名称
        self.desc = ""  # 简短的描述，用于选择的时候给出标题
        self.recomm = []  # 推荐参数
        self.recomm_cmd = []  # 推荐参数，可以作为shell命令传入
        self.if_has = ""  # 当有if_has的使用，有选项值会将if_has带入进去替换
        self._select = ""  # 在选择后填入选项值
        self.refresh_tag = False
        self.key = ""  # #{} 中整个的字符串，用于替换
        self.parse(name)

    def parse(self, name):
        if "[" in name:
            self.name = name.split(']')[1].split('[')[0].strip()
            if_has = name.replace(self.name, '%s')
            if_has = if_has.replace('[', '')
            if_has = if_has.replace(']', '')
            self.if_has = if_has
        else:
            self.name = name.strip()

        self.key = name

    def append_recomm(self, string):
        if string in self.recomm:
            return

        self.recomm.append(string)

    def append_recomm_cmd(self, string):
        self.recomm_cmd.append(string)

    def refresh(self):
        self.recomm = []
        self.refresh_tag = True

    def set(self, info: dict):
        """info = {"func": function, "value": value}"""
        if info["func"] == "desc":
            if info["value"]:
                self.desc = info["value"]
        elif info["func"] == "refresh":
            self.refresh()
        elif info["func"] == "recommend":
            if info["value"]:
                self.append_recomm(info["value"])
        elif info["func"] == "recommend_cmd":
            if info["value"]:
                self.append_recomm_cmd(info["value"])
        elif info["func"] == "if_has":
            if info["value"]:
                self.if_has = info["value"]

    def merge(self, other_var):
        if not self.desc:
            self.desc = other_var.desc

        if not self.if_has:
            self.if_has = other_var.if_has

        if not self.refresh_tag:
            self.recomm += other_var.recomm
            self.recomm_cmd += other_var.recomm_cmd

    @property
    def select(self):
        if not self._select:
            return ""

        if self.if_has:
            return self.if_has.replace('%s', self._select)

        return self._select

    @select.setter
    def select(self, str):
        self._select = str.strip()

    def get_recomm(self):
        """获取所有推荐选项，返回数组"""
        list = []
        for c in self.recomm_cmd:
            #! 这里是要运行bash的
            list.append(c)

        list += self.recomm
        return list


class VariableList:
    """这个需要是数组，有顺序"""

    def __init__(self):
        self.list = OrderedDict()

    def append(self, var):
        if type(var) == Variable:
            if not self.has_key(var.name):
                self.list[var.name] = var
        else:
            if not self.has_key(var):
                var = Variable(var)
                self.list[var.name] = var

    def items(self):
        return self.list.items()

    def key_with_var(self):
        for _, var in self.items():
            yield (var.key, var)

    def __getitem__(self, key: str):
        return self.list[key]

    def __len__(self):
        return self.list.__len__()

    def has_key(self, key):
        return key in self.list

    def set(self, info: dict):
        """info = {"name": variables_name, "func": function, "value": value}"""
        if not self.has_key(info["name"]):
            self.append(info["name"])

        var = self.list[info["name"]]
        var.set(info)

    def merge(self, other_varlist):
        """合并，当原来的列表中有相应的变量才会合并"""
        for key, var in self.list.items():
            if not other_varlist.has_key(key):
                continue

            var.merge(other_varlist[key])

        return self.list

    def __bool__(self):
        return bool(self.list)
