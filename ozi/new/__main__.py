# ozi/new/__main__.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
from __future__ import annotations

import re
import shlex
import sys
from functools import reduce
from typing import TYPE_CHECKING
from typing import Any

from pyparsing import Combine
from pyparsing import ParseException
from pyparsing import ParseResults
from pyparsing import Regex

if TYPE_CHECKING:
    from argparse import Namespace
    from collections.abc import Sequence
    from typing import Callable
    from typing import NoReturn
    from typing import TypeAlias

    from jinja2 import Environment

    Composable: TypeAlias = Callable[[Namespace], Namespace]


from pathlib import Path
from urllib.parse import urlparse

from ozi.new.parser import parser
from ozi.render import env
from ozi.render import render_ci_files_set_user
from ozi.render import render_project_files
from ozi.spdx import spdx_license_expression
from ozi.spec import Metadata
from ozi.tap import TAP
from ozi.vendor.email_validator import EmailNotValidError
from ozi.vendor.email_validator import EmailSyntaxError
from ozi.vendor.email_validator import validate_email

metadata = Metadata()


def parse_project_name(name: str | ParseResults) -> str | ParseResults:
    try:
        Regex('^([A-Z]|[A-Z][A-Z0-9._-]*[A-Z0-9])$', re.IGNORECASE).set_name(
            'Package-Index-Name',
        ).parse_string(str(name))
        TAP.ok('Name')
    except ParseException as e:
        TAP.not_ok(*str(e).split('\n'))
    return name


def parse_spdx(expr: Any | ParseResults) -> Any | ParseResults:
    try:
        expr = Combine(
            spdx_license_expression,
            join_string=' ',
        ).parse_string(
            str(expr),
        )[0]
        TAP.ok('License-Expression')
    except ParseException as e:  # pragma: defer to good-issue
        TAP.not_ok(*str(e).split('\n'))
    return expr


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
            TAP.ok('Author-Email')
        except (EmailNotValidError, EmailSyntaxError) as e:
            TAP.not_ok(*str(e).split('\n'))
    return _author_email, _maintainer_email


def copyright_head(project: Namespace) -> Namespace:
    """OZI:Copyright-Head"""
    if len(project.copyright_head) == 0:
        project.copyright_head = '\n'.join(
            [
                f'Part of {project.name}.',
                f'See {project.license_file} in the project root for details.',
            ],
        )
        TAP.ok('Default-Copyright-Header')
    return project


def license_(project: Namespace) -> Namespace:
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
        TAP.diagnostic(
            'ambiguous license',
            'for more information see: https://github.com/pypa/trove-classifiers/issues/17',
        )
        TAP.diagnostic(
            f'set --license-expression to one of: {spdx_licenses}',
            'OR to a license expression based on one of these.',
        )
        TAP.not_ok('License', 'ambiguous per PEP 639', project.license)

    else:
        TAP.ok('License')
    return project


def license_expression(project: Namespace) -> Namespace:
    """PKG-INFO[PEP-639]:License-Expression"""
    project.license_expression = parse_spdx(project.license_expression)
    return project


def summary(project: Namespace) -> Namespace:
    """PKG-INFO:Summary"""
    if len(project.summary) > 512:
        TAP.not_ok('Summary', '>512 characters', 'PyPI limit')
    else:
        TAP.ok('Summary')
    return project


def keywords(project: Namespace) -> Namespace:
    """PKG-INFO:Keywords"""
    project.keywords = project.keywords.split(',')
    return project


def author_email(project: Namespace) -> Namespace:
    """PKG-INFO:Author-Email"""
    project.author_email, project.maintainer_email = parse_email(
        project.author_email,
        project.maintainer_email,
        project.verify_email,
    )
    return project


def maintainer_email(project: Namespace) -> Namespace:  # noqa: C901
    """PKG-INFO:Maintainer-Email,Author,Maintainer"""
    author_and_maintainer_email = False
    if set(project.author_email).intersection(project.maintainer_email):
        TAP.not_ok(
            'One or more Author-Email and Maintainer-Email are identical.',
            'Maintainer-Email should be empty',
        )
    elif any(map(len, project.maintainer_email)) and not any(map(len, project.author_email)):
        TAP.not_ok('Maintainer-Email', 'provided without setting Author-Email')
    elif any(map(len, project.maintainer_email)) and any(map(len, project.author_email)):
        author_and_maintainer_email = True
        TAP.ok('Author-Email(s) and Maintainter-Email(s) provided.')
    else:
        TAP.ok('Author-Email(s) provided.')

    if set(project.author_email).intersection(project.maintainer_email):
        TAP.not_ok(  # pragma: defer to good-issue
            'Author and Maintainer are identical',
            'Maintainer should be empty',
        )
    elif len(project.maintainer) and not len(project.author):
        TAP.not_ok('Maintainer', 'provided without setting Author')
    elif len(project.maintainer) and len(project.author):
        TAP.ok('Author and Maintainer provided.')
    elif author_and_maintainer_email and not len(project.maintainer):
        TAP.not_ok(  # pragma: defer to good issue
            'Maintainer-Email',
            'expected Maintainer name missing',
        )
    else:
        TAP.ok('Author provided.')
    return project


def name(project: Namespace) -> Namespace:
    """PKG-INFO:Name"""
    project.name = parse_project_name(project.name)
    return project


def home_page(project: Namespace) -> Namespace:
    """PKG-INFO:Home-page"""
    home_url = urlparse(project.home_page)
    if home_url.scheme != 'https':  # pragma: defer to good-issue
        TAP.not_ok('Home-page', 'url', 'scheme', 'unsupported')
    else:
        TAP.ok('Home-page', 'scheme')
    if home_url.netloc == '':  # pragma: defer to good-issue
        TAP.not_ok('Home-page url netloc could not be parsed.')
    else:
        TAP.ok('Home-page', 'netloc')
    return project


def project_url(project: Namespace) -> Namespace:
    """PKG-INFO:Project-URL"""
    for name, url in [str(i).split(',') for i in project.project_url]:
        if len(name) > 32:
            TAP.not_ok('Project-URL', 'name', 'too long', '>32 characters')
        else:
            TAP.ok('Project-URL', 'name')
        parsed_url = urlparse(url)
        if parsed_url.scheme != 'https':
            TAP.diagnostic('only https:// url scheme is supported')
            TAP.not_ok('Project-URL', 'url', 'scheme', 'unsupported')
        if parsed_url.netloc == '':
            TAP.not_ok('Project-URL', 'url', 'netloc', 'not parseable')
        else:
            TAP.ok('Project-URL', 'netloc')
    return project


def create_project_files(
    project: Namespace,
    env: Environment,
) -> None:
    """Create the actual project."""
    project.allow_file = set(map(Path, project.allow_file))
    iterdir = (i for i in project.target.iterdir() if i not in project.allow_file)
    if any(iterdir):  # defer to good-issue
        TAP.not_ok('target directory not empty', 'no files will be created', skip=True)
    else:
        project.ci_user = render_ci_files_set_user(env, project.target, project.ci_provider)
        render_project_files(env, project.target, project.name)


def compose(*functions: Composable) -> Composable:
    def inner(f: Composable, g: Composable) -> Composable:
        """The inner function to be reduced."""

        def result(x: Namespace) -> Namespace:
            """Result output"""
            return f(g(x))

        return result

    return reduce(inner, functions)


def project(project: Namespace) -> None:
    """Create a new project in a target directory."""
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
    if project.strict:
        with TAP.strict():  # pragma: no cover
            project = new_project(project)
    else:
        project = new_project(project)

    project.name = re.sub(r'[-_.]+', '-', project.name).lower()
    project.target = Path(project.target)
    project.topic = list(set(project.topic))
    project.dist_requires = list(set(project.dist_requires))
    env.globals = env.globals | {'project': vars(project)}
    create_project_files(project, env)


def wrap(project: Namespace) -> None:  # pragma: no cover
    """Create a new wrap file for publishing. Not a public function."""
    env.globals = env.globals | {'project': vars(project)}
    template = env.get_template('ozi.wrap.j2')
    with open('ozi.wrap', 'w') as f:
        f.write(template.render())


def main() -> NoReturn | None:  # pragma: no cover
    """Main ozi.new entrypoint."""
    ozi_new = parser.parse_args()
    ozi_new.argv = shlex.join(sys.argv[1:])
    match ozi_new:
        case ozi_new if ozi_new.new in ['p', 'project']:
            project(ozi_new)
            TAP.end()
        case ozi_new if ozi_new.new in ['w', 'wrap']:
            wrap(ozi_new)
            TAP.end()
        case _:
            parser.print_usage()
    return None


if __name__ == '__main__':
    main()
