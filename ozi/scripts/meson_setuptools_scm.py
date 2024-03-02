# noqa: INP001
# ozi/scripts/meson_setuptools_scm.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
# /// script
# requires-python = ">=3.10"
# dependencies = ['tomli>=2;python_version<="3.11"']  # noqa: E800
# [tool.setuptools_scm]  # noqa: E800
# version_file = "PKG-INFO"  # noqa: E800
# ///
""":pep:`723` script: deploy python PKG-INFO template for meson based on pyproject file.

Side-effects
^^^^^^^^^^^^

* in :envvar:`MESON_BUILD_ROOT` create
  ``tool.setuptools_scm:version_file`` from ``tool.setuptools_scm:version_file_template``
  found in the :file:`{MESON_BUILD_ROOT}/pyproject.toml`.

Environment Variables
^^^^^^^^^^^^^^^^^^^^^

* :envvar:`MESON_BUILD_ROOT`

``pyproject.toml`` Tool Table Variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ``tool.setuptools_scm:version_file``
* ``tool.setuptools_scm:version_file_template``

"""

import os
import sys
from pathlib import Path

if sys.version_info >= (3, 11):  # pragma: no cover
    import tomllib as toml
elif sys.version_info < (3, 11):  # pragma: no cover
    import tomli as toml

if __name__ == '__main__':
    source = '/' / Path(
        os.path.relpath(
            os.path.join('/', os.environ.get('MESON_BUILD_ROOT', os.path.relpath('..'))),
            '/',
        ),
    )
    with (source / 'pyproject.toml').open('rb') as project_file:
        pyproject_toml = toml.load(project_file)
    setuptools_scm = pyproject_toml.get('tool', {}).get('setuptools_scm', {})
    path = Path(source / setuptools_scm.get('version_file')).resolve()
    if path.parent != Path(source).resolve():
        raise RuntimeError('Invalid version_file path in pyproject.toml')
    else:
        path.write_text(setuptools_scm.get('version_file_template'))
