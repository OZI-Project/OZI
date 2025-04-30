# noqa: INP001
# ozi/scripts/meson_dist_setuptools_scm.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
# /// script
# requires-python = ">=3.10"
# dependencies = [
# 'tomli>=2;python_version<="3.11"',
# 'pathvalidate~=3.2',
# ]
# [tool.setuptools_scm]
# version_file = "PKG-INFO"
# ///
""":pep:`723` script: deploy python PKG-INFO template for meson based on pyproject file.

Side-effects
^^^^^^^^^^^^

* in :envvar:`MESON_DIST_ROOT` create
  ``tool.setuptools_scm:version_file`` from ``tool.setuptools_scm:version_file_template``
  found in the :file:`{MESON_BUILD_ROOT}/pyproject.toml`.

Environment Variables
^^^^^^^^^^^^^^^^^^^^^

* :envvar:`MESON_BUILD_ROOT`
* :envvar:`MESON_DIST_ROOT`

``pyproject.toml`` Keys
^^^^^^^^^^^^^^^^^^^^^^^

* ``tool.setuptools_scm.version_file``
* ``tool.setuptools_scm.version_file_template``

"""

import os
import sys
from pathlib import Path

from pathvalidate import ValidationError
from pathvalidate import validate_filepath

if sys.version_info >= (3, 11):  # pragma: no cover
    import tomllib as toml
elif sys.version_info < (3, 11):  # pragma: no cover
    import tomli as toml

if __name__ == '__main__':  # noqa: C901

    if sys.platform == 'win32':
        source = Path(os.environ.get('MESON_BUILD_ROOT'))
        dist = Path(os.environ.get('MESON_DIST_ROOT'))
    else:
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
    validate_filepath(source, platform='auto')
    validate_filepath(dist, platform='auto')
    with (source / 'pyproject.toml').open('rb') as project_file:
        pyproject_toml = toml.load(project_file)
    setuptools_scm = pyproject_toml.get('tool', {}).get('setuptools_scm', {})
    try:
        version_file = setuptools_scm.get('version_file')
        validate_filepath(version_file, platform='auto')
        path = Path(source / version_file).resolve()
    except (TypeError, ValidationError):
        exit(0)
    validate_filepath(path, platform='auto')
    if path.exists():
        path.unlink()
    if path.parent != Path(dist).resolve():
        raise RuntimeError('Invalid version_file path in pyproject.toml')
    else:
        version_file_template = setuptools_scm.get('version_file_template')
        validate_filepath(version_file_template, platform='auto')
        path.write_text(version_file_template)
