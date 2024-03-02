# noqa: INP001
# ozi/scripts/version_metadata_template.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
# /// script
# requires-python = ">=3.10"
# ///
""":pep:`723` template script: check installed Python package version.

Input
^^^^^

#. Name of an installed package to check.

Output
^^^^^^

* String representation of the current version for a package.

"""
from importlib.metadata import version

if __name__ == '__main__':
    print(version('@0@'))
