"""OZI - Python Project Packaging
"""
import argparse
import sys
from importlib_metadata import version
from typing import NoReturn, Union


def print_version() -> None:
    """print current version string"""
    print(version('ozi'))
    exit(0)


overview = f"""
{sys.modules[__name__].__doc__}

This is the main OZI console application.
OZI also comes with two additional console applications:

Quick-start with ozi-new

Add/remove files with ozi-fix
"""
parser = argparse.ArgumentParser(description=overview, add_help=False)
helpers = parser.add_mutually_exclusive_group()
helpers.add_argument('-h', '--help', action='help', help='show this help message and exit')
helpers.add_argument(
    '-v',
    '--version',
    action='store_const',
    const=print_version,
    help='print out the current version and exit',
)


def main() -> Union[NoReturn, None]:
    """Main ozi entrypoint."""
    parser.parse_args()


if __name__ == '__main__':
    main()
