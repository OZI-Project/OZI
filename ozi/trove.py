# ozi/trove.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Trove packaging classifiers interface."""
from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from functools import lru_cache
from typing import TYPE_CHECKING
from warnings import warn

from ozi_spec._license import NOT_SUPPORTED  # pyright: ignore
from trove_classifiers import classifiers

if TYPE_CHECKING:
    import sys

    if sys.version_info >= (3, 11):
        from typing import Self
    elif sys.version_info < (3, 11):
        from typing_extensions import Self


@lru_cache
def get_trove_prefix(text: str) -> str | None:
    """Get a trove classifier prefix from a classifier string.

    :param text: full classifier text
    :type text: str
    :return: the prefix if the classifier text is valid otherwise None
    :rtype: str | None
    """
    prefix, partition, _ = text.partition(' :: ')
    if partition:
        return prefix + partition
    return None  # pragma: no cover


valid_trove_prefixes = set(map(get_trove_prefix, classifiers))


@dataclass(frozen=True, slots=True, eq=True)
class Prefix:
    """Trove :term:`classifier` prefix literals for :term:`PyPI`"""

    audience: str = 'Intended Audience :: '
    environment: str = 'Environment :: '
    framework: str = 'Framework :: '
    language: str = 'Natural Language :: '
    license: str = 'License :: '
    status: str = 'Development Status :: '
    topic: str = 'Topic :: '

    def __post_init__(self: Self) -> None:
        """Check if any of the default attributes are deprecated upstream."""
        if not valid_trove_prefixes.issuperset(asdict(self).values()):  # pragma: no cover
            warn('Possible deprecated Classifier prefix literal.', FutureWarning)


@lru_cache
def from_prefix(prefix: str) -> tuple[str, ...]:
    """Return all matching classifiers for a prefix string."""
    match prefix:
        case 'License :: ':
            matches = []
            for c in classifiers:
                selected = c[len(prefix) :].lstrip()
                if c.startswith(str(prefix)) and selected not in NOT_SUPPORTED:
                    matches += [selected]
            return tuple(matches)
        case _:
            return tuple(
                i[len(prefix) :].lstrip() for i in classifiers if i.startswith(str(prefix))
            )
