import os


class PyPaths():
    def __init__(self):
        # soft path
        self.root_path = os.path.split(
            os.path.split(os.path.abspath(__file__))[0])[0]
        self.db_path = os.path.join(self.root_path, 'db')

        # user path
        self.user_path = os.path.expanduser('~')
        self.custom_path = os.path.join(self.user_path, '.cmder')
        self.custom_db_path = os.path.join(self.custom_path, 'db')
        self.history_path = os.path.join(self.custom_path, 'history')
        self.sequence_path = os.path.join(self.custom_path, '.sequence')


class PyStrs():
    def __init__(self):
        self.init_file = '__init__.xd'
        self.config_file = 'config.json'
        self.menu_custom_str = '(Custom)'


class PyOptions():
    def __init__(self):
        self.windows_separator = '\\'
        self.linux_separator = '/'
        self.splitline_char = '-'
        self.note_separator = ':'
        self.db_file_suffix = '.xd'
        self.splitline_color = 'FUCHSIA'
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

                        [bold magenta]GitHub:https://github.com/Elinpf/cmder[/bold magenta]
                                            [bold green]--Info:Elin[/bold green] 
[bold bule]"""
