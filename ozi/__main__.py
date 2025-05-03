# ozi/__main__.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""``ozi`` console application."""  # pragma: no cover

from ozi_core.__main__ import main  # pyright: ignore

from ozi import __version__

if __name__ == '__main__':
    main(__version__)
