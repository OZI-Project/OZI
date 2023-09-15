# noqa: INP001
# ozi/scripts/sync_pkg_readme.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Check if the README.rst file is synchronized with PKG-INFO."""
import difflib
import email
import os
import pathlib
import sys

try:
    import toml  # type: ignore
except ImportError:
    import tomli as toml  # noqa: F401
# pylint: disable=consider-using-with
source = '/' / pathlib.Path(
    os.path.relpath(
        os.path.join('/', os.environ.get('MESON_SOURCE_ROOT', os.path.relpath('..'))), '/'
    )
)
pkg_info_file = open(source / 'PKG-INFO', 'r', encoding='utf-8')
pkg_info = email.message_from_file(pkg_info_file).get_payload()
pkg_info_file.close()
readme_file = open(source / 'README.rst', 'r', encoding='utf-8')
readme = readme_file.read()
readme_file.close()
project_file = open(source / 'pyproject.toml', 'r', encoding='utf-8')
pyproject_toml = toml.loads(project_file.read())
project_file.close()
setuptools_scm = pyproject_toml.get('tool', {}).get('setuptools_scm', {})
write_to_template = email.message_from_string(
    setuptools_scm.get('write_to_template', '')
).get_payload()
DIFF1 = str().join(
    difflib.context_diff(pkg_info, readme, tofile='PKG-INFO', fromfile='README.rst')
)
DIFF2 = str().join(
    difflib.context_diff(
        readme, write_to_template, tofile='pyproject.toml', fromfile='README.rst'
    )
)
DIFF3 = str().join(
    difflib.context_diff(
        write_to_template, pkg_info, tofile='pyproject.toml', fromfile='PKG-INFO'
    )
)
if DIFF1 != '':
    print(DIFF1)
    sys.exit(len(DIFF1))
elif DIFF2 != '':
    print(DIFF2)
    sys.exit(len(DIFF2))
elif DIFF3 != '':
    print(DIFF3)
    sys.exit(len(DIFF3))
