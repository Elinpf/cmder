from cmder.parse import Parse
from cmder.command import SplitLine, Command


def test_split_area(shared_datadir):
    """检查分割区域"""
    # TODO 后面将SplitLine 和 Command 分开
    p = Parse()
    p._split_area(shared_datadir / 'sql_post.xd')
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
