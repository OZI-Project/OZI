# ozi/render.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Rendering utilities for the OZI project templates.
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING
from typing import AnyStr
from typing import Literal
from warnings import warn

from blastpipe.ozi_templates.filter import underscorify  # pyright: ignore
from git import InvalidGitRepositoryError
from git import Repo

if TYPE_CHECKING:
    from jinja2 import Environment

from ozi.spec import METADATA
from ozi.tap import TAP


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
        with open(fp) as template:
            user_template = template.read()
    else:
        TAP.diagnostic('User tempate not found', str(fp))
        user_template = None
    return user_template


def map_to_template(
    fix: Literal['source', 'root', 'test'] | AnyStr,
    filename: str,
) -> str:
    """Map an appropriate template for an ozi-fix mode and filename.

    .. versionadded:: 1.5

    :param fix: ozi-fix mode setting
    :type fix: Literal['source', 'root', 'test'] | AnyStr
    :param filename: name with file extension
    :type filename: str
    :return: template path
    :rtype: str
    """
    match fix, filename:
        case ['test' | 'root', f] if f.endswith('.py'):
            x = 'tests/new_test.py.j2'
        case ['source', f] if f.endswith('.py'):
            x = 'project.name/new_module.py.j2'
        case ['source', f] if f.endswith('.pyx'):  # pragma: no cover
            x = 'project.name/new_ext.pyx.j2'
        case ['root', f]:
            x = f'{f}.j2'
        case ['source', f]:
            x = f'project.name/{f}.j2'
        case ['test', f]:
            x = f'tests/{f}.j2'
        case [_, _]:  # pragma: no cover
            x = ''
    return x


def build_file(
    env: Environment,
    fix: Literal['source', 'root', 'test'] | AnyStr,
    path: Path,
    user_template: str | None,
) -> None:
    """Render project file based on OZI templates.

    .. versionadded:: 1.5

    :param env: rendering environment
    :type env: Environment
    :param fix: ozi-fix setting
    :type fix: Literal['source', 'root', 'test'] | AnyStr
    :param path: full path of file to be rendered
    :type path: Path
    :param user_template: path to a user template to extend
    :type user_template: str | None
    """
    try:
        template = env.get_template(map_to_template(fix, path.name)).render(
            user_template=user_template,
        )
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
        with open((child / 'meson.build'), 'x') as f:
            f.write(env.get_template('new_child.j2').render(parent=parent))


def render_ci_files_set_user(env: Environment, target: Path, ci_provider: str) -> str:
    """Render CI files based on the ci_provider for target in env.

    :param env: the OZI project file rendering environment
    :type env: jinja2.Environment
    :param target: directory path to render the project
    :type target: Path
    :param ci_provider: the name of the project continuous integration provider
    :type ci_provider: str
    :return: the ci_user of the target repository for the continuous integration provider
    :rtype: str
    """
    match ci_provider:
        case 'github':
            try:
                ci_user = Repo(target).config_reader().get('user', 'name')
            except InvalidGitRepositoryError:
                ci_user = ''
            Path(target, '.github', 'workflows').mkdir(parents=True)
            template = env.get_template('github_workflows/ozi.yml.j2')
            with open(Path(target, '.github', 'workflows', 'ozi.yml'), 'w') as f:
                f.write(template.render())
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
    Path(target, underscorify(name)).mkdir()
    Path(target, 'subprojects').mkdir()
    Path(target, 'tests').mkdir()
    templates = METADATA.spec.python.src.template
    for filename in templates.root:
        template = env.get_template(f'{filename}.j2')
        try:
            content = template.render(filename=filename)
        except LookupError:  # pragma: defer to good-first-issue
            content = f'template "{filename}" failed to render.'
            warn(content, RuntimeWarning, stacklevel=0)
        with open(target / filename, 'w') as f:
            f.write(content)

    for filename in templates.source:
        filename = filename.replace('project.name', underscorify(name).lower())
        build_file(
            env,
            'source',
            target / filename,
            find_user_template(str(target), filename, 'source'),
        )

    for filename in templates.test:
        build_file(
            env,
            'test',
            target / filename,
            find_user_template(str(target), filename, 'test'),
        )

    template = env.get_template('project.ozi.wrap.j2')
    with open(target / 'subprojects' / 'ozi.wrap', 'w') as f:
        f.write(template.render())
