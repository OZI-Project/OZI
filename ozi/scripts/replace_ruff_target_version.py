# noqa: INP001
# ozi/scripts/replace_ruff_target_version.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
# /// script
# requires-python = ">=3.10"\
# dependencies = ['pathvalidate~=3.2',]
# ///
""":pep:`723` script: replace commented target-version in [tool.ruff].

Side-effects
^^^^^^^^^^^^

* in :file:`{MESON_BUILD_ROOT}/pyproject.toml` uncomment ``tool.ruff:target-version = ...``

Environment Variables
^^^^^^^^^^^^^^^^^^^^^

* :envvar:`MESON_BUILD_ROOT`

``pyproject.toml`` Tool Table Variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ``tool.ruff:target-version``

"""
import os
import sys
from pathlib import Path

from pathvalidate import validate_filepath

if __name__ == '__main__':
    if sys.platform == 'win32':
        build = Path(os.environ.get('MESON_BUILD_ROOT'))
    else:
        build = '/' / Path(
            os.path.relpath(
                Path('/', os.environ.get('MESON_BUILD_ROOT', Path('..').relative_to('.'))),
                '/',
            ),
        )
    validate_filepath(build, platform='auto')
    file = build / 'pyproject.toml'
    file.write_text(file.read_text().replace('# target-version', 'target-version'))
