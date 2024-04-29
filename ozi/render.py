# ozi/render.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Rendering utilities for the OZI project templates.

.. versionremoved:: 1.2
   The function ``load_environment`` was moved to ``blastpipe.ozi_templates``

"""
from pathlib import Path
from warnings import warn

from blastpipe.ozi_templates.filter import underscorify  # pyright: ignore
from git import InvalidGitRepositoryError
from git import Repo
from jinja2 import Environment
from jinja2 import TemplateNotFound

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
        except TemplateNotFound:  # pragma: defer to good-first-issue
            content = f'template "{filename}" failed to render.'
            warn(content, RuntimeWarning, stacklevel=0)
        with open(target / filename, 'w') as f:
            f.write(content)

    for filename in templates.source:
        template = env.get_template(f'{filename}.j2')
        filename = filename.replace('project.name', underscorify(name).lower())
        with open(target / filename, 'w') as f:
            f.write(template.render())

    for filename in templates.test:
        template = env.get_template(f'{filename}.j2')
        with open(target / filename, 'w') as f:
            f.write(template.render())

    template = env.get_template('project.ozi.wrap.j2')
    with open(target / 'subprojects' / 'ozi.wrap', 'w') as f:
        f.write(template.render())
