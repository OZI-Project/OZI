# noqa: INP001
# ozi/scripts/scm_version_snip.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
# /// script
# requires-python = ">=3.10"
# dependencies = ["setuptools_scm"]  # noqa: E800
# ///
"""python snippet: grab version info

Output
^^^^^^

* String representation of the current :emphasis:`non-normalized` project version

``pyproject.toml`` Tool Table Variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ``tool.setuptools_scm:...`` (fully configured)

"""
from setuptools_scm import get_version  # type: ignore

if __name__ == '__main__':
    print(get_version(normalize=False))
