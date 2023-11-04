# ozi/assets/structure.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Directory structure expected files"""
required_pkg_info = (
    'Description-Content-Type',
    'Home-page',
    'Metadata-Version',
    'Name',
    'Summary',
    'Version',
)
root_dirs = ['tests' 'subprojects']
root_files = [
    'README.rst',
    '.gitignore',
    'pyproject.toml',
    'meson.build',
    'meson.options',
    'LICENSE.txt',
    'PKG-INFO',
    'requirements.in',
    'CHANGELOG.md',
]
source_files = [
    'meson.build',
    '__init__.pyi',
    '__init__.py',
    'py.typed',
]
test_files = [
    'meson.build',
]
