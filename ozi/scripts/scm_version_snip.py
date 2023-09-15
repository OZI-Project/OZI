# noqa: INP001
# ozi/scripts/scm_version_snip.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""python snippet: grab version info"""
from setuptools_scm import get_version  # type: ignore

print(get_version(normalize=False))
