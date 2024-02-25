# ozi/tap.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
from __future__ import annotations

import os
import sys
import warnings
from collections import Counter
from contextlib import ContextDecorator
from contextlib import contextmanager
from contextlib import redirect_stdout
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

    if sys.version_info >= (3, 11):
        from typing import Self
    elif sys.version_info < (3, 11):
        from typing_extensions import Self

from typing import Generator
from typing import NoReturn
from typing import TextIO

OK = 'ok'
NOT_OK = 'not_ok'
SKIP = 'skip'


def tap_warning_format(
    message: Warning | str,
    category: type[Warning],
    filename: str,
    lineno: int,
    line: str | None = None,
) -> str:
    """Test Anything Protocol formatted warnings."""
    return f'# {category.__name__}\n'  # pragma: no cover


def tap_warn(
    message: Warning | str,
    category: type[Warning],
    filename: str,
    lineno: int,
    line: TextIO | None = None,
    stacklevel: int = 1,
) -> None:
    """emit a TAP formatted warning."""
    sys.stdout.write(f'not ok {message}\n')  # pragma: no cover
    sys.stderr.write(  # pragma: no cover
        warnings.formatwarning(message, category, filename, lineno),
    )


class TAP(ContextDecorator):
    """Test Anything Protocol warnings for TAP Producer APIs with a simple decorator.

    Redirects warning messages to stdout with the diagnostic printed to stderr.

    All TAP API calls reference the same thread context.

    :note:`Subtests are not implemented.`

    :note:`Not known to be thread-safe.`
    """

    _formatwarning = staticmethod(warnings.formatwarning)
    _showwarning = staticmethod(warnings.showwarning)
    _count = Counter(ok=0, not_ok=0, skip=0)

    @classmethod
    def end(cls: type[Self], skip_reason: str = '') -> NoReturn:  # pragma: no cover
        skip = cls._count.pop(SKIP)
        count = cls._count.total()
        match [count, skip_reason, skip]:
            case [0, reason, s] if [reason, s] and reason != '' and skip > 0:
                sys.stdout.write(f'1..{count} # SKIP {reason}\n')
                sys.exit(0)
            case [0, reason, s] if [reason, s] and reason == '' and skip > 0:
                sys.stdout.write(f'1..{count} # SKIP no "skip_reason" provided\n')
                sys.exit(0)
            case [n, reason, s] if [reason, s] and reason == '' and skip > 0:
                sys.stdout.write(f'1..{count}\n')
                sys.exit(0)
            case [n, reason, 0] if [n, reason] and reason != '' and count > 0:
                TAP.diagnostic('unecessary argument "skip_reason" to TAP.end')
                sys.stdout.write(f'1..{count}\n')
                sys.exit(0)
            case [n, reason, 0] if [n, reason] and reason == '' and count > 0:
                sys.stdout.write(f'1..{count}\n')
                sys.exit(0)
            case _:
                TAP.bail_out('TAP.end failed due to invalid arguments.')

    @staticmethod
    def diagnostic(*message: str) -> None:
        """Print a diagnostic message."""
        formatted = ' - '.join(message).strip()
        sys.stderr.write(f'# {formatted}\n')  # pragma: no cover

    @staticmethod
    def bail_out(*message: str) -> NoReturn:
        """Print a bail out message and exit."""
        print('Bail out!', *message, file=sys.stderr)
        sys.exit(1)

    @staticmethod
    @contextmanager
    def suppress() -> Generator[None, Any, None]:  # pragma: no cover
        """Suppress output from TAP Producers.

        Suppresses the following output to stderr:
        * ``warnings.warn``
        * ``TAP.bail_out``
        * ``TAP.diagnostic``

        and ALL output to stdout.

        :note:`Does not suppress Python exceptions.`
        """
        warnings.simplefilter('ignore')
        with Path(os.devnull).open('w') as null:
            with redirect_stdout(null):
                yield
        warnings.resetwarnings()

    @staticmethod
    @contextmanager
    def strict() -> Generator[None, Any, None]:  # pragma: no cover
        """Transform any ``warn()`` or ``TAP.not_ok()`` calls into Python errors.
        :note:`Implies non-TAP output`.
        """
        warnings.simplefilter('error', category=RuntimeWarning, append=True)
        yield
        warnings.resetwarnings()

    @classmethod
    def ok(cls: type[Self], *args: str, skip: bool = False) -> None:
        cls._count[OK] += 1
        cls._count[SKIP] += 1 if skip else 0
        directive = '-' if not skip else '# SKIP'
        formatted = ' - '.join(args).strip()
        sys.stdout.write(
            f'ok {cls._count.total() - cls._count[SKIP]} {directive} {formatted}\n',
        )

    @classmethod
    def not_ok(cls: type[Self], *args: str, skip: bool = False) -> None:
        cls._count[NOT_OK] += 1
        cls._count[SKIP] += 1 if skip else 0
        directive = '-' if not skip else '# SKIP'
        formatted = ' - '.join(args).strip()
        warnings.formatwarning = tap_warning_format
        warnings.showwarning = tap_warn  # type: ignore
        warnings.warn(
            f'{cls._count.total() - cls._count[SKIP]} {directive} {formatted}',
            RuntimeWarning,
            stacklevel=2,
        )
        warnings.formatwarning = cls._formatwarning  # pragma: no cover
        warnings.showwarning = cls._showwarning  # pragma: no cover
