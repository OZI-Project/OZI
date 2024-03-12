# ozi/spdx.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""SPDX standard metadata parser expression grammars, with support for :pep:`639` keys."""
from pyparsing import Forward
from pyparsing import Keyword
from pyparsing import Literal
from pyparsing import ZeroOrMore
from pyparsing import oneOf
from spdx_license_list import LICENSES

from ozi.spec import METADATA

spdx_license_expression = Forward()
spdx_license_expression <<= oneOf(
    [
        'LicenseRef-Public-Domain',
        'LicenseRef-Proprietary',
    ]
    + [lic.id for lic in LICENSES.values() if not lic.deprecated_id],
).set_name('License-ID') + ZeroOrMore(
    Keyword('WITH')
    + oneOf(METADATA.spec.python.pkg.license.exceptions).set_name('License-Exception-ID')
    | Keyword('AND') + spdx_license_expression
    | Keyword('OR') + spdx_license_expression,
) | Literal(
    '(',
) + spdx_license_expression + Literal(
    ')',
)
