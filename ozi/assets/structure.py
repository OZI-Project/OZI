# ozi/assets/structure.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Directory structure expected files"""
required_pkg_info = (
    'Name',
    'Version',
    'Metadata-Version',
    'Summary',
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
]
source_files = [
    'meson.build',
    '__init__.py',
    'py.typed',
]
test_files = [
    'meson.build',
]
