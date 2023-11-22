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

from email_validator import EmailNotValidError
from email_validator import EmailSyntaxError
from email_validator import validate_email
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

exceptions = (
    '389-exception',
    'Asterisk-exception',
    'Autoconf-exception-2.0',
    'Autoconf-exception-3.0',
    'Autoconf-exception-generic',
    'Autoconf-exception-macro',
    'Bison-exception-2.2',
    'Bootloader-exception',
    'Classpath-exception-2.0',
    'CLISP-exception-2.0',
    'cryptsetup-OpenSSL-exception',
    'DigiRule-FOSS-exception',
    'eCos-exception-2.0',
    'Fawkes-Runtime-exception',
    'FLTK-exception',
    'Font-exception-2.0',
    'freertos-exception-2.0',
    'GCC-exception-2.0',
    'GCC-exception-3.1',
    'GNAT-exception',
    'gnu-javamail-exception',
    'GPL-3.0-interface-exception',
    'GPL-3.0-linking-exception',
    'GPL-3.0-linking-source-exception',
    'GPL-CC-1.0',
    'GStreamer-exception-2005',
    'GStreamer-exception-2008',
    'i2p-gpl-java-exception',
    'KiCad-libraries-exception',
    'LGPL-3.0-linking-exception',
    'libpri-OpenH323-exception',
    'Libtool-exception',
    'Linux-syscall-note',
    'LLGPL',
    'LLVM-exception',
    'LZMA-exception',
    'mif-exception',
    'OCaml-LGPL-linking-exception',
    'OCCT-exception-1.0',
    'OpenJDK-assembly-exception-1.0',
    'openvpn-openssl-exception',
    'PS-or-PDF-font-exception-20170817',
    'QPL-1.0-INRIA-2004-exception',
    'Qt-GPL-exception-1.0',
    'Qt-LGPL-exception-1.1',
    'Qwt-exception-1.0',
    'SHL-2.0',
    'SHL-2.1',
    'SWI-exception',
    'Swift-exception',
    'u-boot-exception-2.0',
    'Universal-FOSS-exception-1.0',
    'vsftpd-openssl-exception',
    'WxWindows-exception-3.1',
    'x11vnc-openssl-exception',
)
pep639_spdx = [
    'LicenseRef-Public-Domain',
    'LicenseRef-Proprietary',
]
spdx_license_expression = Forward()
spdx_license_expression <<= oneOf(
    pep639_spdx + [lic.id for lic in LICENSES.values() if not lic.deprecated_id],
).set_name('License-ID') + ZeroOrMore(
    Keyword('WITH') + oneOf(exceptions).set_name('License-Exception-ID')
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


def parse_email(
    author_email: list[str],
    maintainer_email: list[str],
    verify: bool,
) -> tuple[list[str], list[str]]:
    _author_email = []
    _maintainer_email = []
    for email in set(author_email).union(maintainer_email):
        try:
            emailinfo = validate_email(email, check_deliverability=verify)
            email_normalized = emailinfo.normalized
            if email in author_email:
                _author_email += [email_normalized]
            if email in maintainer_email:
                _maintainer_email += [email_normalized]
            print('ok', '-', 'Author-Email')
        except (EmailNotValidError, EmailSyntaxError) as e:
            warn(str(e), RuntimeWarning, stacklevel=0)
    return _author_email, _maintainer_email


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
