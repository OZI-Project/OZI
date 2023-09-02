"""OZI - Python Project Packaging

Quick-start:
$ ozi-new

Add/remove files:
$ ozi-fix

"""
import argparse
import sys
from typing import NoReturn, Union


parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__)
parser.add_argument('-v', '--version', action='store_true')


def main() -> Union[NoReturn, None]:
    """Main ozi entrypoint."""
    parser.parse_args()

if __name__ == '__main__':
    main()
