#!/usr/bin/env python3
# Author: Elin

from rich_typer import Abort
import cmder.main as main
from cmder.unit import print_error

try:
    main.app()
except (ValueError, TypeError) as e:
    print_error(repr(e))
    raise Abort()
except KeyboardInterrupt:
    raise Abort()
