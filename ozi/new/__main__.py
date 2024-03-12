# ozi/new/__main__.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""ozi-new entrypoint script."""
from __future__ import annotations

import re
import shlex
import sys
from functools import reduce
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from argparse import Namespace
    from typing import Callable
    from typing import TypeAlias

    from jinja2 import Environment

    Composable: TypeAlias = Callable[[Namespace], Namespace]

from ozi.new.parser import parser
from ozi.new.validate import valid_contact_info
from ozi.new.validate import valid_copyright_head
from ozi.new.validate import valid_emails
from ozi.new.validate import valid_home_page
from ozi.new.validate import valid_license
from ozi.new.validate import valid_project_name
from ozi.new.validate import valid_project_url
from ozi.new.validate import valid_spdx
from ozi.new.validate import valid_summary
from ozi.render import load_environment
from ozi.render import render_ci_files_set_user
from ozi.render import render_project_files
from ozi.tap import TAP


def copyright_head(project: Namespace) -> Namespace:
    """OZI:Copyright-Head"""
    project.copyright_head = valid_copyright_head(
        copyright_head=project.copyright_head,
        project_name=project.name,
        license_file=project.license_file,
    )
    return project


def license_(project: Namespace) -> Namespace:
    """PKG-INFO:License"""
    valid_license(
        _license=project.license,
        license_expression=project.license_expression,
    )
    return project


def license_expression(project: Namespace) -> Namespace:
    """PKG-INFO[PEP-639]:License-Expression"""
    project.license_expression = valid_spdx(project.license_expression)
    return project


def summary(project: Namespace) -> Namespace:
    """PKG-INFO:Summary"""
    valid_summary(project.summary)
    return project


def keywords(project: Namespace) -> Namespace:
    """PKG-INFO:Keywords"""
    project.keywords = project.keywords.split(',')
    return project


def contact_info(project: Namespace) -> Namespace:
    """PKG-INFO:Author-Email,Maintainer-Email,Author,Maintainer"""
    valid_contact_info(
        author=project.author,
        maintainer=project.maintainer,
        author_email=project.author_email,
        maintainer_email=project.maintainer_email,
    )
    project.author_email, project.maintainer_email = valid_emails(
        author_email=project.author_email,
        maintainer_email=project.maintainer_email,
        verify=project.verify_email,
    )
    return project


def name(project: Namespace) -> Namespace:
    """PKG-INFO:Name"""
    valid_project_name(name=project.name)
    return project


def home_page(project: Namespace) -> Namespace:
    """PKG-INFO:Home-page"""
    valid_home_page(home_page=project.home_page)
    return project


def project_url(project: Namespace) -> Namespace:
    """PKG-INFO:Project-URL"""
    valid_project_url(project_url=project.project_url)
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
    """Compose pure functions of :ref:`argparse.Namespace`"""

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
        name,
        summary,
        keywords,
        license_,
        home_page,
        project_url,
        contact_info,
        copyright_head,
        license_expression,
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
    env = load_environment(vars(project))
    create_project_files(project, env)


def wrap(project: Namespace) -> None:  # pragma: no cover
    """Create a new wrap file for publishing. Not a public function."""
    env = load_environment(vars(project))
    template = env.get_template('ozi.wrap.j2')
    with open('ozi.wrap', 'w') as f:
        f.write(template.render())


def main() -> None:  # pragma: no cover
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
