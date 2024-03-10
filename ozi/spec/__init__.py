# ozi/spec/__init__.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Specification API for OZI Metadata."""
from ozi.spec._spec import Metadata
from ozi.spec._spec import PythonSupport
from ozi.spec._spec import current_version
from ozi.spec.pkg import License

__all__ = ('current_version', 'License', 'Metadata', 'PythonSupport')