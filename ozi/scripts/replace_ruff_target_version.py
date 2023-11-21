# noqa: INP001
# ozi/scripts/core_metadata_template.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""python template: replace commented target-version in [tool.ruff]."""
import os
from pathlib import Path

build = '/' / Path(
    os.path.relpath(
        Path('/', os.environ.get('MESON_BUILD_ROOT', Path('..').relative_to('.'))),
        '/',
    ),
)
file = build / 'pyproject.toml.pre'
file.write_text(file.read_text().replace('# target-version', 'target-version'))
