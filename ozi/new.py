# ozi/new.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""quick-start OZI project creation script."""
from __future__ import annotations

import argparse
import re
import shlex
import sys
import warnings
from typing import TYPE_CHECKING
from typing import NoReturn

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Sequence

    from jinja2 import Environment

from pathlib import Path
from urllib.parse import urlparse
from warnings import simplefilter
from warnings import warn

from ozi.actions import CloseMatch
from ozi.assets import parse_project_name
from ozi.assets import parse_spdx
from ozi.render import env
from ozi.render import render_ci_files_set_user
from ozi.render import render_project_files
from ozi.spec import Metadata
from ozi.vendor.email_validator import EmailNotValidError
from ozi.vendor.email_validator import EmailSyntaxError
from ozi.vendor.email_validator import validate_email

metadata = Metadata()


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


def tap_warning_format(  # pragma: no cover
    message: Warning | str,
    category: type[Warning],
    filename: str,
    lineno: int,
    line: str | None = None,
) -> str:
    """Test Anything Protocol formatted warnings."""
    return f'# {filename}:{lineno}: {category.__name__}\nnot ok - {message}\n'  # pragma: no cover


warnings.formatwarning = tap_warning_format


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
    metavar='Part of the NAME project.\\nSee LICENSE...',
)
ozi_defaults.add_argument(
    '--ci-provider',
    type=str,
    default='github',
    choices=frozenset(('github',)),
    metavar='github',
    help='continuous integration and release provider',
)
required.add_argument(
    '-n',
    '--name',
    type=str,
    help='Name (Single Use)',
    required=True,
)
required.add_argument(
    '-a',
    '--author',
    type=str,
    help='Author (Multiple Use, Single output)',
    required=True,
    action='append',
    default=[],
    nargs='?',
)
required.add_argument(
    '-e',
    '--author-email',
    type=str,
    help='Author-email (Multiple Use, Single output)',
    required=True,
    default=[],
    nargs='?',
    action='append',
)
required.add_argument(
    '-s',
    '--summary',
    type=str,
    help='Summary (Single Use)',
    required=True,
)
required.add_argument(
    '-p',
    '--home-page',
    type=str,
    help='Home-page (Single Use)',
    required=True,
)
required.add_argument(
    '--license-expression',
    type=str,
    help='Classifier: License Expression (Single Use, SPDX Expression)',
    required=True,
)
required.add_argument(
    '-l',
    '--license',
    type=str,
    help='Classifier: License (Single Use)',
    action=CloseMatch,
    required=True,
)
ozi_required.add_argument(
    'target',
    type=str,
    help='target directory for new project',
)
project_output = project_parser.add_mutually_exclusive_group()
project_output.add_argument(
    '-h',
    '--help',
    action='help',
    help='show this help message and exit',
)
defaults.add_argument(
    '--audience',
    '--intended-audience',
    type=str,
    help='Classifier: Intended Audience (Multiple Use)(default: ["Other Audience"])',
    default=['Other Audience'],
    nargs='?',
    action=CloseMatch,
)
defaults.add_argument(
    '--typing',
    type=str,
    choices=frozenset(('Typed', 'Stubs Only')),
    nargs='?',
    help='Classifier: Typing (Multiple Use)(default: [Typed])',
    default=['Typed'],
)
defaults.add_argument(
    '--environment',
    default=['Other Environment'],
    help='Classifier: Environment (Multiple Use)(default: ["Other Environment"])',
    action=CloseMatch,
    nargs='?',
    type=str,
)
defaults.add_argument(
    '--license-file',
    default='LICENSE.txt',
    choices=frozenset(('LICENSE.txt',)),
    help='Classifier: License File (Single Use)(default: LICENSE.txt)',
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
    default=[],
    action='append',
    nargs='?',
    help='Maintainer (Multiple Use, Single output, if different from Author)',
)
optional.add_argument(
    '--maintainer-email',
    help='Maintainer-Email (Multiple Use, Single output, if different from Author-Email)',
    action='append',
    default=[],
    nargs='?',
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
    nargs='?',
)
defaults.add_argument(
    '--language',
    '--natural-language',
    default=['English'],
    help='Classifier: Natural Language (Multiple Use)(default: [English])',
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
    help='Classifier: Development Status (Single Use)(default: "1 - Planning")',
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
ozi_defaults.add_argument(
    '--verify-email',
    default='--no-verify-email',
    action=argparse.BooleanOptionalAction,
    help='verify email domain deliverability(default: --no-verify-email)',
)
ozi_defaults.add_argument(
    '--check-for-update',
    default='--check-for-update',
    action=argparse.BooleanOptionalAction,
    help='check that the package version of OZI is up to date(default: --check-for-update)',
)
ozi_defaults.add_argument(
    '--strict',
    default='--no-strict',
    action=argparse.BooleanOptionalAction,
    help='strict mode raises warnings to errors(default: --strict)',
)
ozi_defaults.add_argument(
    '--allow-file',
    help='Add a file to the allow list for new project target folder(default: [templates, .git])',
    action='append',
    type=str,
    nargs='?',
    default=['templates', '.git'],
)


def copyright_head(
    project: argparse.Namespace,
    count: int,
) -> tuple[argparse.Namespace, int]:
    """OZI:Copyright-Head"""
    if len(project.copyright_head) == 0:
        project.copyright_head = '\n'.join(
            [
                f'Part of {project.name}.',
                f'See {project.license_file} in the project root for details.',
            ],
        )
        print('ok', '-', 'Default-Copyright-Header')
    count += 1
    return project, count


def license_(project: argparse.Namespace, count: int) -> tuple[argparse.Namespace, int]:
    """PKG-INFO:License"""
    possible_spdx: Sequence[str] = metadata.spec.python.pkg.license.ambiguous.get(
        project.license,
        (),
    )
    if (
        project.license in iter(metadata.spec.python.pkg.license.ambiguous)
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
        warn(msg, RuntimeWarning, stacklevel=0)
    else:
        print('ok', '-', 'License')
    count += 1
    return project, count


def license_expression(
    project: argparse.Namespace,
    count: int,
) -> tuple[argparse.Namespace, int]:
    """PKG-INFO[PEP-639]:License-Expression"""
    project.license_expression = parse_spdx(project.license_expression)
    count += 1
    return project, count


def summary(project: argparse.Namespace, count: int) -> tuple[argparse.Namespace, int]:
    """PKG-INFO:Summary"""
    if len(project.summary) > 512:
        warn(
            'Project summary exceeds 512 characters (PyPI limit).',
            RuntimeWarning,
            stacklevel=0,
        )
    else:
        print('ok', '-', 'Summary')
    count += 1
    return project, count


def keywords(project: argparse.Namespace, count: int) -> tuple[argparse.Namespace, int]:
    """PKG-INFO:Keywords"""
    project.keywords = project.keywords.split(',')
    return project, count


def author_email(
    project: argparse.Namespace,
    count: int,
) -> tuple[argparse.Namespace, int]:
    """PKG-INFO:Author-Email"""
    project.author_email, project.maintainer_email = parse_email(
        project.author_email,
        project.maintainer_email,
        project.verify_email,
    )
    return project, count


def maintainer_email(  # noqa: C901
    project: argparse.Namespace,
    count: int,
) -> tuple[argparse.Namespace, int]:
    """PKG-INFO:Maintainer-Email,Author,Maintainer"""
    author_and_maintainer_email = False
    if set(project.author_email).intersection(project.maintainer_email):
        warn(
            'One or more Author-Email and Maintainer-Email are identical.'
            'Maintainer-Email should be empty.',
            RuntimeWarning,
            stacklevel=0,
        )
    elif any(map(len, project.maintainer_email)) and not any(map(len, project.author_email)):
        warn(
            'Maintainer-Email provided without setting Author-Email.',
            RuntimeWarning,
            stacklevel=0,
        )
    elif any(map(len, project.maintainer_email)) and any(map(len, project.author_email)):
        author_and_maintainer_email = True
        print('ok', '-', 'Author-Email(s) and Maintainter-Email(s) provided.')
    else:
        print('ok', '-', 'Author-Email(s) provided.')
    count += 1

    if set(project.author_email).intersection(project.maintainer_email):
        warn(
            'Author and Maintainer are identical. Maintainer should be empty.',
            RuntimeWarning,
            stacklevel=0,
        )
    elif len(project.maintainer) and not len(project.author):
        warn('Maintainer provided without setting Author.', RuntimeWarning, stacklevel=0)
    elif len(project.maintainer) and len(project.author):
        print('ok', '-', 'Author and Maintainer provided.')
    elif author_and_maintainer_email and not len(project.maintainer):
        warn(  # pragma: defer to good-first-issue
            'Expected Maintainer name missing for provided Maintainer-Email.',
            RuntimeWarning,
            stacklevel=0,
        )
    else:
        print('ok', '-', 'Author provided.')
    count += 1
    return project, count


def name(project: argparse.Namespace, count: int) -> tuple[argparse.Namespace, int]:
    """PKG-INFO:Name"""
    project.name = parse_project_name(project.name)
    count += 1
    return project, count


def home_page(project: argparse.Namespace, count: int) -> tuple[argparse.Namespace, int]:
    """PKG-INFO:Home-page"""
    home_url = urlparse(project.home_page)
    if home_url.scheme != 'https':
        warn('Home-page url scheme unsupported.', RuntimeWarning, stacklevel=0)
    else:
        print('ok', '-', 'Home-page scheme')
    count += 1
    if home_url.netloc == '':
        warn('Home-page url netloc could not be parsed.', RuntimeWarning, stacklevel=0)
    else:
        print('ok', '-', 'Home-page netloc')
    count += 1
    return project, count


def project_url(project: argparse.Namespace, count: int) -> tuple[argparse.Namespace, int]:
    """PKG-INFO:Project-URL"""
    for name, url in [str(i).split(',') for i in project.project_url]:
        if len(name) > 32:
            warn(
                'Project-URL name is longer than 32 characters.',
                RuntimeWarning,
                stacklevel=0,
            )
        else:
            print('ok', '-', 'Project-URL name')
        count += 1
        parsed_url = urlparse(url)
        if parsed_url.scheme != 'https':
            warn('Project-URL url scheme unsupported.', RuntimeWarning, stacklevel=0)
        count += 1
        if parsed_url.netloc == '':
            warn('Project-URL url netloc could not be parsed.', RuntimeWarning, stacklevel=0)
        else:
            print('ok', '-', 'Project-URL netloc')
        count += 1
    return project, count


def create_project_files(
    project: argparse.Namespace,
    count: int,
    env: Environment,
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
    project.ci_user = render_ci_files_set_user(env, project.target, project.ci_provider)
    render_project_files(env, project.target, project.name)
    return count


def project(project: argparse.Namespace) -> int:
    """Create a new project in a target directory."""
    count = 0
    if project.strict:  # pragma: defer to pytest
        simplefilter('error', RuntimeWarning, append=True)
    project, count = project_url(
        *home_page(
            *name(
                *maintainer_email(
                    *author_email(
                        *keywords(
                            *summary(
                                *license_expression(
                                    *license_(*copyright_head(project, count)),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )
    project.name = re.sub(r'[-_.]+', '-', project.name).lower()
    project.target = Path(project.target)
    project.topic = list(set(project.topic))
    project.dist_requires = list(set(project.dist_requires))
    env.globals = env.globals | {'project': vars(project)}
    return create_project_files(project, count, env)


def wrap(project: argparse.Namespace) -> int:  # pragma: no cover
    """Create a new wrap file for publishing. Not a public function."""
    env.globals = env.globals | {'project': vars(project)}
    template = env.get_template('ozi.wrap.j2')
    with open('ozi.wrap', 'w') as f:
        f.write(template.render())
    return 1


def main() -> NoReturn | None:  # pragma: no cover
    """Main ozi.new entrypoint."""
    ozi_new = parser.parse_args()
    ozi_new.argv = shlex.join(sys.argv[1:])
    result = 0
    match ozi_new:
        case ozi_new if ozi_new.new in ['p', 'project']:
            result = project(ozi_new)
        case ozi_new if ozi_new.new in ['w', 'wrap']:
            result = wrap(ozi_new)
        case _:
            parser.print_usage()

    return print(f'1..{result}')


if __name__ == '__main__':
    main()
