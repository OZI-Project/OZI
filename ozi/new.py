# ozi/new.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""quick-start OZI project creation script."""
import argparse
import hashlib
import re
import shlex
import sys
import warnings
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path
from typing import Callable, Mapping, NoReturn, Sequence, Tuple, Union
from urllib.parse import urlparse
from warnings import warn

import requests  # type: ignore
from email_validator import EmailNotValidError, EmailSyntaxError, validate_email
from git import InvalidGitRepositoryError, Repo
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
    prog='ozi-new',
    description=sys.modules[__name__].__doc__,
    add_help=False,
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
required = project_parser.add_argument_group('PKG-INFO required')
ozi_required = project_parser.add_argument_group('required')
ozi_defaults = project_parser.add_argument_group('defaults')
optional = project_parser.add_argument_group('PKG-INFO optional')
defaults = project_parser.add_argument_group('PKG-INFO defaults')
ozi_defaults.add_argument(
    '--copyright-head',
    type=str,
    default='',
    help='copyright header string',
    metavar='"Part of the NAME project.\\nSee LICENSE..."',
)
ozi_defaults.add_argument(
    '--ci-provider',
    type=str,
    default='github',
    choices=frozenset(('github',)),
    metavar='"github"',
    help='continuous integration and release provider',
)
required.add_argument('-n', '--name', type=str, help='Name (Single Use)')
required.add_argument('-a', '--author', type=str, help='Author (Single Use)')
required.add_argument(
    '-e',
    '--author-email',
    type=str,
    help='Author-email (Single Use, Comma-separated List)',
    action='append',
)
required.add_argument('-s', '--summary', type=str, help='Summary (Single Use)')
required.add_argument('-p', '--home-page', type=str, help='Home-page (Single Use)')
required.add_argument(
    '--license-expression',
    type=str,
    help='Classifier: License Expression (Single Use, SPDX Expression)',
)
required.add_argument(
    '-l',
    '--license',
    type=str,
    help='Classifier: License (Single Use)',
    action=CloseMatch,
)
ozi_required.add_argument(
    'target',
    type=str,
    help='target directory for new project',
)
project_output = project_parser.add_mutually_exclusive_group()
project_output.add_argument(
    '-h', '--help', action='help', help='show this help message and exit'
)
defaults.add_argument(
    '--audience',
    '--intended-audience',
    type=str,
    help='Classifier: Intended Audience (Multiple Use)',
    default=['Other Audience'],
    metavar='{Other Audience, ...}',
    nargs='?',
    action=CloseMatch,
)
defaults.add_argument(
    '--typing',
    type=str,
    choices=frozenset(('Typed', 'Stubs Only')),
    metavar='{Typing, ...}',
    nargs='?',
    help='Classifier: Typing (Multiple Use)',
    default=['Typed'],
)
defaults.add_argument(
    '--environment',
    default=['Other Environment'],
    metavar='{Other Environment,...}',
    help='Classifier: Environment (Multiple Use)',
    action=CloseMatch,
    nargs='?',
    type=str,
)
defaults.add_argument(
    '--license-file',
    default='LICENSE.txt',
    choices=frozenset(('LICENSE.txt',)),
    help='Classifier: License File (Single Use)',
    type=str,
)
optional.add_argument(
    '--keywords',
    default='',
    help='Keywords (Single Use, Comma-separated List)',
    type=str,
)
optional.add_argument(
    '--maintainer',
    default='',
    help='Maintainer (if different from Author)',
)
optional.add_argument(
    '--maintainer-email',
    default='',
    help='Maintainer-Email (if different from Author-Email)',
    action='append',
)
optional.add_argument(
    '--framework',
    help='Classifier: Framework (Multiple Use)',
    action=CloseMatch,
    type=str,
    nargs='?',
    default=[],
)
optional.add_argument(
    '--project-url',
    help='Project-URL (Multiple Use, Comma-separated Tuple[name, url])',
    action='append',
    default=[],
)
defaults.add_argument(
    '--language',
    '--natural-language',
    default=['English'],
    metavar='{English, ...}',
    help='Classifier: Natural Language (Multiple Use)',
    action=CloseMatch,
    type=str,
    nargs='?',
)
optional.add_argument(
    '--topic',
    help='Classifier: Topic (Multiple Use)',
    nargs='?',
    action=CloseMatch,
    type=str,
    default=[],
)
defaults.add_argument(
    '--status',
    '--development-status',
    action=CloseMatch,
    default=['1 - Planning'],
    help='Classifier: Development Status (Single Use)',
    metavar='"1 - Planning"',
    type=str,
)
optional.add_argument(
    '-r',
    '--dist-requires',
    help='Dist-Requires (Multiple Use)',
    action='append',
    type=str,
    nargs='?',
    default=[],
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
ozi_defaults.add_argument(
    '--verify-email',
    default='--no-verify-email',
    action=argparse.BooleanOptionalAction,
    help='email domain deliverability check',
)
ozi_defaults.add_argument(
    '--strict',
    default='--no-strict',
    action=argparse.BooleanOptionalAction,
    help='strict mode raises warnings to errors.',
)
ozi_defaults.add_argument(
    '--allow-file',
    help='Add a file to the allow list for new project target folder.',
    action='append',
    type=str,
    nargs='?',
    default=['templates', '.git'],
)


def copyright_head(
    project: argparse.Namespace, count: int
) -> Tuple[argparse.Namespace, int]:
    """OZI:Copyright-Head"""
    if len(project.copyright_head) == 0:
        project.copyright_head = '\n'.join(
            [
                f'Part of {project.name}.',
                f'See {project.license_file} in the project root for details.',
            ]
        )
        print('ok', '-', 'Default-Copyright-Header')
    count += 1
    return project, count


def license_(project: argparse.Namespace, count: int) -> Tuple[argparse.Namespace, int]:
    """PKG-INFO:License"""
    possible_spdx: Sequence[str] = spdx_options.get(project.license, ())
    if (
        project.license in ambiguous_licenses
        and project.license_expression.split(' ')[0] not in possible_spdx
    ):
        spdx_licenses = ', '.join(possible_spdx)
        msg = (
            f'Ambiguous License string per PEP 639: {project.license}; '
            'See also: https://github.com/pypa/trove-classifiers/issues/17;'
            'set --license-expression'
            f'to one of: {spdx_licenses} OR'
            'to a license expression based on one of these.'
        )
        warn(msg, RuntimeWarning)
    else:
        print('ok', '-', 'License')
    count += 1
    return project, count


def license_expression(
    project: argparse.Namespace, count: int
) -> Tuple[argparse.Namespace, int]:
    """PKG-INFO[PEP-639]:License-Expression"""
    try:
        project.license_expression = Combine(
            spdx_license_expression, join_string=' '
        ).parse_string(project.license_expression)[0]
        print('ok', '-', 'License-Expression')
    except ParseException as e:
        warn(str(e).strip('\n'), RuntimeWarning)
    count += 1
    return project, count


def summary(project: argparse.Namespace, count: int) -> Tuple[argparse.Namespace, int]:
    """PKG-INFO:Summary"""
    if len(project.summary) > 512:
        warn('Project summary exceeds 512 characters (PyPI limit).', RuntimeWarning)
    else:
        print('ok', '-', 'Summary')
    count += 1
    return project, count


def keywords(project: argparse.Namespace, count: int) -> Tuple[argparse.Namespace, int]:
    """PKG-INFO:Keywords"""
    project.keywords = project.keywords.split(',')
    return project, count


def author_email(  # noqa: C901
    project: argparse.Namespace, count: int
) -> Tuple[argparse.Namespace, int]:
    """PKG-INFO:Author-Email"""
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
        except (EmailNotValidError, EmailSyntaxError) as e:
            warn(str(e), RuntimeWarning)
        count += 1
    project.author_email = author_email
    project.maintainer_email = maintainer_email

    return project, count


def maintainer_email(  # noqa: C901
    project: argparse.Namespace, count: int
) -> Tuple[argparse.Namespace, int]:
    """PKG-INFO:Maintainer-Email,Author,Maintainer"""
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
    return project, count


def name(project: argparse.Namespace, count: int) -> Tuple[argparse.Namespace, int]:
    """PKG-INFO:Name"""
    try:
        Regex('^([A-Z]|[A-Z][A-Z0-9._-]*[A-Z0-9])$', re.IGNORECASE).set_name(
            'Package-Index-Name'
        ).parse_string(project.name)
        print('ok', '-', 'Name')
    except ParseException as e:
        warn(str(e), RuntimeWarning)
    count += 1
    return project, count


def home_page(project: argparse.Namespace, count: int) -> Tuple[argparse.Namespace, int]:
    """PKG-INFO:Home-page"""
    home_url = urlparse(project.home_page)
    if home_url.scheme != 'https':
        warn('Home-page url scheme unsupported.', RuntimeWarning)
    else:
        print('ok', '-', 'Home-page scheme')
    count += 1
    if home_url.netloc == '':
        warn('Home-page url netloc could not be parsed.', RuntimeWarning)
    else:
        print('ok', '-', 'Home-page netloc')
    count += 1
    return project, count


def project_url(project: argparse.Namespace, count: int) -> Tuple[argparse.Namespace, int]:
    """PKG-INFO:Project-URL"""
    for name, url in [str(i).split(',') for i in project.project_url]:
        if len(name) > 32:
            warn('Project-URL name is longer that 32 characters.', RuntimeWarning)
        else:
            print('ok', '-', 'Project-URL name')
        count += 1
        parsed_url = urlparse(url)
        if parsed_url.scheme != 'https':
            warn('Project-URL url scheme unsupported.', RuntimeWarning)
        else:
            print('ok', '-', 'Project-URL scheme')
        count += 1
        if parsed_url.netloc == '':
            warn('Project-URL url netloc could not be parsed.', RuntimeWarning)
        else:
            print('ok', '-', 'Project-URL netloc')
        count += 1
    return project, count


def create_project_files(  # noqa: C901
    project: argparse.Namespace, count: int, env: Environment
) -> int:
    """Create the actual project."""
    project.allow_file = set(map(Path, project.allow_file))
    iterdir = (i for i in project.target.iterdir() if i not in project.allow_file)
    if any(iterdir):
        warn(
            'Bail out! target directory not empty. No files will be created. Exiting.',
            RuntimeWarning,
        )
        return 0

    if project.ci_provider == 'github':
        try:
            project.ci_user = Repo(project.target).config_reader().get('user', 'name')
        except InvalidGitRepositoryError:
            project.ci_user = ''
        Path(project.target, '.github', 'workflows').mkdir(parents=True)
        template = env.get_template('github_workflows/ozi.yml.j2')
        with open(Path(project.target, '.github', 'workflows', 'ozi.yml'), 'w') as f:
            f.write(template.render())
    else:
        warn(
            f'--ci-provider "{project.ci_provider}" unrecognized. ci_user could not be set.',
            RuntimeWarning,
        )

    Path(project.target, underscorify(project.name)).mkdir()
    Path(project.target, 'subprojects').mkdir()
    Path(project.target, 'tests').mkdir()

    for filename in root_templates:
        template = env.get_template(f'{filename}.j2')
        try:
            content = template.render(
                filename=filename,
                date=datetime.now(tz=datetime.now(timezone.utc).astimezone().tzinfo),
            )
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

    template = env.get_template('project.ozi.wrap.j2')
    with open(project.target / 'subprojects' / 'ozi.wrap', 'w') as f:
        f.write(template.render())

    return count


def new_project(project: argparse.Namespace) -> int:
    """Create a new project in a target directory."""
    count = 0

    if project.strict:  # pragma: defer to pytest
        import warnings

        warnings.simplefilter('error', RuntimeWarning, append=True)

    args = copyright_head(project, count)
    args = license_(*args)
    args = license_expression(*args)
    args = summary(*args)
    args = keywords(*args)
    args = author_email(*args)
    args = maintainer_email(*args)
    args = name(*args)
    args = home_page(*args)
    args = project_url(*args)

    project, count = args

    project.name = re.sub(r'[-_.]+', '-', project.name).lower()
    project.target = Path(project.target)
    project.topic = list(set(project.topic))
    project.dist_requires = list(set(project.dist_requires))

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
    return create_project_files(project, count, env)


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


__new_item: Mapping[str, Callable[[argparse.Namespace], int]] = {
    'project': new_project,
    'wrap': __new_wrap,
}


def main() -> Union[NoReturn, None]:  # pragma: no cover
    """Main ozi.new entrypoint."""
    project = parser.parse_args()
    project.argv = shlex.join(sys.argv[1:])
    if project.list == '':
        pass
    elif project.list in list_available.keys():
        print(*list_available.get(project.list, []), sep='\n')
        exit(0)
    return print(f'1..{__new_item.get(project.new, lambda _: None)(project)}')


if __name__ == '__main__':
    main()
