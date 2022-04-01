from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.theme import Theme

console = Console(
    theme=Theme(
        {
            "variable": "dim",
        }
    )
)


class CommandHighlighter(RegexHighlighter):
    highlights = [
        r"(?P<variable>#{.*?})"
    ]


def custom_str(style: str, message: str) -> str:
    return f"[{style}]{message}[/{style}]"


def dim(s): return custom_str('dim', s)
def red(s): return custom_str('red', s)
def blue(s): return custom_str('blue', s)
def green(s): return custom_str('green', s)
def yellow(s): return custom_str('yellow', s)
def magenta(s): return custom_str('magenta', s)
def bright_red(s): return custom_str('bright_red', s)
def bright_blue(s): return custom_str('bright_blue', s)
def bright_green(s): return custom_str('bright_green', s)
def bright_yellow(s): return custom_str('bright_yellow', s)
def bright_magenta(s): return custom_str('bright_magenta', s)


cmd_highlighter = CommandHighlighter()
