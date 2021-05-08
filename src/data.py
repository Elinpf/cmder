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

        # patterns
        self.note_desc_pattern = r"^\s*desc\s*:"
        self.note_refer_pattern = r"^\s*refer\s*:"
        self.note_link_pattern = r"^\s*link\s*:"
        self.variable_pattern = r"#{(.*?)}"


pypaths = PyPaths()
pystrs = PyStrs()
pyoptions = PyOptions()
