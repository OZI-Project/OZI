# noqa: INP001
# ozi/scripts/create_subproject_symlink.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
# /// script
# requires-python = ">=3.9"
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
    build_root = os.environ.get('MESON_BUILD_ROOT', '..')
    source = pathlib.Path(build_root).resolve()
    validate_filepath(source, platform='auto')
    current_dir = os.getcwd()
    # chdir to the resolved absolute path
    os.chdir(source)
    try:
        matches = glob('subprojects/OZI-*')
        if not matches:
            raise IndexError
        target = pathlib.Path('..', matches[0])
        link_path = pathlib.Path('subprojects/ozi')
        with suppress(FileExistsError):
            link_path.symlink_to(
                target,
                target_is_directory=True,
            )
    except IndexError:
        sys.exit(print('OZI subproject directory not found', file=sys.stderr))
    finally:
        os.chdir(current_dir)
