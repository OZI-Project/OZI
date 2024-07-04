# ozi/new/__main__.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""ozi-new entrypoint script."""
from __future__ import annotations

import re
import shlex
import sys
from itertools import chain
from pathlib import Path
from typing import TYPE_CHECKING

from ozi_spec import METADATA  # pyright: ignore
from ozi_templates import load_environment  # type: ignore
from tap_producer import TAP

from ozi.new.interactive import interactive_prompt
from ozi.new.parser import parser
from ozi.new.validate import valid_classifier
from ozi.new.validate import valid_contact_info
from ozi.new.validate import valid_copyright_head
from ozi.new.validate import valid_emails
from ozi.new.validate import valid_home_page
from ozi.new.validate import valid_license
from ozi.new.validate import valid_project_name
from ozi.new.validate import valid_project_url
from ozi.new.validate import valid_spdx
from ozi.new.validate import valid_summary
from ozi.render import render_ci_files_set_user
from ozi.render import render_project_files

if TYPE_CHECKING:
    from argparse import Namespace
    from typing import Callable
    from typing import TypeAlias

    from jinja2 import Environment

    Composable: TypeAlias = Callable[[Namespace], Namespace]


def create_project_files(
    project: Namespace,
    env: Environment,
) -> None:
    """Create the actual project."""
    project.allow_file = set(map(Path, project.allow_file))
    project.ci_user = render_ci_files_set_user(env, project.target, project.ci_provider)
    render_project_files(env, project.target, project.name)
    if project.ci_provider == 'github':
        Path(
            project.target,
            f'README.{project.long_description_content_type}',
        ).symlink_to(Path(project.target, 'README'))
    else:  # pragma: no cover
        pass


def _valid_project(project: Namespace) -> Namespace:
    """Validate a project namespace."""
    valid_project_name(name=project.name)
    valid_summary(project.summary)
    project.license = valid_license(
        _license=project.license,
        license_expression=project.license_expression,
    )
    valid_home_page(home_page=project.home_page)
    valid_project_url(project_url=project.project_url)
    project.copyright_head = valid_copyright_head(
        copyright_head=project.copyright_head,
        project_name=project.name,
        license_file=project.license_file,
    )
    valid_spdx(project.license_expression)
    valid_contact_info(
        author=project.author,
        maintainer=project.maintainer,
        author_email=project.author_email,
        maintainer_email=project.maintainer_email,
    )
    for i in [
        project.audience,
        project.environment,
        project.framework,
        project.topic,
    ]:
        for classifier in i:
            valid_classifier(classifier)
    return project


def preprocess_arguments(project: Namespace) -> Namespace:
    """Preprocess (validate) arguments for project namespace."""
    if project.strict:
        with TAP.strict():  # pragma: no cover
            return _valid_project(project)
    else:
        return _valid_project(project)


def postprocess_arguments(project: Namespace) -> Namespace:
    """Postprocess (normalize) arguments for project namespace."""
    project.author_email, project.maintainer_email = valid_emails(
        author_email=project.author_email,
        maintainer_email=project.maintainer_email,
        verify=project.verify_email,
    )
    project.keywords = project.keywords.split(',')
    project.name = re.sub(r'[-_.]+', '-', project.name)
    project.target = Path(project.target)
    project.topic = list(set(project.topic))
    project.dist_requires = list(set(project.dist_requires))
    if any(
        i for i in project.target.iterdir() if i not in project.allow_file
    ):  # defer to good-issue
        TAP.not_ok('target directory not empty', 'no files will be created', skip=True)
    match project.ci_provider:
        case 'github':  # pragma: no cover
            pass
        case _:
            TAP.not_ok(
                f'--ci-provider "{project.ci_provider}" unrecognized. ci_user will not be set.',
            )
    return project


def project(project: Namespace) -> None:
    """Create a new project in a target directory."""
    project = postprocess_arguments(preprocess_arguments(project))
    create_project_files(
        project=project,
        env=load_environment(vars(project), METADATA.asdict()),
    )


def wrap(project: Namespace) -> None:  # pragma: no cover
    """Create a new wrap file for publishing. Not a public function."""
    env = load_environment(vars(project), METADATA.asdict())
    template = env.get_template('ozi.wrap.j2')
    with open('ozi.wrap', 'w', encoding='UTF-8') as f:
        f.write(template.render())


def main(args: list[str] | None = None) -> None:  # pragma: no cover
    """Main ozi.new entrypoint."""
    pipe = sys.stdin if not sys.stdin.isatty() else None
    args = (
        list(chain.from_iterable([shlex.split(line.strip()) for line in pipe]))
        if pipe
        else args
    )
    ozi_new = parser.parse_args(args=args)
    ozi_new.argv = shlex.join(args) if args else shlex.join(sys.argv[1:])
    match ozi_new:
        case ozi_new if ozi_new.new in ['i', 'interactive']:
            args = interactive_prompt(ozi_new)
            ozi_new = parser.parse_args(args=args)
            main(args)
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
