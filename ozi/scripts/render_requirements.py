# noqa: INP001
# ozi/scripts/render_requirements.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
# /// script
# requires-python = ">=3.10"
# ///
""":pep:`723` script: render OZI-style ``requirements.in`` as ``PKG-INFO`` headers.

Output
^^^^^^

* ``Requires-Dist`` headers for the :file:`{PWD}/requirements.in`

Environment Variables
^^^^^^^^^^^^^^^^^^^^^

* :envvar:`PWD`


"""
import pathlib

if __name__ == '__main__':
    requirements = (
        r.partition('\u0023')[0]
        for r in filter(
            lambda r: not (r.startswith('\u0023') or r == ''),
            pathlib.Path('./requirements.in').read_text('utf-8').splitlines(),
        )
    )
    for req in requirements:
        if len(req) > 0:
            print(f'Requires-Dist: {req}')
