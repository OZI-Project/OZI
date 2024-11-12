# noqa: INP001
# ozi/scripts/meson_postconf_install_dependencies.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
# /// script
# requires-python = ">=3.10"
# dependencies = ['tomli>=2;python_version<="3.11"']
# ///
""":pep:`723` script: deploy python package build dependencies based on pyproject file.

Side-effects
^^^^^^^^^^^^

* None

Environment Variables
^^^^^^^^^^^^^^^^^^^^^

* :envvar:`MESON_BUILD_ROOT`
* :envvar:`MESON_DIST_ROOT`

``pyproject.toml`` Tool Table Variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ``project.dependencies``

"""
import os
import sys
from pathlib import Path

if sys.version_info >= (3, 11):  # pragma: no cover
    import tomllib as toml
elif sys.version_info < (3, 11):  # pragma: no cover
    import tomli as toml


if __name__ == '__main__':
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
    with (source / 'pyproject.toml').open('rb') as project_file:
        pyproject_toml = toml.load(project_file)
    dependencies = pyproject_toml.get('project', {}).get('dependencies', [])
    print('$$'.join(dependencies))
