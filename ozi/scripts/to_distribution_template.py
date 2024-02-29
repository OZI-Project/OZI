# noqa: INP001
# ozi/scripts/to_distribution_template.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
# /// script
# requires-python = ">=3.10"
# ///
from importlib.metadata import packages_distributions

if __name__ == '__main__':
    print({v[0]: k for k, v in packages_distributions().items()}.get('@0@', '@0@'))
