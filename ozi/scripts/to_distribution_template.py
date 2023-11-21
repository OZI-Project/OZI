# noqa: INP001
# ozi/scripts/to_distribution_template.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
from importlib.metadata import packages_distributions

print({v[0]: k for k, v in packages_distributions().items()}.get('@0@', '@0@'))
