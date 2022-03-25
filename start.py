#!/usr/bin/env python3
# Author: Elin

import cmder.main as main
from cmder.unit import print_error

try:
    main.app()
except (ValueError, TypeError) as e:
    print_error(repr(e))
except KeyboardInterrupt:
    exit()
