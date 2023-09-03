#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
"""quick-start OZI project creation script."""
import argparse
from datetime import datetime, timezone
from difflib import get_close_matches
from pathlib import Path
import re
import sys
from typing import NoReturn, Union
from urllib.parse import urlparse
from warnings import warn

from jinja2 import Environment, FileSystemLoader, select_autoescape
from spdx_license_list import LICENSES
from email_validator import validate_email, EmailNotValidError
from pyparsing import Regex, ParseException
from trove_classifiers import classifiers

ambiguous_licenses = [
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
]
top4 = [
    'MIT License',
    'BSD License',
    'GNU General Public License v3',
    'Apache Software License',
]
status_prefix = 'Development Status :: '
license_prefix = 'License :: '
topic_prefix = 'Topic :: '
root_templates = [
    '.gitignore',
    'meson.build',
    'meson.options',
    'PKG-INFO',
    'pyproject.toml',
    'README.rst',
]
source_templates = [
    'project.name/__init__.py',
    'project.name/__init__.pyi',
    'project.name/meson.build',
]
status = [
    i[len(status_prefix):].lstrip() for i in classifiers if i.startswith(status_prefix)
]
licenses = [
    i[len(license_prefix):].lstrip() for i in classifiers if i.startswith(license_prefix)
]
topic = [i[len(topic_prefix):].lstrip() for i in classifiers if i.startswith(topic_prefix)]
license_spdx = [k for k, v in LICENSES.items() if v.deprecated_id is False]


class CloseMatch(argparse.Action):
    """Special choices action. Warn the user if a close match could not be found."""

    license = licenses
    status = status
    topic = topic
    license_spdx = license_spdx

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
        values: str,
        option_string: str,
    ) -> None:
        """Action business logic."""
        key = option_string.lstrip('-').replace('-', '_')
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


env = Environment(
    loader=FileSystemLoader(['templates', 'templates/project.name']),
    autoescape=select_autoescape(),
    enable_async=True,
)
parser = argparse.ArgumentParser(
    prog='ozi-new', description=sys.modules[__name__].__doc__, add_help=False
)
subparser = parser.add_subparsers(help='project help')
project_parser = subparser.add_parser('project', add_help=False)
required = project_parser.add_argument_group('required')
required.add_argument('--name', type=str, help='name of project')
required.add_argument('--author', type=str, help='author of project')
required.add_argument('--email', type=str, help='valid author email')
required.add_argument('--summary', type=str, help='short summary')
required.add_argument('--homepage', type=str, help='homepage URL')
required.add_argument(
    '--license-spdx',
    type=str,
    metavar='ID e.g. MIT, BSD-2-Clause, GPL-3.0-or-later, Apache-2.0',
    help='SPDX short ID',
)
required.add_argument(
    '--license',
    type=str,
    metavar=f'LICENSE e.g. {", ".join(top4)}',
    help='license classifier',
    action=CloseMatch,
)
required.add_argument(
    'target',
    type=str,
    help='target directory for new project',
)
email = project_parser.add_argument_group('email options')
email.add_argument(
    '--verify-email',
    default='--verify-email',
    action=argparse.BooleanOptionalAction,
    help='email domain deliverability check',
)
defaults = project_parser.add_argument_group('defaults')
defaults.add_argument(
    '--copyright-head',
    type=str,
    default='',
    help='copyright header string',
    metavar='COPYRIGHT_HEAD="Copyright {year}, {author}\\nSee LICENSE..."',
)
defaults.add_argument(
    '--ci-provider',
    type=str,
    default='github',
    choices=('github',),
    help='continuous integration and release provider',
)
project_output = project_parser.add_mutually_exclusive_group()
project_output.add_argument(
    '-h', '--help', action='help', help='show this help message and exit'
)

defaults.add_argument(
    '--topic',
    choices=topic,
    default='Utilities',
    help='Python package topic',
    metavar='TOPIC="Utilities"',
    type=str,
)
defaults.add_argument(
    '--status',
    choices=status,
    default='1 - Planning',
    help='Python package status',
    metavar='STATUS="1 - Planning"',
    type=str,
)
output = parser.add_mutually_exclusive_group()
output.add_argument('-h', '--help', action='help', help='show this help message and exit')
output.add_argument(
    '-l',
    '--list',
    type=str,
    choices=['license', 'license-spdx', 'status', 'topic'],
    help='list valid option settings and exit',
)


def main() -> Union[NoReturn, None]:
    """Main ozi.new entrypoint."""
    project = parser.parse_args()
    if project.list == 'license':
        print(*sorted((i for i in licenses)), sep='\n')
        exit(0)
    if project.list == 'license-spdx':
        print(
            *sorted((k for k, v in LICENSES.items() if v.deprecated_id is False)),
            sep='\n'
        )
        exit(0)
    if project.list == 'status':
        print(*sorted((i for i in status)), sep='\n')
        exit(0)
    if project.list == 'topic':
        print(*sorted(i for i in topic), sep='\n')
        exit(0)

    if 'project' not in project:
        parser.print_help()
        exit(0)

    year = datetime.now(tz=datetime.now(timezone.utc).astimezone().tzinfo).year
    if len(project.copyright_head) == 0:
        project.copyright_head = '\n'.join(
            [
                f'Copyright {year}, {project.author}',
                'See LICENSE.txt in the project root for details.',
            ]
        )
    else:
        project.copyright_head = project.copyright_head.format(
            year=year, author=project.author
        )

    if project.license in ambiguous_licenses:
        msg = [
            f'Ambiguous License string per PEP 639: {project.licenses}',
            'See also: https://github.com/pypa/trove-classifiers/issues/17',
            'This will need updated when PEP 639 is implemented.',
        ]
        warn('\n'.join(msg), PendingDeprecationWarning)

    if len(project.summary) > 512:
        warn('Project summary exceeds 512 characters (PyPI limit).', RuntimeWarning)

    try:
        emailinfo = validate_email(
            project.email, check_deliverability=(~project.no_verify_email)
        )
        project.email = emailinfo.normalized
    except EmailNotValidError as e:
        warn(f'{str(e)}\nInvalid maintainer email format or domain unreachable.', RuntimeWarning)

    try:
        Regex('^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$', re.IGNORECASE).parse_string(
            project.name
        )
    except ParseException as e:
        warn(f'{str(e)}\nInvalid project name.', RuntimeWarning)

    home_url = urlparse(project.homepage).geturl
    if home_url.scheme != 'https':
        warn('Homepage url scheme unsupported.', RuntimeWarning)

    if home_url.netloc == '':
        warn('Homepage url netloc cound not be parsed.', RuntimeWarning)

    project.name = re.sub(r'[-_.]+', '-', project.name).lower()
    project.target = Path(project.target)

    env.globals = {'project': vars(project)}
    Path(project.target, project.name).mkdir()
    Path(project.target, '.github', 'workflows').mkdir(parents=True)
    Path(project.target, 'subprojects').mkdir()
    Path(project.target, 'tests').mkdir()

    for filename in root_templates:
        template = env.get_template(f'{filename}.j2')
        with open(project.target / filename, 'w') as f:
            f.write(template.render())

    for filename in source_templates:
        template = env.get_template(f'{filename}.j2')
        with open(project.target / filename, 'w') as f:
            f.write(template.render())


if __name__ == '__main__':
    main()
