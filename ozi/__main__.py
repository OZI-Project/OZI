# ozi/__main__.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""``ozi`` console application."""  # pragma: no cover

from ozi_core.__main__ import main as ozi_main  # pyright: ignore
from ozi_core.__main__ import setup_parser  # pyright: ignore

from ozi import __version__

parser = setup_parser(__version__)  # type: ignore


def main() -> None:
    setup_parser(__version__)
    ozi_main()  # pyright: ignore
