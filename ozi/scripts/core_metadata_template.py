# noqa: INP001
# ozi/scripts/core_metadata_template.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""python template: check core metadata"""
import os
import pathlib

#
import tomli

# pylint: disable=consider-using-with
source = pathlib.Path(
    os.path.relpath(
        os.path.join('/', os.environ.get('MESON_SOURCE_ROOT', os.path.relpath('..'))),
        '/',
    ),
)
project_file = open(source / 'pyproject.toml', 'rb')
pyproject_toml = tomli.load(project_file)
project_file.close()
core_metadata = pyproject_toml.get('project', {'optional_dependencies': {}})
print(core_metadata.get('optional_dependencies', {'todo': []}).get('@0@', 'fail'))
