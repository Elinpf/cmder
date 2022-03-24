from rich.console import Console
from rich.theme import Theme
from rich.highlighter import RegexHighlighter

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
