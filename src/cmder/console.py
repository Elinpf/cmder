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


cmd_highlighter = CommandHighlighter()
