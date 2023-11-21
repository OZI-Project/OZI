"""Core OZI packaging management plane module."""
# ozi/__init__.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
from .spec import current_version

__version__ = current_version()
__author__ = 'Ross J. Duff MSc'
__all__ = ('__version__', '__author__', '__doc__')
