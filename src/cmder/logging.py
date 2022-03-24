import logging

from rich.logging import RichHandler

FORMAT = "%(message)s"
# FORMAT = "%(asctime)-15s - %(levelname)s - %(message)s"
logging.basicConfig(
    level="NOTSET",
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, tracebacks_show_locals=True)],
)

log = logging.getLogger("cmder")
