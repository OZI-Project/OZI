# ozi/render.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Rendering utilities for the OZI project templates.
"""
from __future__ import annotations

import configparser
from pathlib import Path
from typing import TYPE_CHECKING
from typing import AnyStr
from typing import Literal
from warnings import warn

from git import InvalidGitRepositoryError
from git import Repo
from ozi_spec import METADATA  # pyright: ignore
from ozi_templates.filter import underscorify  # type: ignore
from tap_producer import TAP

if TYPE_CHECKING:
    from jinja2 import Environment


def find_user_template(target: str, file: str, fix: str) -> str | None:
    """Find a user-defined project template file e.g. :file:`{target}/templates/{fix}/{file}`.

    :param target: path to an OZI project directory
    :type target: Path
    :param file: filename
    :type file: str
    :param fix: template directory fix path
    :type fix: str
    :return: a user-defined template as a string
    :rtype: str | None
    """
    fp = Path(target, 'templates', fix, file)
    if fp.exists():
        with open(fp, encoding='UTF-8') as template:
            user_template = template.read()
    else:
        TAP.diagnostic('User tempate not found', str(fp))
        user_template = None
    return user_template


def map_to_template(  # noqa: C901
    fix: (
        Literal[
            'child',
            'github_workflows',
            'root',
            'source',
            'subprojects',
            'templates',
            'test',
        ]
        | AnyStr
    ),
    filename: str,
) -> str:
    """Map an appropriate template for an ozi-fix mode and filename.

    .. versionadded:: 1.5

    :param fix: ozi-fix mode setting
    :type fix: AnyStr
    :param filename: name with file extension
    :type filename: str
    :return: template path
    :rtype: str
    """
    match fix, filename:
        case ['test' | 'root', f] if f.endswith('.py'):
            x: str = METADATA.spec.python.src.template.add_test
        case ['source', f] if f.endswith('.py'):
            x = METADATA.spec.python.src.template.add_source
        case ['source', f] if f.endswith('.pyx'):  # pragma: no cover
            x = 'project.name/new_ext.pyx.j2'
        case ['root', f]:
            x = f'{f}.j2'
        case ['source', f]:
            x = f'project.name/{f}.j2'
        case ['test', f]:
            x = f'tests/{f}.j2'
        case ['templates', f]:
            x = f'templates/{f}.j2'
        case ['subprojects', f]:
            x = f'subprojects/{f}.j2'
        case ['child', f]:
            x = 'new_child.j2'
        case ['github_workflows', f]:
            x = f'github_workflows/{f}.j2'
        case [_, _]:  # pragma: no cover
            x = ''
    return x


def build_file(
    env: Environment,
    fix: (
        Literal[
            'child',
            'github_workflows',
            'root',
            'source',
            'subprojects',
            'templates',
            'test',
        ]
        | AnyStr
    ),
    path: Path,
    user_template: str | None,
    **kwargs: str,
) -> None:
    """Render project file based on OZI templates.

    .. versionadded:: 1.5

    :param env: rendering environment
    :type env: Environment
    :param fix: ozi-fix setting
    :type fix: AnyStr
    :param path: full path of file to be rendered
    :type path: Path
    :param user_template: path to a user template to extend
    :type user_template: str | None
    """
    try:
        template = env.get_template(map_to_template(fix, path.name)).render(
            user_template=user_template,
            **kwargs,
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(template)
    except LookupError as e:
        warn(str(e), RuntimeWarning)


def build_child(env: Environment, parent: str, child: Path) -> None:
    """Add a child directory to a parent in an existing OZI-style project.

    :param env: the OZI project file rendering environment
    :type env: jinja2.Environment
    :param parent: existing directory name in project
    :type parent: str
    :param child: path to a new child directory
    :type child: Path
    """
    child.mkdir(parents=True)
    parent = parent.rstrip('/')
    heirs = parent.split('/')
    if len(heirs) > 1:
        warn(
            'Nested folder creation not supported.',
            RuntimeWarning,
            stacklevel=0,
        )
    else:
        build_file(
            env,
            'child',
            (child / 'meson.build'),
            find_user_template(str(parent / child), 'meson.build.j2', 'child'),
            parent=parent,
        )


def render_ci_files_set_user(env: Environment, target: Path, ci_provider: str) -> str:
    """Render :term:`CI` files based on the ci_provider for target in env.

    :param env: the OZI project file rendering environment
    :type env: jinja2.Environment
    :param target: directory path to render the project
    :type target: Path
    :param ci_provider: the name of the project continuous integration provider
    :type ci_provider: str
    :return: the ci_user of the target repository for the continuous integration provider
    :rtype: str
    """
    repo = Repo.init(target, mkdir=False)
    try:
        ci_user = repo.config_reader().get('user', 'name')
    except (InvalidGitRepositoryError, configparser.NoSectionError):  # pragma: no cover
        ci_user = ''

    match ci_provider:
        case 'github':
            for filename in METADATA.spec.python.src.template.ci_provider['github']:
                build_file(
                    env,
                    'github_workflows',
                    target / filename.replace('github_workflows', '.github/workflows'),
                    find_user_template(str(target), str(filename), 'github_workflows'),
                )
        case _:  # pragma: no cover
            ci_user = ''
    return ci_user


def render_project_files(env: Environment, target: Path, name: str) -> None:
    """Render the primary new project files(excluding CI).

    :param env: the OZI project file rendering environment
    :type env: jinja2.Environment
    :param target: directory path to render the project
    :type target: Path
    :param name: the canonical project name (without normalization)
    :type name: str
    """
    templates = METADATA.spec.python.src.template
    all_templates = [
        (i, getattr(templates, i))
        for i in ('root', 'test', 'source', 'templates', 'subprojects')
    ]
    for fix, files in all_templates:
        for filename in files:
            filename = (
                filename
                if fix != 'source'
                else filename.replace('project.name', underscorify(name).lower())
            )
            build_file(
                env,
                fix,
                target / filename,
                find_user_template(str(target), filename, fix),
            )
