# noqa: INP001
# ozi/scripts/get_optional_dependencies.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
# /// script
# requires-python = ">=3.10"
# dependencies = [
# 'tomli>=2;python_version<="3.11"',
# 'pathvalidate~=3.2',
# ]
# ///
""":pep:`723` script template: check OZI core dependency metadata

Input
^^^^^

#. Key name to match in ``project:optional_dependencies`` table

Output
^^^^^^

* String representation of matched value(s) for a key.

Environment Variables
^^^^^^^^^^^^^^^^^^^^^

* :envvar:`MESON_SOURCE_ROOT`

``pyproject.toml`` Keys
^^^^^^^^^^^^^^^^^^^^^^^

* ``project.optional-dependencies``

"""
import os
import pathlib
import sys

from pathvalidate import validate_filepath

if sys.version_info >= (3, 11):  # pragma: no cover
    import tomllib as toml
elif sys.version_info < (3, 11):  # pragma: no cover
    import tomli as toml

if __name__ == '__main__':
    # pylint: disable=consider-using-with
    if sys.platform == 'win32':
        source = pathlib.Path(os.environ.get('MESON_SOURCE_ROOT'))
    else:
        source = pathlib.Path(
            os.path.relpath(
                os.path.join(
                    '/', os.environ.get('MESON_SOURCE_ROOT', os.path.relpath('..'))
                ),
                '/',
            ),
        )
    validate_filepath(source, platform='auto')
    with open(source / 'pyproject.toml', 'rb') as fp:
        pyproject_toml = toml.load(fp)
    metadata = pyproject_toml.get('project', {'optional-dependencies': {}})
    print(*metadata.get('optional-dependencies', {'todo': []}).get('@0@', []), sep='$$')
