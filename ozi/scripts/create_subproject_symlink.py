# noqa: INP001
# ozi/scripts/create_subproject_symlink.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
# /// script
# requires-python = ">=3.10"
# dependencies = [
# 'pathvalidate~=3.2',
# ]
# ///
""":pep:`723` script: create symbolic link to subproject

Side-effects
^^^^^^^^^^^^

* Create symbolic link :file:`{MESON_BUILD_ROOT}/subprojects/ozi` to the
  versioned OZI wrap directory.

Environment Variables
^^^^^^^^^^^^^^^^^^^^^

* :envvar:`MESON_BUILD_ROOT`


"""
import os
import pathlib
import sys
from contextlib import suppress
from glob import glob

from pathvalidate import validate_filepath

if __name__ == '__main__':
    if sys.platform == 'win32':
        source = pathlib.Path(os.environ.get('MESON_BUILD_ROOT'))
    else:
        source = pathlib.Path(
            os.path.relpath(
                os.path.join('/', os.environ.get('MESON_BUILD_ROOT', os.path.relpath('..'))),
                '/',
            ),
        )
    validate_filepath(source)
    try:
        target = pathlib.Path(glob('subprojects/OZI-*', root_dir='/' / source)[0])
    except IndexError:
        print('OZI subproject directory not found', file=sys.stderr)
        exit(0)
    with suppress(FileExistsError):
        ('/' / source / 'subprojects' / 'ozi').symlink_to(
            '/' / source / target,
            target_is_directory=True,
        )
