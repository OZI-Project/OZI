# ozi/spdx.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""SPDX standard metadata parser expression grammars, with support for :pep:`639` keys."""
from ozi_spec import METADATA  # pyright: ignore
from pyparsing import Combine
from pyparsing import Forward
from pyparsing import Keyword
from pyparsing import Literal
from pyparsing import MatchFirst
from pyparsing import Optional
from pyparsing import Word
from pyparsing import ZeroOrMore
from pyparsing import alphanums
from pyparsing import oneOf
from spdx_license_list import LICENSES

user_defined_license = Combine(
    Optional('DocumentRef-' + Word(alphanums + '-.') + ':')
    + 'LicenseRef-'
    + Word(alphanums + '-.'),
)
spdx_license_expression = Forward()
spdx_license_expression <<= MatchFirst(
    [
        user_defined_license,
    ]
    + [Literal(lic.id) for lic in LICENSES.values() if not lic.deprecated_id],
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
