# ozi/actions.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Parsing actions for the OZI commandline interface."""
from __future__ import annotations

from argparse import Action
from dataclasses import dataclass
from difflib import get_close_matches
from typing import TYPE_CHECKING
from typing import Any
from warnings import warn

if TYPE_CHECKING:
    import sys
    from argparse import ArgumentParser
    from argparse import Namespace
    from collections.abc import Sequence

    if sys.version_info >= (3, 11):
        from typing import Self
    elif sys.version_info < (3, 11):
        from typing_extensions import Self

from spdx_license_list import LICENSES

from ozi.spec import METADATA
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
        self: Self,
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
