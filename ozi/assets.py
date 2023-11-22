# ozi/assets.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Assets for python packaging metadata."""
from __future__ import annotations

import re
from email.message import Message
from typing import Any
from warnings import warn

from pyparsing import CaselessKeyword
from pyparsing import Combine
from pyparsing import Forward
from pyparsing import Keyword
from pyparsing import Literal
from pyparsing import ParseException
from pyparsing import ParseResults
from pyparsing import Regex
from pyparsing import Suppress
from pyparsing import White
from pyparsing import ZeroOrMore
from pyparsing import oneOf
from spdx_license_list import LICENSES

from ozi.spec import License

pep639_spdx = [
    'LicenseRef-Public-Domain',
    'LicenseRef-Proprietary',
]
spdx_license_expression = Forward()
spdx_license_expression <<= oneOf(
    pep639_spdx + [lic.id for lic in LICENSES.values() if not lic.deprecated_id],
).set_name('License-ID') + ZeroOrMore(
    Keyword('WITH') + oneOf(License().exceptions).set_name('License-Exception-ID')
    | Keyword('AND') + spdx_license_expression
    | Keyword('OR') + spdx_license_expression,
) | Literal(
    '(',
) + spdx_license_expression + Literal(
    ')',
)
sspace = Suppress(White(' ', exact=1))
dcolon = sspace + Suppress(Literal('::')) + sspace
classifier = Suppress(White(' ', min=2)) + Suppress(Literal('Classifier:')) + sspace
pep639_headers = Forward()
license_expression = classifier + (
    Keyword('License-Expression')
    + dcolon
    + Combine(spdx_license_expression, join_string=' ')
).set_parse_action(lambda t: {str(t[0]): str(t[1])})
license_file = classifier + (
    Keyword('License-File') + dcolon + oneOf(['LICENSE', 'LICENSE.txt'])
).set_parse_action(lambda t: {str(t[0]): str(t[1])})
pep639_headers <<= license_expression + license_file


def _str_dict_union(toks: ParseResults) -> Any | ParseResults:
    """Parse-time union of dict[str, str]."""
    if len(toks) >= 2:
        return dict(toks[0]) | dict(toks[1])
    else:  # pragma: no cover
        return None


pep639_parse = Suppress(
    Keyword('..') + CaselessKeyword('ozi'),
) + pep639_headers.set_parse_action(_str_dict_union).set_name('pep639')


def parse_spdx(expr: Any | ParseResults) -> Any | ParseResults:
    try:
        expr = Combine(
            spdx_license_expression,
            join_string=' ',
        ).parse_string(
            str(expr),
        )[0]
        print('ok', '-', 'License-Expression')
    except ParseException as e:
        warn(str(e).strip('\n'), RuntimeWarning, stacklevel=0)
    return expr


def parse_project_name(name: str | ParseResults) -> str | ParseResults:
    try:
        Regex('^([A-Z]|[A-Z][A-Z0-9._-]*[A-Z0-9])$', re.IGNORECASE).set_name(
            'Package-Index-Name',
        ).parse_string(str(name))
        print('ok', '-', 'Name')
    except ParseException as e:
        warn(str(e), RuntimeWarning, stacklevel=0)
    return name


def pkg_info_extra(payload: str, as_message: bool = True) -> dict[str, str] | Message:
    """Get extra PKG-INFO Classifiers tacked onto the payload by OZI."""
    pep639: dict[str, str] = pep639_parse.parse_string(payload)[0]  # pyright: ignore
    if as_message:
        msg = Message()
        for k, v in pep639.items():
            msg.add_header('Classifier', f'{k} :: {v}')
        return msg
    return pep639


def parse_extra_pkg_info(pkg_info: Message) -> tuple[dict[str, str], str | None]:
    errstr = None
    try:
        extra_pkg_info = dict(pkg_info_extra(pkg_info.get_payload()))
    except ParseException as e:  # pragma: defer to good-first-issue
        extra_pkg_info = {}
        newline = '\n'
        errstr = str(e).replace(newline, ' ')
    return extra_pkg_info, errstr
