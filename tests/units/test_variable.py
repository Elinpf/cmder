from sre_constants import ASSERT_NOT
from cmder.variable import Variable, VariableList


class TestVariable:
    def test_base(cls):
        """测试基本功能"""
        var = Variable('RHOST')
        assert var.name == 'RHOST'

    def test_set(cls):
        var = Variable('RHOST')
        var.set({'func': 'desc', 'value': 'remote host'})
        assert var.desc == 'remote host'

        var.set({'func': 'recommend', 'value': '192.168.1.1'})
        assert var.recommend[0] == '192.168.1.1'
        var.set({'func': 'recommend', 'value': '192.168.1.2'})
        assert var.recommend[1] == '192.168.1.2'

        var.set({'func': 'recommend_cmd', 'value': '-r'})
        assert var.recommend_cmd[0] == '-r'
        var.set({'func': 'recommend_cmd', 'value': '-d'})
        assert var.recommend_cmd[1] == '-d'

        var.set({'func': 'if_has', 'value': '-r %s'})
        assert var.if_has == '-r %s'

        var.set({'func': 'refresh'})
        assert len(var.recommend) == 0
        assert len(var.recommend_cmd) == 0

    def test_parse(cls):
        var = Variable('[-s] RHOST')
        assert var.name == 'RHOST'
        assert var.if_has == '-s %s'

    def test_merge(cls):
        var = Variable('RHOST')
        var.set({'func': 'desc', 'value': 'remote host'})
        var.set({'func': 'recommend', 'value': '192.168.1.1'})
        var.set({'func': 'recommend', 'value': '192.168.1.2'})

        other_var = Variable('RHOST')
        other_var.set({'func': 'desc', 'value': 'rhost'})
        other_var.set({'func': 'recommend', 'value': '10.10.10.1'})

        var.merge(other_var)

        assert var.desc == 'remote host'
        assert len(var.recommend) == 3
        assert var.recommend[2] == '10.10.10.1'

    def test_get_recommend(cls):
        var = Variable('RHOST')
        var.set({'func': 'recommend', 'value': '192.168.1.1'})
        var.set({'func': 'recommend', 'value': '192.168.1.2'})
        # TODO 还要增加 recommend_cmd

        recommend = var.get_recommend()
        assert len(recommend) == 2
        assert recommend == ['192.168.1.1', '192.168.1.2']

    def test_select(cls):
        var = Variable('RHOST')
        var.select = ' 10.10.10.1'
        assert var.select == '10.10.10.1'

        var = Variable('[-r] RHOST')
        var.select = '10.10.10.1'
        assert var.select == '-r 10.10.10.1'

        var = Variable('[-r] RHOST')
        var.select = ''
        assert var.if_has == '-r %s'
        assert var.select == ''


def create_list():
    varlist = VariableList()
    varlist.append(Variable('RHOST'))
    varlist.append('LHOST')
    return varlist


class TestVariableList:

    def test_append(cls):
        varlist = create_list()

        assert len(varlist.list) == 2
        assert type(varlist.list['LHOST']) == Variable

        # 有同名变量时，不做添加
        varlist.append('RHOST')
        assert len(varlist.list) == 2

    def test_key_with_var(cls):
        # ! 这个 key_with_var 方法修改为 __iter__ 魔法方法
        # ! 后面将移除 key_with_var 方法
        varlist = create_list()
        # for key, var in varlist.key_with_var():
        for key, var in varlist:
            assert type(key) == str  # RHOST
            assert type(var) == Variable

    def test_get_var(cls):
        varlist = create_list()
        var = varlist['RHOST']  # type: Variable
        assert var.name == 'RHOST'
        assert type(var) == Variable

    def test_len(cls):
        varlist = create_list()
        assert len(varlist) == 2

    def test_has_key(cls):
        # ! 后面将取消掉 has_key 方法
        varlist = create_list()
        assert varlist.has_key('RHOST')
        assert 'RHOST' in varlist

    def test_set(cls):
        varlist = VariableList()
        varlist.set({'name': 'RHOST', 'func': 'desc', 'value': 'remote host'})
        varlist.set({'name': 'LHOST', 'func': 'desc', 'value': 'local host'})

        assert varlist['RHOST'].name == 'RHOST'
        assert varlist['RHOST'].desc == 'remote host'
        assert varlist['LHOST'].name == 'LHOST'
        assert varlist['LHOST'].desc == 'local host'

    def test_merge(cls):
        """合并，当原来的列表中有相应的变量才会合并"""
        varlist = create_list()
        other_varlist = VariableList()
        other_varlist.set(
            {'name': 'RHOST', 'func': 'desc', 'value': 'remote host'})
        other_varlist.set(
            {'name': 'LHOST', 'func': 'desc', 'value': 'local host'})
        other_varlist.set(
            {'name': 'IP', 'func': 'desc', 'value': 'ip'})

        varlist.merge(other_varlist)
        assert varlist['RHOST'].desc == 'remote host'
        assert varlist['LHOST'].desc == 'local host'
        assert 'IP' not in varlist
