# ozi/new.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""quick-start OZI project creation script."""
import argparse
import hashlib
import re
import sys
import warnings
from importlib.metadata import version
from pathlib import Path
from typing import Callable, Mapping, NoReturn, Sequence, Union
from urllib.parse import urlparse
from warnings import warn

import requests
from email_validator import EmailNotValidError, validate_email
from jinja2 import Environment, PackageLoader, TemplateNotFound, select_autoescape
from pyparsing import Combine, ParseException, Regex
from spdx_license_list import LICENSES  # type: ignore

from .assets import (
    CloseMatch,
    ambiguous_licenses,
    implementation_support,
    metadata_version,
    python_support,
    root_templates,
    source_templates,
    spdx_exceptions,
    spdx_license_expression,
    spdx_options,
    specification_version,
    tap_warning_format,
    test_templates,
    top4,
    underscorify,
    wheel_repr,
)

warnings.formatwarning = tap_warning_format  # type: ignore

list_available = {
    'audience': sorted((i for i in CloseMatch.audience)),
    'environment': sorted((i for i in CloseMatch.environment)),
    'framework': sorted((i for i in CloseMatch.framework)),
    'language': sorted((i for i in CloseMatch.language)),
    'license': sorted((i for i in CloseMatch.license)),
    'license-id': sorted((k for k, v in LICENSES.items() if v.deprecated_id is False)),
    'license-exception-id': sorted(spdx_exceptions),
    'status': sorted(CloseMatch.status),
    'topic': sorted(CloseMatch.topic),
}


def __sha256sum(url: str) -> str:  # pragma: no cover
    """Checksum filter for URL content."""
    checksum = hashlib.sha256()
    chunksize = 128 * 512
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
env.filters['sha256sum'] = __sha256sum
env.filters['wheel_repr'] = wheel_repr

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
wrap_parser = subparser.add_parser(
    'wrap',
    aliases=['w'],
    description='Create a new OZI wrapdb file.',
)
required = project_parser.add_argument_group('required')
required.add_argument('--name', type=str, help='name of project')
required.add_argument('--author', type=str, help='author of project')
required.add_argument('--author-email', type=str, help='valid author email', action='append')
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
    metavar='"Part of the NAME project.\\nSee LICENSE..."',
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
defaults.add_argument(
    '--keywords', default='', help='comma-separated list of keywords', type=str
)
optional = project_parser.add_argument_group('optional')
optional.add_argument(
    '--maintainer',
    default='',
    metavar='Maintainer (if different from Author)',
    help='maintainer of project',
)
optional.add_argument(
    '--maintainer-email',
    default='',
    metavar='Maintainer-Email (if different from Author-Email)',
    help='valid maintainer email',
    action='append',
)
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
    choices=list_available.keys(),
    help='list valid option settings and exit',
)


def new_project(project: argparse.Namespace) -> int:
    """Create a new project in a target directory."""
    count = 0
    if len(project.copyright_head) == 0:
        project.copyright_head = '\n'.join(
            [
                f'Part of {project.name}.',
                'See LICENSE.txt in the project root for details.',
            ]
        )
        print('ok', '-', 'Default-Copyright-Header')
    count += 1

    if project.strict:  # pragma: defer to pytest
        import warnings

        warnings.simplefilter('error', RuntimeWarning, append=True)

    possible_spdx: Sequence[str] = spdx_options.get(project.license, ())
    if (
        project.license in ambiguous_licenses
        and project.license_expression.split(' ')[0] not in possible_spdx
    ):
        msg = (
            f'Ambiguous License string per PEP 639: {project.license}; '
            'See also: https://github.com/pypa/trove-classifiers/issues/17;'
            'set --license-expression'
            f'to one of: {", ".join(possible_spdx)} OR'
            'to a license expression based on one of these.'
        )
        warn(msg, RuntimeWarning)
    else:
        print('ok', '-', 'License')
    count += 1

    try:
        project.license_expression = Combine(
            spdx_license_expression, join_string=' '
        ).parse_string(project.license_expression)[0]
        print('ok', '-', 'License-Expression')
    except ParseException as e:
        warn(str(e).strip('\n'), RuntimeWarning)
    count += 1

    if len(project.summary) > 512:
        warn('Project summary exceeds 512 characters (PyPI limit).', RuntimeWarning)
    else:
        print('ok', '-', 'Summary')
    count += 1

    project.keywords = project.keywords.split(',')

    author_email = []
    maintainer_email = []
    for email in set(project.author_email).union(project.maintainer_email):
        try:
            emailinfo = validate_email(email, check_deliverability=project.verify_email)
            email_normalized = emailinfo.normalized
            if email in project.author_email:
                author_email += [email_normalized]
            if email in project.maintainer_email:
                maintainer_email += [email_normalized]
            print('ok', '-', 'Author-Email')
        except EmailNotValidError as e:
            warn(str(e), RuntimeWarning)
        count += 1
    project.author_email = author_email
    project.maintainer_email = maintainer_email

    author_and_maintainer_email = False
    if set(project.author_email).intersection(project.maintainer_email):
        warn(
            'One or more Author-Email and Maintainer-Email are identical.'
            'Maintainer-Email should be empty.',
            RuntimeWarning,
        )
    elif any(map(len, project.maintainer_email)) and not any(map(len, project.author_email)):
        warn('Maintainer-Email provided without setting Author-Email.', RuntimeWarning)
    elif any(map(len, project.maintainer_email)) and any(map(len, project.author_email)):
        author_and_maintainer_email = True
        print('ok', '-', 'Author-Email(s) and Maintainter-Email(s) provided.')
    else:
        print('ok', '-', 'Author-Email(s) provided.')
    count += 1

    if project.author == project.maintainer:
        warn(
            'Author and Maintainer are identical. Maintainer should be empty.',
            RuntimeWarning,
        )
    elif len(project.maintainer) and not len(project.author):
        warn('Maintainer provided without setting Author.', RuntimeWarning)
    elif len(project.maintainer) and len(project.author):
        print('ok', '-', 'Author and Maintainer provided.')
    elif author_and_maintainer_email and not len(project.maintainer):
        warn(
            'Expected Maintainer name missing for provided Maintainer-Email.', RuntimeWarning
        )
    else:
        print('ok', '-', 'Author provided.')
    count += 1

    try:
        Regex('^([A-Z]|[A-Z][A-Z0-9._-]*[A-Z0-9])$', re.IGNORECASE).set_name(
            'Package-Index-Name'
        ).parse_string(project.name)
        print('ok', '-', 'Name')
    except ParseException as e:
        warn(str(e), RuntimeWarning)
    count += 1

    home_url = urlparse(project.homepage)
    if home_url.scheme != 'https':
        warn('Homepage url scheme unsupported.', RuntimeWarning)
    else:
        print('ok', '-', 'Homepage-Scheme')
    count += 1

    if home_url.netloc == '':
        warn('Homepage url netloc could not be parsed.', RuntimeWarning)
    else:
        print('ok', '-', 'Homepage-Netloc')
    count += 1

    project.name = re.sub(r'[-_.]+', '-', project.name).lower()
    project.target = Path(project.target)
    project.topic = list(set(project.topic))

    env.globals = env.globals | {
        'project': vars(project),
        'ozi': {
            'version': version('OZI'),
            'spec': specification_version,
            'metadata_version': metadata_version,
            'py_major': python_support.major,
            'py_security': '.'.join(
                map(str, (python_support.major, python_support.security))
            ),
            'py_bugfix2': '.'.join(map(str, (python_support.major, python_support.bugfix2))),
            'py_bugfix1': '.'.join(map(str, (python_support.major, python_support.bugfix1))),
            'py_implementations': implementation_support,
        },
    }

    if any(project.target.iterdir()):
        warn(
            'Bail out! target directory not empty. No files will be created. Exiting.',
            RuntimeWarning,
        )
        return 0

    if project.ci_provider == 'github':
        Path(project.target, '.github', 'workflows').mkdir(parents=True)
        template = env.get_template('github_workflows/ozi.yml.j2')
        with open(Path(project.target, '.github', 'workflows', 'ozi.yml'), 'w') as f:
            f.write(template.render())
    else:
        warn(
            f'Bail out! --ci-provider {project.ci_provider} unrecognized. No files will be created. Exiting',
            RuntimeWarning,
        )
        return 0

    Path(project.target, underscorify(project.name)).mkdir()
    Path(project.target, 'subprojects').mkdir()
    Path(project.target, 'tests').mkdir()

    for filename in root_templates:
        template = env.get_template(f'{filename}.j2')
        try:
            content = template.render()
        except TemplateNotFound:  # pragma: defer to good-first-issue
            content = f'template "{filename}" failed to render.'
            warn(content, RuntimeWarning)
        with open(project.target / filename, 'w') as f:
            f.write(content)

    for filename in source_templates:
        template = env.get_template(f'{filename}.j2')
        filename = filename.replace('project.name', underscorify(project.name).lower())
        with open(project.target / filename, 'w') as f:
            f.write(template.render())

    for filename in test_templates:
        template = env.get_template(f'{filename}.j2')
        with open(project.target / filename, 'w') as f:
            f.write(template.render())

    return count


def __new_wrap(project: argparse.Namespace) -> int:  # pragma: no cover
    """Create a new wrap file for publishing. Not a public function."""

    env.globals = env.globals | {
        'project': vars(project),
        'ozi': {
            'version': version('OZI'),
            'metadata_version': metadata_version,
            'spec': specification_version,
            'py_major': python_support.major,
            'py_security': '.'.join(
                map(str, (python_support.major, python_support.security))
            ),
            'py_bugfix2': '.'.join(map(str, (python_support.major, python_support.bugfix2))),
            'py_bugfix1': '.'.join(map(str, (python_support.major, python_support.bugfix1))),
            'py_implementations': implementation_support,
        },
    }
    template = env.get_template('ozi.wrap.j2')
    with open('ozi.wrap', 'w') as f:
        f.write(template.render())
    return 1


__new_item: Mapping[str, Callable] = {
    'project': new_project,
    'wrap': __new_wrap,
}


def main() -> Union[NoReturn, None]:  # pragma: no cover
    """Main ozi.new entrypoint."""
    project = parser.parse_args()
    if project.list == '':
        pass
    elif project.list in list_available.keys():
        print(*list_available.get(project.list, []), sep='\n')
        exit(0)
    return print(f'1..{__new_item.get(project.new, lambda _: None)(project)}')


if __name__ == '__main__':
    main()
