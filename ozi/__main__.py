# ozi/__main__.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""OZI - Python Project Packaging console application.

Most functionality is found in two additional console applications:

ozi-new:
  project authoring command

ozi-fix:
  project maintainence command

"""  # pragma: no cover
import argparse  # pragma: no cover
import json  # pragma: no cover
import sys  # pragma: no cover
from importlib.metadata import version  # pragma: no cover
from typing import NoReturn, Union  # pragma: no cover

import requests  # pragma: no cover
from packaging.version import parse  # pragma: no cover

from . import check_for_update, metadata  # pragma: no cover
from .assets import CloseMatch  # pragma: no cover


def print_version() -> NoReturn:  # pragma: no cover
    """print current version string"""
    print(version('ozi'))
    exit(0)


def check_version() -> NoReturn:  # pragma: no cover
    """print out the current version and exit"""
    response = requests.get('https://pypi.org/pypi/OZI/json', timeout=30)
    match response.status_code:
        case 200:
            check_for_update(
                current_version=parse(version('OZI')),
                releases=response.json()['releases'].keys(),
            )
            print('1..1')
        case _:
            print(
                '1..0 # skip OZI package version check with status code'
                f' {response.status_code}.'
            )
    exit(0)


def info() -> NoReturn:  # pragma: no cover
    """check for a newer version and exit"""
    exit(print(json.dumps(metadata, indent=2)))


def list_available(key: str) -> NoReturn:  # pragma: no cover
    """print a list of valid values for a key and exit"""
    exit(print(*sorted((getattr(CloseMatch, key.replace('-', '_')))), sep='\n'))


parser = argparse.ArgumentParser(
    prog='ozi',
    description=sys.modules[__name__].__doc__,
    add_help=False,
    formatter_class=argparse.RawDescriptionHelpFormatter,
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
    help=print_version.__doc__,
)
helpers.add_argument(  # pragma: no cover
    '-c',
    '--check-version',
    action='store_const',
    default=lambda: None,
    const=check_version,
    help=check_version.__doc__,
)
helpers.add_argument(  # pragma: no cover
    '-i',
    '--info',
    action='store_const',
    default=lambda: None,
    const=info,
    help=info.__doc__,
)
helpers.add_argument(  # pragma: no cover
    '-l',
    '--list-available',
    help=list_available.__doc__,
    action='store',
    choices={
        'audience',
        'environment',
        'framework',
        'language',
        'license',
        'license-id',
        'license-exception-id',
        'status',
        'topic',
    },
)


def main() -> Union[NoReturn, str]:  # pragma: no cover
    """Main ozi entrypoint."""
    ozi = parser.parse_args()
    ozi.version()
    ozi.check_version()
    ozi.info()
    if ozi.list_available:
        list_available(ozi.list_available)
    parser.print_help()
    return 'ok'


if __name__ == '__main__':
    main()
