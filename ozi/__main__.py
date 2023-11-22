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
from __future__ import annotations  # pragma: no cover

import argparse  # pragma: no cover
import json  # pragma: no cover
import sys  # pragma: no cover
import warnings  # pragma: no cover
from dataclasses import fields  # pragma: no cover
from typing import TYPE_CHECKING  # pragma: no cover
from typing import NoReturn  # pragma: no cover

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Collection

from warnings import warn  # pragma: no cover

import requests  # pragma: no cover
from packaging.version import Version  # pragma: no cover
from packaging.version import parse  # pragma: no cover

from ozi.actions import ExactMatch  # pragma: no cover
from ozi.spec import Metadata  # pragma: no cover

metadata = Metadata()  # pragma: no cover


def tap_warning_format(  # pragma: no cover
    message: Warning | str,
    category: type[Warning],
    filename: str,
    lineno: int,
    line: str | None = None,
) -> str:
    """Test Anything Protocol formatted warnings."""
    return f'# {filename}:{lineno}: {category.__name__}\nnot ok - {message}\n'  # pragma: no cover


pywarningformat = warnings.formatwarning  # pragma: no cover
warnings.formatwarning = tap_warning_format  # pragma: no cover


def print_version() -> NoReturn:  # pragma: no cover
    """Print out the current version and exit."""
    print(metadata.ozi.version)
    sys.exit(0)


def check_for_update(
    current_version: Version,
    releases: Collection[Version],
) -> None:  # pragma: no cover
    """Issue a warning if installed version of OZI is not up to date."""
    match max(releases):
        case latest if latest > current_version:
            warn(
                f'Newer version of OZI ({latest} > {current_version}) available to download on PyPI: '
                'https://pypi.org/project/OZI/',
                RuntimeWarning,
                stacklevel=0,
            )
        case latest if latest < current_version:
            print(f'ok - OZI package is development version ({current_version}).')
        case latest if latest == current_version:
            print(f'ok - OZI package is up to date ({current_version}).')


def check_version() -> NoReturn:  # pragma: no cover
    """Check for a newer version of OZI and exit."""
    response = requests.get('https://pypi.org/pypi/OZI/json', timeout=30)
    match response.status_code:
        case 200:
            check_for_update(
                current_version=parse(Metadata().ozi.version),
                releases=set(map(parse, response.json()['releases'].keys())),
            )
            print('1..1')
        case _:
            print(
                '1..0 # skip OZI package version check with status code'
                f' {response.status_code}.',
            )
    sys.exit(0)


def info() -> NoReturn:  # pragma: no cover
    """Print all metadata as JSON and exit."""
    sys.exit(print(json.dumps(metadata.asdict(), indent=2)))


def list_available(key: str) -> NoReturn:  # pragma: no cover
    """Print a list of valid values for a key and exit."""
    sys.exit(print(*sorted(getattr(ExactMatch, key.replace('-', '_'))), sep='\n'))


parser = argparse.ArgumentParser(
    prog='ozi',
    description=sys.modules[__name__].__doc__,
    add_help=False,
    formatter_class=argparse.RawDescriptionHelpFormatter,
)  # pragma: no cover
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
    choices={i.name for i in fields(ExactMatch) if i.repr},
)


def main() -> NoReturn | str:  # pragma: no cover
    """Main ozi entrypoint."""
    ozi = parser.parse_args()
    ozi.version()
    ozi.check_version()
    warnings.filterwarnings = pywarningformat  # type: ignore
    ozi.info()
    if ozi.list_available:
        list_available(ozi.list_available)
    parser.print_help()
    return 'ok'


if __name__ == '__main__':
    main()
