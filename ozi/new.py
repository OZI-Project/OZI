#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
"""quick-start OZI project creation script."""
import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import NoReturn, Union
from urllib.parse import urlparse
from warnings import warn

from email_validator import EmailNotValidError, validate_email
from jinja2 import Environment, PackageLoader, select_autoescape
from pyparsing import ParseException, Regex

from .assets import (
    CloseMatch,
    LICENSES,
    ambiguous_licenses,
    root_templates,
    source_templates,
    spdx_options,
    top4,
)


env = Environment(
    loader=PackageLoader('ozi'),
    autoescape=select_autoescape(),
    enable_async=True,
)


def underscorify(s: str) -> str:
    """Filter to replace non-alphanumerics with underscores."""
    return re.sub('[^0-9a-zA-Z]', '_', s)


env.filters['underscorify'] = underscorify

parser = argparse.ArgumentParser(
    prog='ozi-new', description=sys.modules[__name__].__doc__, add_help=False
)
subparser = parser.add_subparsers(help='project help')
project_parser = subparser.add_parser(
    'project',
    description='Create a new Python project with OZI.',
    add_help=False)
required = project_parser.add_argument_group('required')
required.add_argument('--name', type=str, help='name of project')
required.add_argument('--author', type=str, help='author of project')
required.add_argument('--email', type=str, help='valid author email')
required.add_argument('--summary', type=str, help='short summary')
required.add_argument('--homepage', type=str, help='homepage URL')
license = project_parser.add_argument_group('license options')
license.add_argument(
    '--license-spdx',
    type=str,
    metavar='ID e.g. MIT, BSD-2-Clause, GPL-3.0-or-later, Apache-2.0',
    help='SPDX short ID for license disambiguation',
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
    default='--no-verify-email',
    action=argparse.BooleanOptionalAction,
    help='email domain deliverability check',
)
defaults = project_parser.add_argument_group('defaults')
defaults.add_argument(
    '--copyright-head',
    type=str,
    default='',
    help='copyright header string',
    metavar='"Copyright {year}, {author}\\nSee LICENSE..."',
)
defaults.add_argument(
    '--ci-provider',
    type=str,
    default='github',
    choices=('github',),
    metavar='"github"',
    help='continuous integration and release provider',
)
project_output = project_parser.add_mutually_exclusive_group()
project_output.add_argument(
    '-h', '--help', action='help', help='show this help message and exit'
)
defaults.add_argument(
    '--audience',
    type=str,
    metavar='"Other Audience"',
    default='Other Audience',
    help='audience for the project',
    action=CloseMatch,
)
defaults.add_argument(
    '--typing',
    type=str,
    metavar='"Typed"',
    default='Typed',
    help='typing for the project (OZI specifies Typed packages).'
)
defaults.add_argument(
    '--environment',
    default='Other Environment',
    help='primary environment for project use case',
    metavar='"Other Environment"',
    action=CloseMatch,
    type=str,
)
optional = project_parser.add_argument_group('optional')
optional.add_argument(
    '--framework',
    default='',
    help='primary project framework',
    metavar='FRAMEWORK e.g. tox, Flake8, etc',
    action=CloseMatch,
    type=str,
)
defaults.add_argument(
    '--language',
    default='English',
    help='primary natural language',
    metavar='"English"',
    action=CloseMatch,
    type=str,
)
defaults.add_argument(
    '--topic',
    default='Utilities',
    help='Python package topic',
    metavar='"Utilities"',
    action=CloseMatch,
    type=str,
)
defaults.add_argument(
    '--status',
    action=CloseMatch,
    default='1 - Planning',
    help='Python package status',
    metavar='"1 - Planning"',
    type=str,
)
output = parser.add_mutually_exclusive_group()
output.add_argument('-h', '--help', action='help', help='show this help message and exit')
output.add_argument(
    '-l',
    '--list',
    type=str,
    choices=[
        'audience',
        'environment',
        'framework',
        'language',
        'license',
        'license-spdx',
        'status',
        'topic',
    ],
    help='list valid option settings and exit',
)


def main() -> Union[NoReturn, None]:
    """Main ozi.new entrypoint."""
    ambiguous_license_classifier = True
    project = parser.parse_args()
    if project.list == 'license':
        print(*sorted((i for i in CloseMatch.license)), sep='\n')
        exit(0)
    if project.list == 'language':
        print(*sorted((i for i in CloseMatch.language)), sep='\n')
        exit(0)
    if project.list == 'framework':
        print(*sorted((i for i in CloseMatch.framework)), sep='\n')
        exit(0)
    if project.list == 'environment':
        print(*sorted((i for i in CloseMatch.environment)), sep='\n')
        exit(0)
    if project.list == 'license-spdx':
        print(
            *sorted((k for k, v in LICENSES.items() if v.deprecated_id is False)), sep='\n'
        )
        exit(0)
    if project.list == 'status':
        print(*sorted((i for i in CloseMatch.status)), sep='\n')
        exit(0)
    if project.list == 'topic':
        print(*sorted(i for i in CloseMatch.topic), sep='\n')
        exit(0)
    if project.list == 'audience':
        print(*sorted(i for i in CloseMatch.audience), sep='\n')
        exit(0)

    project.copyright_year = datetime.now(tz=datetime.now(timezone.utc).astimezone().tzinfo).year
    if len(project.copyright_head) == 0:
        project.copyright_head = '\n'.join(
            [
                f'Copyright {project.copyright_year}, {project.author}',
                'See LICENSE.txt in the project root for details.',
            ]
        )
    else:
        project.copyright_head = project.copyright_head.format(
            year=project.copyright_year, author=project.author
        )

    if project.license in ambiguous_licenses:
        msg = [
            f'Ambiguous License string per PEP 639: {project.license}',
            'See also: https://github.com/pypa/trove-classifiers/issues/17',
            'This will need updated when PEP 639 is implemented.',
        ]
        warn('\n'.join(msg), PendingDeprecationWarning)
    else:
        ambiguous_license_classifier = False

    possible_spdx = spdx_options.get(project.license, [])
    if ambiguous_license_classifier and project.license_spdx not in possible_spdx:
        msg = [
            'Cannot disambiguate license automatically.',
            'Please set --spdx-license',
            f'to one of: {", ".join(possible_spdx)}'
        ]
        warn('\n'.join(msg), RuntimeWarning)

    if len(project.summary) > 512:
        warn('Project summary exceeds 512 characters (PyPI limit).', RuntimeWarning)

    try:
        emailinfo = validate_email(
            project.email, check_deliverability=project.verify_email
        )
        project.email = emailinfo.normalized
    except EmailNotValidError as e:
        warn(
            f'{str(e)}\nInvalid maintainer email format or domain unreachable.',
            RuntimeWarning,
        )

    try:
        Regex('^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$', re.IGNORECASE).parse_string(
            project.name
        )
    except ParseException as e:
        warn(f'{str(e)}\nInvalid project name.', RuntimeWarning)

    home_url = urlparse(project.homepage)
    if home_url.scheme != 'https':
        warn('Homepage url scheme unsupported.', RuntimeWarning)

    if home_url.netloc == '':
        warn('Homepage url netloc cound not be parsed.', RuntimeWarning)

    project.name = re.sub(r'[-_.]+', '-', project.name).lower()
    project.target = Path(project.target)

    if any(project.target.iterdir()):
        raise FileExistsError('Directory not empty.')

    env.globals = env.globals | {'project': vars(project)}
    Path(project.target, underscorify(project.name)).mkdir()
    Path(project.target, '.github', 'workflows').mkdir(parents=True)
    Path(project.target, 'subprojects').mkdir()
    Path(project.target, 'tests').mkdir()

    for filename in root_templates:
        template = env.get_template(f'{filename}.j2')
        with open(project.target / filename, 'w') as f:
            f.write(template.render())

    for filename in source_templates:
        template = env.get_template(f'{filename}.j2')
        filename = filename.replace('project.name', underscorify(project.name))
        with open(project.target / filename, 'w') as f:
            f.write(template.render())


if __name__ == '__main__':
    main()
