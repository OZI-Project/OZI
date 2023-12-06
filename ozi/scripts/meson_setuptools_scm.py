# noqa: INP001
# ozi/scripts/meson_setuptools_scm.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""deploy python PKG-INFO template for meson based on pyproject file."""

import os
from pathlib import Path

try:
    import toml
except ModuleNotFoundError:
    import tomli as toml

source = '/' / Path(
    os.path.relpath(
        os.path.join('/', os.environ.get('MESON_BUILD_ROOT', os.path.relpath('..'))),
        '/',
    ),
)
project_file = (source / 'pyproject.toml.ozi').open()
pyproject_toml = toml.loads(project_file.read())
project_file.close()
setuptools_scm = pyproject_toml.get('tool', {}).get('setuptools_scm', {})
Path(source / setuptools_scm.get('write_to')).write_text(
    setuptools_scm.get('write_to_template')
)
