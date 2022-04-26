from cmder.parse import Parse
from cmder.command import SplitLine, Command
from cmder.data import pyoptions

CONTEXT = """# desc: Login
# Login with mssqlclient.py
@RHOST.recommend(192.168.1.1)
mssqlclient.py #{DOMAIN}/#{USER}@#{RHOST} -windows-auth
# refer: https://book.hacktricks.xyz/pentesting"""


class TestParse():
    def test_parse_file(cls, shared_datadir):
        """检查分割区域"""
        # TODO 后面将SplitLine 和 Command 分开
        p = Parse()
        p.parse_file(shared_datadir / 'sql_post.xd')
        assert len(p.cmdlist.list) == 6
        assert isinstance(p.cmdlist.list[0], SplitLine)
        cmd: Command = p.cmdlist.list[1]
        assert isinstance(cmd, Command)
        assert cmd.cmd[0] == 'mssqlclient.py #{DOMAIN}/#{USER}@#{RHOST} -windows-auth'
        assert cmd.desc == 'Login'
        assert len(cmd.notes) == 1
        assert cmd.notes[0] == 'Login with mssqlclient.py'
        assert len(cmd.refer) == 1
        assert cmd.refer[0] == 'https://book.hacktricks.xyz/pentesting'
        assert str(cmd.vars.list.keys()
                   ) == "odict_keys(['DOMAIN', 'USER', 'RHOST'])"

    def test_parse_cmd_area(cls):
        area = CONTEXT.split('\n')
        p = Parse()
        cmd = Command(
            'mssqlclient.py #{DOMAIN}/#{USER}@#{RHOST} -windows-auth')
        cmd = p._parse_cmd_area(cmd, area)  # type: Command
        assert len(cmd.cmd) == 1
        assert cmd.cmd[0] == 'mssqlclient.py #{DOMAIN}/#{USER}@#{RHOST} -windows-auth'
        assert cmd.vars['RHOST'].recommend.pop() == '192.168.1.1'

    def test_parse_normal_area(cls):
        area = CONTEXT.split('\n')
        area.remove(
            'mssqlclient.py #{DOMAIN}/#{USER}@#{RHOST} -windows-auth')

        p = Parse()
        p._parse_normal_area(area)
        assert len(p.g_varlist) == 1
        assert p.g_varlist['RHOST'].recommend.pop() == '192.168.1.1'
        notes = [
            'desc: Login',
            'Login with mssqlclient.py',
            'refer: https://book.hacktricks.xyz/pentesting'
        ]
        assert p.notes == notes
