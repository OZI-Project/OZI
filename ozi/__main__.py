"""OZI - Python Project Packaging
This is the main OZI console application.
OZI also comes with two additional console applications:
ozi-new project quick-start and ozi-fix editing.
"""
import argparse
import sys
from importlib_metadata import version
from typing import NoReturn, Union


def print_version() -> None:
    """print current version string"""
    print(version('ozi'))
    exit(0)


parser = argparse.ArgumentParser(
    prog='ozi',
    description=sys.modules[__name__].__doc__,
    add_help=False
)
helpers = parser.add_mutually_exclusive_group()
helpers.add_argument('-h', '--help', action='help', help='show this help message and exit')
helpers.add_argument(
    '-v',
    '--version',
    action='store_const',
    default=lambda: None,
    const=print_version,
    help='print out the current version and exit',
)


def main() -> Union[NoReturn, None]:
    """Main ozi entrypoint."""
    ozi = parser.parse_args()
    ozi.version()
    parser.print_help()


if __name__ == '__main__':
    main()
