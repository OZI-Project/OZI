# ozi/__main__.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""OZI - Python Project Packaging
This is the main OZI console application.
OZI also comes with two additional console applications:
ozi-new project quick-start and ozi-fix editing.
"""  # pragma: no cover
import argparse  # pragma: no cover
import sys  # pragma: no cover
from importlib.metadata import version  # pragma: no cover
from typing import NoReturn, Union  # pragma: no cover


def print_version() -> NoReturn:  # pragma: no cover
    """print current version string"""
    print(version('ozi'))
    exit(0)


parser = argparse.ArgumentParser(
    prog='ozi', description=sys.modules[__name__].__doc__, add_help=False
)  # pragma: no cover
helpers = parser.add_mutually_exclusive_group()  # pragma: no cover
helpers.add_argument(
    '-h', '--help', action='help', help='show this help message and exit'
)  # pragma: no cover
helpers.add_argument(  # pragma: no cover
    '-v',
    '--version',
    action='store_const',
    default=lambda: None,
    const=print_version,
    help='print out the current version and exit',
)


def main() -> Union[NoReturn, str]:  # pragma: no cover
    """Main ozi entrypoint."""
    ozi = parser.parse_args()
    ozi.version()
    parser.print_help()
    return 'ok'


if __name__ == '__main__':
    main()
