# ozi/actions.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Parsing actions for the OZI commandline interface."""
from __future__ import annotations

import json
import sys
from argparse import Action
from dataclasses import dataclass
from difflib import get_close_matches
from typing import TYPE_CHECKING
from typing import Any
from typing import Collection
from typing import NoReturn
from warnings import warn

if TYPE_CHECKING:
    from argparse import ArgumentParser
    from argparse import Namespace
    from collections.abc import Sequence

    if sys.version_info >= (3, 11):
        from typing import Self
    elif sys.version_info < (3, 11):
        from typing_extensions import Self

import requests
from packaging.version import Version
from packaging.version import parse
from pyparsing import ParseException
from spdx_license_list import LICENSES

from ozi.spdx import spdx_license_expression
from ozi.spec import METADATA
from ozi.tap import TAP
from ozi.trove import Prefix
from ozi.trove import from_prefix

_prefix = Prefix()


@dataclass
class ExactMatch:
    """Exact matches data for packaging core metadata."""

    audience: tuple[str, ...] = from_prefix(_prefix.audience)
    language: tuple[str, ...] = from_prefix(_prefix.language)
    framework: tuple[str, ...] = from_prefix(_prefix.framework)
    environment: tuple[str, ...] = from_prefix(_prefix.environment)
    license: tuple[str, ...] = from_prefix(_prefix.license)
    license_id: tuple[str, ...] = tuple(
        k for k, v in LICENSES.items() if v.deprecated_id is False
    )
    license_exception_id: tuple[str, ...] = METADATA.spec.python.pkg.license.exceptions
    status: tuple[str, ...] = from_prefix(_prefix.status)
    topic: tuple[str, ...] = from_prefix(_prefix.topic)


class CloseMatch(Action):
    """Special argparse choices action. Warn the user if a close match could not be found."""

    exact_match = ExactMatch()

    def __init__(
        self: Self,  # pyright: ignore
        option_strings: list[str],
        dest: str,
        nargs: int | str | None = None,
        **kwargs: Any,
    ) -> None:
        """Argparse init"""
        if nargs not in [None, '?']:
            text = 'nargs (other than "?") not allowed'
            raise ValueError(text)

        super().__init__(option_strings, dest, nargs=nargs, **kwargs)

    def close_matches(
        self: Self,
        key: str,
        value: str,
    ) -> Sequence[str]:
        """Get a close matches for a Python project packaging core metadata key.

        :param key: Python project packaging core metadata key name (normalized)
        :type key: str
        :param value: the value to query a close match for
        :type value: Sequence[str]
        :return: sequence with the best match or an empty sequence
        :rtype: Sequence[str]
        """
        if value is None:
            return []  # pragma: defer to good-first-issue
        no_match = False
        matches: list[str] | str = []
        if hasattr(self.exact_match, key):
            matches = get_close_matches(
                value,
                self.exact_match.__getattribute__(key),
                cutoff=0.40,
            )
            no_match = False if len(matches) else True
        else:  # pragma: no cover
            matches = [value]
            no_match = True
        if no_match:
            warn(
                f'No {key} choice matching "{value}" available.'
                'To list available options:'
                f'$ ozi-new -l {key}',
                RuntimeWarning,
                stacklevel=0,
            )
        return matches

    def _set_matches(
        self: Self,
        key: str,
        values: str | Sequence[str],
        namespace: Namespace,
    ) -> None:
        """Set the matches for a key in namespace."""
        match self.nargs:
            case '?':
                setattr(namespace, self.dest, [self.close_matches(key, v) for v in values])
            case _:
                setattr(
                    namespace,
                    self.dest,
                    self.close_matches(
                        key,
                        values if isinstance(values, str) else values[0],
                    ),
                )

    def __call__(
        self: Self,
        parser: ArgumentParser,
        namespace: Namespace,
        values: str | Sequence[str] | None,
        option_string: str | None = None,
    ) -> None:
        """Find closest matching class attribute."""
        if values is None:
            return
        if option_string is not None:
            key = option_string.lstrip('-').replace('-', '_')
        else:
            key = ''  # pragma: defer to good-first-issue
        self._set_matches(key, values, namespace)


def print_version() -> NoReturn:  # pragma: no cover
    """Print out the current version and exit."""
    print(METADATA.ozi.version)
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
                current_version=parse(METADATA.ozi.version),
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
    sys.exit(print(json.dumps(METADATA.asdict(), indent=2)))


def list_available(key: str) -> NoReturn:  # pragma: no cover
    """Print a list of valid values for a key and exit."""
    sys.exit(print(*sorted(getattr(ExactMatch, key.replace('-', '_'))), sep='\n'))


def license_expression(expr: str) -> NoReturn:  # pragma: no cover
    """Validate a SPDX license expression."""
    try:
        spdx_license_expression.parse_string(expr, parse_all=True)
        TAP.ok(expr, 'parsed successfully')
    except ParseException as e:
        TAP.not_ok(expr, str(e))
    TAP.end()
