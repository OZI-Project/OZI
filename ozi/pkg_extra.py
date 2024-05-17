# ozi/pkg_extra.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Extra packaging metadata used by OZI."""
from __future__ import annotations

from email.message import Message
from typing import Any

from pyparsing import CaselessKeyword
from pyparsing import Combine
from pyparsing import Forward
from pyparsing import Keyword
from pyparsing import Literal
from pyparsing import ParseException
from pyparsing import ParseResults
from pyparsing import Suppress
from pyparsing import White
from pyparsing import oneOf

from ozi.spdx import spdx_license_expression

sspace = Suppress(White(' ', exact=1))
dcolon = sspace + Suppress(Literal('::')) + sspace
classifier = Suppress(White(' ', min=2)) + Suppress(Literal('Classifier:')) + sspace
pep639_headers = Forward()
pep639_headers_md = Forward()
license_expression = classifier + (
    Keyword('License-Expression')
    + dcolon
    + Combine(spdx_license_expression, join_string=' ')
).set_parse_action(lambda t: {str(t[0]): str(t[1])})
license_file = classifier + (
    Keyword('License-File') + dcolon + oneOf(['LICENSE', 'LICENSE.txt'])
).set_parse_action(lambda t: {str(t[0]): str(t[1])})
pep639_headers <<= license_expression + license_file
pep639_headers_md <<= (
    Suppress(
        Keyword('[comment]') + Literal('#') + Literal('('),
    )
    + license_expression
    + Suppress(Literal(')'))
    + Suppress(
        Keyword('[comment]') + Literal('#') + Literal('('),
    )
    + license_file
    + Suppress(Literal(')'))
)
extra_classifiers_comment = (
    Suppress(
        Keyword('..') + CaselessKeyword('ozi'),
    )
    + pep639_headers
    | Suppress(
        Keyword('[comment]')
        + Keyword('#')
        + Literal('(')
        + Keyword('..')
        + CaselessKeyword('ozi')
        + Literal(')'),
    )
    + pep639_headers_md
)


def _str_dict_union(toks: ParseResults) -> Any | ParseResults:
    """Parse-time union of dict[str, str]."""
    if len(toks) >= 2:
        return dict(toks[0]) | dict(toks[1])
    else:  # pragma: no cover
        return None


pep639_headers.set_parse_action(_str_dict_union).set_name('pep639')


def _pkg_info_extra(payload: str, as_message: bool = True) -> dict[str, str] | Message:
    """Extra PKG-INFO parsers."""
    extras: dict[str, str] = extra_classifiers_comment.parse_string(payload)[
        0
    ]  # pyright: ignore
    if as_message:
        msg = Message()
        for k, v in extras.items():
            msg.add_header('Classifier', f'{k} :: {v}')
        return msg
    return extras


def parse_extra_pkg_info(
    pkg_info: Message,
) -> tuple[dict[str, str], str | None]:
    """Get extra Classifiers tacked onto the PKG-INFO payload by OZI."""
    errstr = None
    try:
        extra_pkg_info = dict(
            _pkg_info_extra(str(pkg_info.get_payload())),
        )  # pyright: ignore
    except ParseException as e:  # pragma: defer to good-first-issue
        extra_pkg_info = {}
        newline = '\n'
        errstr = str(e).replace(newline, ' ')
    return extra_pkg_info, errstr
