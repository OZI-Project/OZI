# noqa: INP001
# ozi/scripts/meson_setuptools_scm.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""deploy python PKG-INFO template for meson based on pyproject file."""

import os
import sys
from pathlib import Path

if sys.version_info >= (3, 11):  # pragma: no cover
    import tomllib as toml
elif sys.version_info < (3, 11):  # pragma: no cover
    import tomli as toml

source = '/' / Path(
    os.path.relpath(
        os.path.join('/', os.environ.get('MESON_BUILD_ROOT', os.path.relpath('..'))),
        '/',
    ),
)
dist = '/' / Path(
    os.path.relpath(
        os.path.join('/', os.environ.get('MESON_DIST_ROOT', os.path.relpath('..'))),
        '/',
    ),
)
with (source / 'pyproject.toml').open('rb') as project_file:
    pyproject_toml = toml.load(project_file)
setuptools_scm = pyproject_toml.get('tool', {}).get('setuptools_scm', {})
Path(dist / setuptools_scm.get('version_file')).write_text(
    setuptools_scm.get('version_file_template')
)
