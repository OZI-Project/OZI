from __future__ import annotations

import re
import shlex
import sys
import warnings
from functools import reduce
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from argparse import Namespace
    from collections.abc import Sequence
    from typing import Callable
    from typing import NoReturn
    from typing import TypeAlias

    from jinja2 import Environment

    Composable: TypeAlias = Callable[[Namespace, int], tuple[Namespace, int]]


from pathlib import Path
from urllib.parse import urlparse
from warnings import simplefilter
from warnings import warn

from ozi.assets import parse_project_name
from ozi.assets import parse_spdx
from ozi.assets import tap_warning_format
from ozi.new.parser import parser
from ozi.render import env
from ozi.render import render_ci_files_set_user
from ozi.render import render_project_files
from ozi.spec import Metadata
from ozi.vendor.email_validator import EmailNotValidError
from ozi.vendor.email_validator import EmailSyntaxError
from ozi.vendor.email_validator import validate_email

metadata = Metadata()
warnings.formatwarning = tap_warning_format


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


def copyright_head(
    project: Namespace,
    count: int,
) -> tuple[Namespace, int]:
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


def license_(project: Namespace, count: int) -> tuple[Namespace, int]:
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
    project: Namespace,
    count: int,
) -> tuple[Namespace, int]:
    """PKG-INFO[PEP-639]:License-Expression"""
    project.license_expression = parse_spdx(project.license_expression)
    count += 1
    return project, count


def summary(project: Namespace, count: int) -> tuple[Namespace, int]:
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


def keywords(project: Namespace, count: int) -> tuple[Namespace, int]:
    """PKG-INFO:Keywords"""
    project.keywords = project.keywords.split(',')
    return project, count


def author_email(
    project: Namespace,
    count: int,
) -> tuple[Namespace, int]:
    """PKG-INFO:Author-Email"""
    project.author_email, project.maintainer_email = parse_email(
        project.author_email,
        project.maintainer_email,
        project.verify_email,
    )
    return project, count


def maintainer_email(  # noqa: C901
    project: Namespace,
    count: int,
) -> tuple[Namespace, int]:
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


def name(project: Namespace, count: int) -> tuple[Namespace, int]:
    """PKG-INFO:Name"""
    project.name = parse_project_name(project.name)
    count += 1
    return project, count


def home_page(project: Namespace, count: int) -> tuple[Namespace, int]:
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


def project_url(project: Namespace, count: int) -> tuple[Namespace, int]:
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
    project: Namespace,
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


def compose(*functions: Composable) -> Composable:
    def inner(f: Composable, g: Composable) -> Composable:
        """The inner function to be reduced."""

        def result(x: Namespace, y: int) -> tuple[Namespace, int]:
            """Result output"""
            return f(*g(x, y))

        return result

    return reduce(inner, functions)


def project(project: Namespace) -> int:
    """Create a new project in a target directory."""
    count = 0
    if project.strict:  # pragma: defer to pytest
        simplefilter('error', RuntimeWarning, append=True)

    new_project = compose(
        project_url,
        home_page,
        name,
        maintainer_email,
        author_email,
        keywords,
        summary,
        license_expression,
        license_,
        copyright_head,
    )
    project, count = new_project(project, count)
    project.name = re.sub(r'[-_.]+', '-', project.name).lower()
    project.target = Path(project.target)
    project.topic = list(set(project.topic))
    project.dist_requires = list(set(project.dist_requires))
    env.globals = env.globals | {'project': vars(project)}
    return create_project_files(project, count, env)


def wrap(project: Namespace) -> int:  # pragma: no cover
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
