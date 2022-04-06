import os


class PyPaths():
    def __init__(self):
        # soft path
        self.root_path = os.path.split(
            os.path.split(os.path.abspath(__file__))[0])[0]

        # user path
        self.user_path = os.path.expanduser('~')
        self.custom_path = os.path.join(self.user_path, '.cmder')
        self.custom_db_path = os.path.join(self.custom_path, 'db')
        self.custom_script_path = os.path.join(self.custom_path, 'scripts')
        self.history_path = os.path.join(self.custom_path, 'history')
        self.sequence_path = os.path.join(self.custom_path, '.sequence')

    @property
    def db_root_path(self):
        # 取数据库根目录，包含db和scripts文件夹
        from . import conf
        if conf.get_global_config('db_path'):
            return conf.get_global_config('db_path')
        return self.root_path

    @property
    def db_path(self):
        return os.path.join(self.db_root_path, 'db')

    @property
    def scripts_path(self):
        return os.path.join(self.db_root_path, 'scripts')


class PyStrs():
    def __init__(self):
        self.init_file = '__init__.xd'
        self.config_file = 'config.json'
        self.menu_custom_str = '(Custom)'
        self.menu_back_str = '(Back)'


class PyOptions():
    def __init__(self):
        self.windows_separator = '\\'
        self.linux_separator = '/'
        self.splitline_char = '-'
        self.note_separator = ':'
        self.db_file_suffix = '.xd'
        self.encode_flag = 'cmder_encode'

        # patterns
        self.note_desc_pattern = r"^\s*desc\s*:"
        self.note_refer_pattern = r"^\s*refer\s*:"
        self.note_link_pattern = r"^\s*link\s*:"
        self.variable_pattern = r"#{(.*?)}"
        self.multi_line_note_pattern = r'"""((?:.|\n)*?)"""'

        # cmdlist
        self.cmd_list = None


pypaths = PyPaths()
pystrs = PyStrs()
pyoptions = PyOptions()

banner = """[bold bule]
             _____                   _
            / ____|                 | |
           | |       _ __ ___     __| |   ___   _ __
           | |      | '_ ` _ \   / _` |  / _ \ | '__|
           | |____  | | | | | | | (_| | |  __/ | |
            \_____| |_| |_| |_|  \__,_|  \___| |_|  [bold yellow]ver:{version}[/bold yellow]

                        [bold magenta]GitHub:{url}[/bold magenta]
                        [yellow]Database:{db}[/]
                                            [bold green]--Author:Elin[/bold green] 
[bold bule]"""

repository_url = 'https://github.com/Elinpf/cmder'
database_url = 'https://github.com/Elinpf/cmder_db'
