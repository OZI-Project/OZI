# ozi/new.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""quick-start OZI project creation script."""
import argparse
import hashlib
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import NoReturn, Tuple, Union
from urllib.parse import urlparse
from warnings import warn

from email_validator import EmailNotValidError, validate_email
from importlib_metadata import version
from jinja2 import Environment, PackageLoader, select_autoescape
from pyparsing import Combine, ParseException, Regex
import requests
from spdx_license_list import LICENSES  # type: ignore

from .assets import (
    CloseMatch,
    OZI_SPEC,
    ambiguous_licenses,
    root_templates,
    source_templates,
    spdx_license_expression,
    spdx_options,
    test_templates,
    top4,
    underscorify,
)
from .fix import report_missing


def sha256sum(url: str) -> str:
    """Checksum filter for URL content."""
    checksum = hashlib.sha256()
    chunksize = 128*512
    response = requests.get(url, allow_redirects=True, stream=True, timeout=30)
    for chunk in response.iter_content(chunksize):
        checksum.update(chunk)
    return checksum.hexdigest()


env = Environment(
    loader=PackageLoader('ozi'),
    autoescape=select_autoescape(),
    enable_async=True,
)
env.filters['underscorify'] = underscorify
env.filters['sha256sum'] = sha256sum

parser = argparse.ArgumentParser(
    prog='ozi-new', description=sys.modules[__name__].__doc__, add_help=False
)
subparser = parser.add_subparsers(help='create new projects, sources, & tests', dest='new')
project_parser = subparser.add_parser(
    'project',
    aliases=['p'],
    description='Create a new Python project with OZI.',
    add_help=False,
)
source_parser = subparser.add_parser(
    'source', aliases=['s'], description='Create a new Python source in an OZI project.'
)
test_parser = subparser.add_parser(
    'test',
    aliases=['t'],
    description='Create a new Python test in an OZI project.',
)
wrap_parser = subparser.add_parser(
    'wrap',
    aliases=['w'],
    description='Create a new OZI wrapdb file.',
)
required = project_parser.add_argument_group('required')
required.add_argument('--name', type=str, help='name of project')
required.add_argument('--author', type=str, help='author of project')
required.add_argument('--email', type=str, help='valid author email')
required.add_argument('--summary', type=str, help='short summary')
required.add_argument('--homepage', type=str, help='homepage URL')
license = project_parser.add_argument_group('license options')
license.add_argument(
    '--license-expression',
    type=str,
    metavar='ID e.g. MIT, BSD-2-Clause, GPL-3.0-or-later, Apache-2.0',
    help='SPDX short ID or composite license for license disambiguation',
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
    default=False,
    action=argparse.BooleanOptionalAction,
    help='email domain deliverability check',
)
output = project_parser.add_argument_group('output options')
output.add_argument(
    '--strict',
    default=False,
    action=argparse.BooleanOptionalAction,
    help='strict mode raises warnings to errors.',
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
    '--intended-audience',
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
    help='typing for the project (OZI specifies Typed packages).',
)
defaults.add_argument(
    '--environment',
    default='Other Environment',
    help='primary environment for project use case',
    metavar='"Other Environment"',
    action=CloseMatch,
    type=str,
)
defaults.add_argument(
    '--license-file',
    default='LICENSE.txt',
    help='license text file path',
    metavar='PATH',
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
    '--natural-language',
    default='English',
    help='primary natural language',
    metavar='"English"',
    action=CloseMatch,
    type=str,
)
defaults.add_argument(
    '--topic',
    default=['Utilities'],
    help='Python package topic (this option may be used multiple times)',
    metavar='"Utilities"',
    nargs='?',
    action='append',
    type=str,
)
defaults.add_argument(
    '--status',
    '--development-status',
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
        'license-expression',
        'status',
        'topic',
    ],
    help='list valid option settings and exit',
)
source_required = source_parser.add_argument_group('required')
source_required.add_argument(
    'target', type=str, help='path to directory containing an OZI project'
)
source_required.add_argument('name', type=str, help='name of the Python source file')
source_required.add_argument('--author', type=str, help='author of file')
source_defaults = source_parser.add_argument_group('defaults')
source_defaults.add_argument(
    '--copyright-head',
    type=str,
    default='',
    help='copyright header string',
    metavar='"Copyright {year}, {author}\\nSee LICENSE..."',
)
test_required = test_parser.add_argument_group('required')
test_required.add_argument(
    'target', type=str, help='path to directory containing an OZI project'
)
test_required.add_argument('name', type=str, help='name of the Python test file')
test_required.add_argument('--author', type=str, help='author of file')
test_defaults = test_parser.add_argument_group('defaults')
test_defaults.add_argument(
    '--copyright-head',
    type=str,
    default='',
    help='copyright header string',
    metavar='"Copyright {year}, {author}\\nSee LICENSE..."',
)


def main() -> Union[NoReturn, str]:
    """Main ozi.new entrypoint."""
    ambiguous_license_classifier = True
    project = parser.parse_args()
    if project.list == '':
        pass
    elif project.list == 'license':
        print(*sorted((i for i in CloseMatch.license)), sep='\n')
        exit(0)
    elif project.list == 'language':
        print(*sorted((i for i in CloseMatch.language)), sep='\n')
        exit(0)
    elif project.list == 'framework':
        print(*sorted((i for i in CloseMatch.framework)), sep='\n')
        exit(0)
    elif project.list == 'environment':
        print(*sorted((i for i in CloseMatch.environment)), sep='\n')
        exit(0)
    elif project.list == 'license-expression':
        print(
            *sorted((k for k, v in LICENSES.items() if v.deprecated_id is False)), sep='\n'
        )
        exit(0)
    elif project.list == 'status':
        print(*sorted((i for i in CloseMatch.status)), sep='\n')
        exit(0)
    elif project.list == 'topic':
        print(*sorted(i for i in CloseMatch.topic), sep='\n')
        exit(0)
    elif project.list == 'audience':
        print(*sorted(i for i in CloseMatch.audience), sep='\n')
        exit(0)

    if project.new == 'project':

        local_tz = datetime.now(timezone.utc).astimezone().tzinfo
        project.copyright_year = datetime.now(tz=local_tz).year
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

        if project.strict:
            import warnings
            warnings.simplefilter('error', RuntimeWarning, append=True)

        if project.license in ambiguous_licenses:
            msg = [
                f'Ambiguous License string per PEP 639: {project.license}',
                'See also: https://github.com/pypa/trove-classifiers/issues/17',
            ]
            warn('\n'.join(msg), RuntimeWarning)
        else:
            ambiguous_license_classifier = False

        possible_spdx: Tuple[str, ...] = spdx_options.get(project.license, ())
        if (
            ambiguous_license_classifier
            and project.license_expression.split(' ')[0] not in possible_spdx
        ):
            msg = [
                'Cannot disambiguate license automatically.',
                'Please set --license-expression',
                f'to one of: {", ".join(possible_spdx)}',
                'OR',
                'to a compound license expression based on one of those listed above.',
            ]
            warn('\n'.join(msg), RuntimeWarning)

        project.license_expression = Combine(
            spdx_license_expression, join_string=' '
        ).parse_string(project.license_expression)[0]

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
        project.topic = list(set(project.topic))

        if any(project.target.iterdir()):
            raise FileExistsError('Directory not empty.')

        env.globals = env.globals | {
            'project': vars(project),
            'ozi': {
                'version': version('OZI'),
                'spec': '0.1',
            },
        }
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
            filename = filename.replace('project.name', underscorify(project.name).lower())
            with open(project.target / filename, 'w') as f:
                f.write(template.render())

        for filename in test_templates:
            template = env.get_template(f'{filename}.j2')
            with open(project.target / filename, 'w') as f:
                f.write(template.render())

        if project.ci_provider == 'github':
            template = env.get_template('github_workflows/ozi.yml.j2')
            with open(Path(project.target, '.github', 'workflows', 'ozi.yml'), 'w') as f:
                f.write(template.render())

    elif project.new == 'source':
        local_tz = datetime.now(timezone.utc).astimezone().tzinfo
        project.copyright_year = datetime.now(tz=local_tz).year
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
        env.globals = env.globals | {
            'project': vars(project),
            'ozi': {
                'version': version('OZI'),
                'spec': OZI_SPEC,
            },
        }
        template = env.get_template('project.name/new_module.py.j2')
        normalized_name, pkg_info, *_ = report_missing(project.target, True, False)
        with open(
            Path(project.target, underscorify(normalized_name), project.name), 'w'
        ) as f:
            f.write(template.render())

    elif project.new == 'test':
        local_tz = datetime.now(timezone.utc).astimezone().tzinfo
        project.copyright_year = datetime.now(tz=local_tz).year
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
        env.globals = env.globals | {
            'project': vars(project),
            'ozi': {
                'version': version('OZI'),
                'spec': OZI_SPEC,
            },
        }
        template = env.get_template('tests/new_test.py.j2')
        normalized_name, pkg_info, *_ = report_missing(project.target, True, False)
        with open(Path(project.target, 'tests', project.name), 'w') as f:
            f.write(template.render())

    elif project.new == 'wrap':
        env.globals = env.globals | {
            'project': vars(project),
            'ozi': {
                'version': version('OZI'),
                'spec': OZI_SPEC,
            },
        }
        template = env.get_template('ozi.wrap.j2')
        with open('ozi.wrap', 'w') as f:
            f.write(template.render())

    return 'ok'


if __name__ == '__main__':
    main()
