# noqa: INP001
# ozi/scripts/version_metadata_template.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""python template: check package version"""
from importlib.metadata import version

print(version('@0@'))
