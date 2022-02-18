#!/usr/bin/env python3
# Author: Elin

from cmder.main import get_options
from rich.traceback import install

install(show_locals=True)

args = get_options()
try:
    args.func(args)
except ValueError as e:
    print("[-] " + repr(e))

except TypeError as e:
    exit()
