"""Asset files for python packaging."""
import argparse
from difflib import get_close_matches
import re
from typing import Any, NoReturn, Sequence, Union
from warnings import warn

from trove_classifiers import classifiers  # type: ignore
from spdx_license_list import LICENSES  # type: ignore

ambiguous_licenses = [
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
        'Zlib'
    ),
    ('AFL-3.0',),
    ('Apache-2.0',),
    (),
    ('Artistic-2.0',),
    ('0BSD', 'BSD-2-Clause', 'BSD-3-Clause', 'BSD-3-Clause-Clear', 'BSD-4-Clause'),
    ('AGPL-3.0-only', 'AGPL-3.0-or-later'),
    ('GFDL-1.3-only', 'GFDL-1.3-or-later'),
    ('GPL-2.0-only', 'GPL-2.0-or-later', 'GPL-3.0-only', 'GPL-3.0-or-later'),
    ('GPL-2.0-only', 'GPL-2.0-or-later'),
    ('GPL-3.0-only', 'GPL-3.0-or-later'),
    (),
    ('LGPL-2.1-or-later',),
    ('LGPL-3.0-only', 'LGPL-3.0-or-later'),
    ('LGPL-2.1-or-later', 'LGPL-3.0-only', 'LGPL-3.0-or-later'),
    ('CC0-1.0', 'Unlicense')
]
spdx_options = dict(zip(ambiguous_licenses, spdx_disambiguation))
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
    'NOTICE',
    'LICENSE.txt'
]
source_templates = [
    'project.name/__init__.py',
    'project.name/meson.build',
]
test_templates = [
    'tests/meson.build',
]
ci_provider_templates = [
    'github_workflows/ozi.yml'
]


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
    license_spdx = [k for k, v in LICENSES.items() if v.deprecated_id is False]
    status = [
        i[len(status_prefix) :].lstrip()
        for i in classifiers
        if i.startswith(status_prefix)
    ]
    topic = [
        i[len(topic_prefix) :].lstrip()
        for i in classifiers
        if i.startswith(topic_prefix)
    ]

    def __init__(
        self: argparse.Action,
        option_strings,  # noqa: ANN001
        dest,  # noqa: ANN001
        nargs=None,  # noqa: ANN001
        **kwargs,  # noqa: ANN003
    ) -> None:
        """argparse init"""
        if nargs is not None:
            raise ValueError('nargs not allowed')

        super().__init__(option_strings, dest, **kwargs)

    def __call__(
        self: argparse.Action,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Union[str, None] = None,
    ) -> None:
        """Action business logic."""
        if option_string is not None:
            key = option_string.lstrip('-').replace('-', '_')
        else:
            key = ''
        if values is None:
            values = ''
        try:
            values = get_close_matches(values, self.__getattribute__(key), cutoff=0.40)[0]
        except IndexError:
            warn(
                '\n'.join(
                    [
                        f'No {key} choice matching "{values}" available.',
                        'To list available options:',
                        f'$ ozi-new -l {key}',
                    ]
                ),
                RuntimeWarning,
            )
        setattr(namespace, self.dest, values)


def underscorify(s: str) -> str:
    """Filter to replace non-alphanumerics with underscores."""
    return re.sub('[^0-9a-zA-Z]', '_', s)


def strict_warn(msg: str, category: type[Warning], strict: bool) -> Union[None, NoReturn]:
    """Warn or raise with a flag argument."""
    if strict:
        raise category(msg)
    else:
        warn('\n'.join(msg), category)
