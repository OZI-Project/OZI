# ozi/__main__.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""OZI - Python Project Packaging console application.

project authoring console application:
  ozi-new -h         show help for the ozi-new command.

project maintainence console application:
  ozi-fix -h         show help for the ozi-fix command.

continuous integration checkpoints:
  tox -e lint        run formatting, linting, and typechecking.
  tox -e test        run testing and coverage.
  tox -e dist        run distribution and packaging.
"""  # pragma: no cover
from __future__ import annotations  # pragma: no cover

import argparse  # pragma: no cover
import json  # pragma: no cover
import sys  # pragma: no cover
from dataclasses import fields  # pragma: no cover
from typing import TYPE_CHECKING  # pragma: no cover
from typing import NoReturn  # pragma: no cover

from pyparsing import ParseException  # pragma: no cover

if TYPE_CHECKING:
    from collections.abc import Collection

import requests  # pragma: no cover
from packaging.version import Version  # pragma: no cover
from packaging.version import parse  # pragma: no cover

from ozi.actions import ExactMatch  # pragma: no cover
from ozi.fix.__main__ import main as fix_main  # pragma: no cover
from ozi.new.__main__ import main as new_main  # pragma: no cover
from ozi.spdx import spdx_license_expression  # pragma: no cover
from ozi.spec import Metadata  # pragma: no cover
from ozi.tap import TAP  # pragma: no cover

metadata = Metadata()  # pragma: no cover


def print_version() -> NoReturn:  # pragma: no cover
    """Print out the current version and exit."""
    print(metadata.ozi.version)
    sys.exit(0)


def check_for_update(
    current_version: Version,
    releases: Collection[Version],
) -> None:  # pragma: defer to python
    """Issue a warning if installed version of OZI is not up to date."""
    match max(releases):
        case latest if latest > current_version:
            TAP.not_ok(
                f'Newer version of OZI ({latest} > {current_version})',
                'available to download on PyPI',
                'https://pypi.org/project/OZI/',
            )
        case latest if latest < current_version:
            TAP.ok('OZI package is development version', str(current_version))
        case latest if latest == current_version:
            TAP.ok('OZI package is up to date', str(current_version))


def check_version() -> NoReturn:  # pragma: defer to PyPI
    """Check for a newer version of OZI and exit."""
    response = requests.get('https://pypi.org/pypi/OZI/json', timeout=30)
    match response.status_code:
        case 200:
            check_for_update(
                current_version=parse(Metadata().ozi.version),
                releases=set(map(parse, response.json()['releases'].keys())),
            )
            TAP.end()
        case _:
            TAP.end(
                skip_reason='OZI package version check failed with status code'
                f' {response.status_code}.',
            )


def info() -> NoReturn:  # pragma: no cover
    """Print all metadata as JSON and exit."""
    sys.exit(print(json.dumps(metadata.asdict(), indent=2)))


def list_available(key: str) -> NoReturn:  # pragma: no cover
    """Print a list of valid values for a key and exit."""
    sys.exit(print(*sorted(getattr(ExactMatch, key.replace('-', '_'))), sep='\n'))


def license_expression(expr: str) -> NoReturn:  # pragma: no cover
    try:
        spdx_license_expression.parse_string(expr, parse_all=True)
        TAP.ok(expr, 'parsed successfully')
    except ParseException as e:
        TAP.not_ok(expr, str(e))
    TAP.end()


parser = argparse.ArgumentParser(
    prog='ozi',
    description=sys.modules[__name__].__doc__,
    add_help=False,
    formatter_class=argparse.RawDescriptionHelpFormatter,
)  # pragma: no cover
tools = parser.add_mutually_exclusive_group()  # pragma: no cover
tools.add_argument(  # pragma: no cover
    '-fix',
    action='store_const',
    default=lambda: None,
    const=fix_main,
    help='alternate entrypoint for ozi-fix',
)
tools.add_argument(  # pragma: no cover
    '-new',
    action='store_const',
    default=lambda: None,
    const=new_main,
    help='alternate entrypoint for ozi-new',
)
helpers = parser.add_mutually_exclusive_group()  # pragma: no cover
helpers.add_argument(
    '-h',
    '--help',
    action='help',
    help='show this help message and exit',
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
    '-e',
    '--license-expression',
    action='store',
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
    choices={i.name.replace('_', '-') for i in fields(ExactMatch) if i.repr},
)


def main() -> None:  # pragma: no cover
    ozi, args = parser.parse_known_args()
    ozi.version()
    ozi.check_version()
    ozi.info()
    if ozi.list_available:
        list_available(ozi.list_available)
    elif ozi.license_expression:
        license_expression(ozi.license_expression)
    ozi.fix()
    ozi.new()
    parser.print_help()


if __name__ == '__main__':
    """Main ozi entrypoint."""
    main()
