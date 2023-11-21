"""Parsing actions for the OZI commandline interface."""
from __future__ import annotations

import re
from argparse import Action
from dataclasses import asdict
from dataclasses import dataclass
from functools import lru_cache
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar
from typing import Self

if TYPE_CHECKING:  # pragma: no cover
    from argparse import ArgumentParser
    from argparse import Namespace
    from collections.abc import Sequence

from difflib import get_close_matches
from warnings import warn

from spdx_license_list import LICENSES
from trove_classifiers import classifiers

from .spec import License

CLASSIFIER_RE = re.compile(r'^([\w\s]*\s\:\:\s)?')


@lru_cache
def get_trove_prefix(text: str) -> str | None:
    if m := re.match(CLASSIFIER_RE, text):
        return str(m[0])
    return None  # pragma: no cover


valid_trove_prefixes = set(map(get_trove_prefix, classifiers))


@dataclass(frozen=True, slots=True, eq=True)
class Prefix:
    audience: str = 'Intended Audience :: '
    environment: str = 'Environment :: '
    framework: str = 'Framework :: '
    language: str = 'Natural Language :: '
    license: str = 'License :: '
    status: str = 'Development Status :: '
    topic: str = 'Topic :: '

    def __post_init__(self: Self) -> None:
        if not valid_trove_prefixes.issuperset(asdict(self).values()):  # pragma: no cover
            warn('Possible deprecated Classifier prefix literal.', FutureWarning)


@lru_cache
def from_prefix(prefix: str) -> tuple[str, ...]:
    return tuple(i[len(prefix) :].lstrip() for i in classifiers if i.startswith(str(prefix)))


@dataclass
class ExactMatch:
    _prefix = Prefix()
    audience = from_prefix(_prefix.audience)
    language = from_prefix(_prefix.language)
    framework = from_prefix(_prefix.framework)
    environment = from_prefix(_prefix.environment)
    license = from_prefix(_prefix.license)
    license_id: ClassVar[list[str]] = [
        k for k, v in LICENSES.items() if v.deprecated_id is False
    ]
    license_exception_id = License().exceptions
    status = from_prefix(_prefix.status)
    topic = from_prefix(_prefix.topic)


class CloseMatch(Action):
    """Special choices action. Warn the user if a close match could not be found."""

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
        value: Sequence[str],
    ) -> Sequence[str]:
        """Get a single close match for a class attribute."""
        if value is None:
            return []  # pragma: defer to good-first-issue
        try:
            value = get_close_matches(
                value,
                self.exact_match.__getattribute__(key),
                cutoff=0.40,
            )[0]
        except (IndexError, AttributeError):
            warn(
                f'No {key} choice matching "{value}" available.'
                'To list available options:'
                f'$ ozi-new -l {key}',
                RuntimeWarning,
                stacklevel=0,
            )
        return value

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

        if self.nargs == '?':
            matches: list[str] = []
            for v in values:
                v = self.close_matches(key, v)  # type: ignore
                matches += v
            setattr(namespace, self.dest, matches)
        else:
            values = self.close_matches(key, values)
            setattr(namespace, self.dest, values)
