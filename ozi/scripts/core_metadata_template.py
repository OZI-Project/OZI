# noqa: INP001
# ozi/scripts/core_metadata_template.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
# /// script
# requires-python = ">=3.10"
# dependencies = ['tomli>=2;python_version<="3.11"']  # noqa: E800
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

``pyproject.toml`` Project Variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ``project:optional_dependencies``

"""
import os
import pathlib
import sys

if sys.version_info >= (3, 11):  # pragma: no cover
    import tomllib as toml
elif sys.version_info < (3, 11):  # pragma: no cover
    import tomli as toml

if __name__ == '__main__':
    # pylint: disable=consider-using-with
    source = pathlib.Path(
        os.path.relpath(
            os.path.join('/', os.environ.get('MESON_SOURCE_ROOT', os.path.relpath('..'))),
            '/',
        ),
    )
    project_file = open(source / 'pyproject.toml', 'rb')
    pyproject_toml = toml.load(project_file)
    project_file.close()
    core_metadata = pyproject_toml.get('project', {'optional_dependencies': {}})
    print(core_metadata.get('optional_dependencies', {'todo': []}).get('@0@', 'fail'))
