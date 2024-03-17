# noqa: INP001
"""Unit and fuzz tests for ``ozi-new``."""
# Part of ozi.
# See LICENSE.txt in the project root for details.
from __future__ import annotations

import pytest

from ozi.tap import TAP  # pyright: ignore


def test_end_skip() -> None:  # noqa: DC102, RUF100
    with pytest.raises(SystemExit):
        TAP.end()
    TAP._count.clear()  # noqa: SLF001


def test_bail_out() -> None:  # noqa: DC102, RUF100
    with pytest.raises(SystemExit):
        TAP.bail_out()
    TAP._count.clear()  # noqa: SLF001


def test_end_skip_reason() -> None:  # noqa: DC102, RUF100
    with pytest.raises(SystemExit):
        TAP.end('reason')
    TAP._count.clear()  # noqa: SLF001


def test_producer_ok() -> None:  # noqa: DC102, RUF100
    TAP.ok('Producer passes')
    with pytest.raises(SystemExit):
        TAP.end()
    TAP._count.clear()  # noqa: SLF001


def test_producer_ok_skip_reason() -> None:  # noqa: DC102, RUF100
    TAP.ok('Producer passes')
    with pytest.raises(SystemExit):
        TAP.end('reason')
    TAP._count.clear()  # noqa: SLF001


def test_producer_skip_ok() -> None:  # noqa: DC102, RUF100
    TAP.ok('Producer passes', skip=True)
    with pytest.raises(SystemExit):
        TAP.end()
    TAP._count.clear()  # noqa: SLF001


def test_producer_skip_ok_with_reason() -> None:  # noqa: DC102, RUF100
    TAP.ok('Producer passes', skip=True)
    with pytest.raises(SystemExit):
        TAP.end('Skip pass reason.')
    TAP._count.clear()  # noqa: SLF001


def test_producer_not_ok() -> None:  # noqa: DC102, RUF100
    with pytest.raises(RuntimeWarning):
        TAP.not_ok('Producer fails')
    with pytest.raises(SystemExit):
        TAP.end()
    TAP._count.clear()  # noqa: SLF001


def test_producer_skip_not_ok() -> None:  # noqa: DC102, RUF100
    with pytest.raises(RuntimeWarning):
        TAP.not_ok('Producer fails', skip=True)
    with pytest.raises(SystemExit):
        TAP.end()
    TAP._count.clear()  # noqa: SLF001


def test_producer_skip_not_ok_with_reason() -> None:  # noqa: DC102, RUF100
    with pytest.raises(RuntimeWarning):
        TAP.not_ok('Producer fails', skip=True)
    with pytest.raises(SystemExit):
        TAP.end('Skip fail reason.')
    TAP._count.clear()  # noqa: SLF001
