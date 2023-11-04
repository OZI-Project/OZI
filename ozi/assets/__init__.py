# ozi/assets/__init__.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Asset files for python packaging."""
import argparse
import platform
import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from difflib import get_close_matches
from typing import Any, List, Optional, Sequence, Union
from warnings import warn

from pyparsing import Forward, Keyword, Literal, ZeroOrMore, oneOf
from spdx_license_list import LICENSES  # type: ignore

# pyright: reportMissingImports = false
from trove_classifiers import classifiers

required_pkg_info_patterns = (
    'Name',
    'Version',
    'Metadata-Version',
    'Summary',
    'Home-page',
    'License-Expression',
    'License-File',
    'Programming Language :: Python',
    'Description-Content-Type',
)
metadata_version = '2.1'
implementation_support = ('CPython',)
specification_version = '0.1'
__pymajor, __pyminor, __pypatch = map(int, platform.python_version_tuple())

minor_deprecation = {
    8: date(2024, 10, 1),
    9: date(2025, 10, 1),
    10: date(2026, 10, 1),
    11: date(2027, 10, 1),
    12: date(2028, 10, 1),
    13: date(2029, 10, 1),
}
python3_eol = minor_deprecation.get(__pyminor, date(2008, 12, 3))
current_date = datetime.now(tz=timezone.utc).date()
ozi_support_eol = python3_eol - timedelta(weeks=104)
if current_date > python3_eol:  # pragma: no cover
    raise RuntimeError(
        f'Python {__pymajor}.{__pyminor}.{__pypatch} is not supported as of {python3_eol}.'
    )
elif current_date > ozi_support_eol:  # pragma: no cover
    warn(
        f'Python {__pymajor}.{__pyminor}.{__pypatch} support is deprecated as of {ozi_support_eol}.',
        DeprecationWarning,
    )


@dataclass(frozen=True)
class __PythonSupport:
    """Datatype for OZI Python version support."""

    major: int
    bugfix1: int
    bugfix2: int
    security: int


def __python_support_versions(date: date) -> __PythonSupport:
    """Get the currently supported Python versions from the schedule."""
    return __PythonSupport(
        3,
        *sorted(
            [k for k, v in minor_deprecation.items() if v - timedelta(weeks=104) > date]
        )[:3],
    )


python_support = __python_support_versions(current_date)
python_support_required = {
    ('Classifier', f'Programming Language :: Python :: {str(python_support.major)} :: Only'),
    (
        'Classifier',
        'Programming Language :: Python :: '
        f'{str(python_support.major)}.{str(python_support.security)}',
    ),
    (
        'Classifier',
        'Programming Language :: Python :: '
        f'{str(python_support.major)}.{str(python_support.bugfix2)}',
    ),
    (
        'Classifier',
        'Programming Language :: Python :: '
        f'{str(python_support.major)}.{str(python_support.bugfix1)}',
    ),
}

pep639_spdx = [
    'LicenseRef-Public-Domain',
    'LicenseRef-Proprietary',
]
spdx_exceptions = [
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
]

ambiguous_licenses = [
    'Private',
    'DFSG approved',
    'OSI Approved :: Academic Free License (AFL)',
    'OSI Approved :: Apache Software License',
    'OSI Approved :: Apple Public Source License',
    'OSI Approved :: Artistic License',
    'OSI Approved :: BSD License',
    'OSI Approved :: GNU Affero General Public License v3',
    'OSI Approved :: GNU Free Documentation License (FDL)',
    'OSI Approved :: GNU General Public License (GPL)',
    'OSI Approved :: GNU General Public License v2 (GPLv2)',
    'OSI Approved :: GNU General Public License v3 (GPLv3)',
    'OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
    'OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
    'OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
    'OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
    'Public Domain',
]
spdx_disambiguation = [
    ('LicenseRef-Proprietary',),
    (
        'AGPL-3.0-only',
        'AGPL-3.0-or-later',
        'Apache-2.0',
        'Artistic-2.0',
        'BSD-3-Clause',
        'CC-BY-4.0',
        'CC-BY-SA-4.0',
        'EPL-1.0',
        'GPL-2.0-only',
        'GPL-2.0-or-later',
        'GPL-3.0-only',
        'GPL-3.0-or-later',
        'ISC',
        'LGPL-2.1-or-later',
        'LGPL-3.0-only',
        'LGPL-3.0-or-later',
        'MIT',
        'OFL-1.1',
        'WTFPL',
        'Zlib',
    ),
    ('AFL-3.0',),
    ('Apache-2.0',),
    ('APSL-1.0', 'APSL-1.1', 'APSL-1.2', 'APSL-2.0'),
    ('Artistic-2.0',),
    ('0BSD', 'BSD-2-Clause', 'BSD-3-Clause', 'BSD-3-Clause-Clear', 'BSD-4-Clause'),
    ('AGPL-3.0-only', 'AGPL-3.0-or-later'),
    ('GFDL-1.3-only', 'GFDL-1.3-or-later'),
    ('GPL-2.0-only', 'GPL-2.0-or-later', 'GPL-3.0-only', 'GPL-3.0-or-later'),
    ('GPL-2.0-only', 'GPL-2.0-or-later'),
    ('GPL-3.0-only', 'GPL-3.0-or-later'),
    ('LGPL-2.0-only',),
    ('LGPL-2.1-or-later',),
    ('LGPL-3.0-only', 'LGPL-3.0-or-later'),
    ('LGPL-2.1-or-later', 'LGPL-3.0-only', 'LGPL-3.0-or-later'),
    ('LicenseRef-Public-Domain', 'CC0-1.0', 'Unlicense'),
]
spdx_options = dict(zip(ambiguous_licenses, spdx_disambiguation))
spdx_license_expression = Forward()
spdx_license_expression <<= oneOf(
    (pep639_spdx + [lic.id for lic in LICENSES.values() if not lic.deprecated_id])
).set_name('License-ID') + ZeroOrMore(
    (
        Keyword('WITH') + oneOf(spdx_exceptions).set_name('License-Exception-ID')
        | Keyword('AND') + spdx_license_expression
        | Keyword('OR') + spdx_license_expression
    )
) | Literal(
    '('
) + spdx_license_expression + Literal(
    ')'
)
top4 = [
    'MIT License',
    'BSD License',
    'GNU General Public License v3',
    'Apache Software License',
]
framework_prefix = 'Framework :: '
environment_prefix = 'Environment :: '
audience_prefix = 'Intended Audience :: '
status_prefix = 'Development Status :: '
language_prefix = 'Natural Language :: '
license_prefix = 'License :: '
topic_prefix = 'Topic :: '
root_templates = [
    '.gitignore',
    'meson.build',
    'meson.options',
    'PKG-INFO',
    'pyproject.toml',
    'README.rst',
    'LICENSE.txt',
    'requirements.in',
    'CHANGELOG.md',
]
source_templates = [
    'project.name/__init__.py',
    'project.name/__init__.pyi',
    'project.name/meson.build',
    'project.name/py.typed',
]
test_templates = [
    'tests/meson.build',
]
ci_provider_templates = ['github_workflows/ozi.yml']
new_module_templates = ['project.name/new_module.py']
new_test_templates = ['tests/new_test.py']


class CloseMatch(argparse.Action):
    """Special choices action. Warn the user if a close match could not be found."""

    audience = [
        i[len(audience_prefix) :].lstrip()
        for i in classifiers
        if i.startswith(audience_prefix)
    ]
    language = [
        i[len(language_prefix) :].lstrip()
        for i in classifiers
        if i.startswith(language_prefix)
    ]
    framework = [
        i[len(framework_prefix) :].lstrip()
        for i in classifiers
        if i.startswith(framework_prefix)
    ]
    environment = [
        i[len(environment_prefix) :].lstrip()
        for i in classifiers
        if i.startswith(environment_prefix)
    ]
    license = [
        i[len(license_prefix) :].lstrip()
        for i in classifiers
        if i.startswith(license_prefix)
    ]
    license_id = [k for k, v in LICENSES.items() if v.deprecated_id is False]
    license_exception_id = spdx_exceptions
    status = [
        i[len(status_prefix) :].lstrip() for i in classifiers if i.startswith(status_prefix)
    ]
    topic = [
        i[len(topic_prefix) :].lstrip() for i in classifiers if i.startswith(topic_prefix)
    ]

    def __init__(
        self: argparse.Action,
        option_strings: List[str],
        dest: str,
        nargs: Union[int, str, None] = None,
        **kwargs: Any,
    ) -> None:
        """argparse init"""
        if nargs not in [None, '?']:
            raise ValueError('nargs (other than "?") not allowed')

        super().__init__(option_strings, dest, nargs=nargs, **kwargs)  # type: ignore

    def close_matches(
        self: argparse.Action, key: str, value: Sequence[str]
    ) -> Sequence[str]:
        """Get a single close match for a class attribute."""
        if value is None:
            return []  # pragma: defer to good-first-issue
        try:
            value = get_close_matches(value, self.__getattribute__(key), cutoff=0.40)[0]
        except (IndexError, AttributeError):
            warn(
                f'No {key} choice matching "{value}" available.'
                'To list available options:'
                f'$ ozi-new -l {key}',
                RuntimeWarning,
            )
        return value

    def __call__(
        self: argparse.Action,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[str], None],
        option_string: Union[str, None] = None,
    ) -> None:
        """Action business logic."""
        if values is None:
            return
        if option_string is not None:
            key = option_string.lstrip('-').replace('-', '_')
        else:
            key = ''  # pragma: defer to good-first-issue

        if self.nargs == '?':
            matches: List[str] = []
            for v in values:
                v = self.close_matches(key, v)  # type: ignore
                matches += v
            setattr(namespace, self.dest, matches)
        else:
            values = self.close_matches(key, values)  # type: ignore
            setattr(namespace, self.dest, values)


def underscorify(s: str) -> str:
    """Filter to replace non-alphanumerics with underscores."""
    return re.sub('[^0-9a-zA-Z]', '_', s)


def wheel_repr(version: str) -> str:
    """Filter to transform versions of the form "X.Y" into "pyXY"."""
    major, minor = version.split('.')
    return f'py{major}{minor}'


def tap_warning_format(
    msg: str, category: type[Warning], filename: str, lineno: int, line: Optional[str] = None
) -> str:
    """Test Anything Protocol formatted warnings."""
    return f'# {filename}:{lineno}: {category.__name__}\nnot ok - {msg}\n'
