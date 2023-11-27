# ozi/assets.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Assets for python packaging metadata."""
from __future__ import annotations

import gc
import sys
from contextlib import contextmanager
from contextlib import redirect_stderr
from contextlib import redirect_stdout
from contextlib import suppress
from runpy import run_module
from typing import Generator


@contextmanager
def redirect_argv(*args: str) -> Generator[None, None, None]:  # pragma: no cover
    argv = sys.argv[:]
    sys.argv = list(args)
    yield
    sys.argv = argv


@contextmanager
def nogc() -> Generator[None, None, None]:  # pragma: no cover
    gc.freeze()
    if gc.isenabled():
        gc.disable()
    yield
    gc.unfreeze()
    gc.enable()
    gc.collect()


def run_utility(name: str, *args: str) -> None:  # pragma: no cover
    with nogc():
        with redirect_argv(name, *args):
            with redirect_stdout(None):
                with redirect_stderr(None):
                    with suppress(SystemExit):
                        run_module(name)
