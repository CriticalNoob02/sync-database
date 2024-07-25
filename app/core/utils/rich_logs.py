import logging
import os
from rich.logging import RichHandler
from rich.console import Console


log_level = os.environ.get('LOG', 'INFO')
format = "%(message)s"
logging.basicConfig(
    level=log_level,
    format=format,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)


LOG = logging.getLogger("rich")


def get_traceback():
    locals = True if log_level == "DEBUG" else False
    c = Console()
    c.print_exception(show_locals=locals)
