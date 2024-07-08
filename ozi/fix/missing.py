# ozi/fix/missing.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Find missing OZI project files."""
from __future__ import annotations

import re
import sys
from email import message_from_string
from pathlib import Path
from typing import TYPE_CHECKING

from ozi_spec import METADATA  # pyright: ignore
from ozi_templates.filter import underscorify  # type: ignore
from tap_producer import TAP

from ozi.fix.build_definition import walk
from ozi.meson import load_ast
from ozi.meson import project_metadata
from ozi.pkg_extra import parse_extra_pkg_info

if sys.version_info >= (3, 11):  # pragma: no cover
    import tomllib as toml
elif sys.version_info < (3, 11):  # pragma: no cover
    import tomli as toml

if TYPE_CHECKING:
    from email.message import Message


def render_requirements(target: Path) -> str:
    """Render requirements.in as it would appear in PKG-INFO"""
    requirements = (
        r.partition('\u0023')[0]
        for r in filter(
            lambda r: not (r.startswith('\u0023') or r == '\n'),
            target.joinpath('requirements.in').read_text('utf-8').splitlines(),
        )
    )
    return ''.join([f'Requires-Dist: {req}\n' for req in requirements])


def render_pkg_info(target: Path, name: str, _license: str) -> Message:
    """Render PKG-INFO as it would be produced during packaging."""
    with target.joinpath('pyproject.toml').open('rb') as f:
        setuptools_scm = toml.load(f).get('tool', {}).get('setuptools_scm', {})
        return message_from_string(
            setuptools_scm.get('version_file_template', '@README_TEXT@')
            .replace(
                '@README_TEXT@',
                target.joinpath('README').read_text(),
            )
            .replace('@PROJECT_NAME@', name)
            .replace('@LICENSE@', _license)
            .replace('@REQUIREMENTS_IN@\n', render_requirements(target))
            .replace('@SCM_VERSION@', '{version}'),
        )


def python_support(pkg_info: Message) -> set[tuple[str, str]]:
    """Check PKG-INFO Message for python support."""
    remaining_pkg_info = {
        (k, v)
        for k, v in pkg_info.items()
        if k not in METADATA.spec.python.pkg.info.required
    }
    for k, v in iter(METADATA.ozi.python_support.classifiers[:4]):
        if (k, v) in remaining_pkg_info:  # pragma: no cover
            TAP.ok(k, v)
        else:
            TAP.not_ok('MISSING', v)  # pragma: defer to good-issue
    return remaining_pkg_info


def required_extra_pkg_info(pkg_info: Message) -> dict[str, str]:
    """Check missing required OZI extra PKG-INFO"""
    remaining_pkg_info = python_support(pkg_info)
    remaining_pkg_info.difference_update(set(iter(METADATA.ozi.python_support.classifiers)))
    for k, v in iter(remaining_pkg_info):
        TAP.ok(k, v)
    extra_pkg_info, errstr = parse_extra_pkg_info(pkg_info)
    if errstr not in ('', None):  # pragma: no cover
        TAP.not_ok('MISSING', str(errstr))
    return extra_pkg_info


def required_pkg_info(
    target: Path,
) -> tuple[str, dict[str, str]]:
    """Find missing required PKG-INFO"""
    ast = load_ast(str(target))
    name = ''
    license_ = ''
    if ast:
        name, license_ = project_metadata(ast)
    pkg_info = render_pkg_info(target, name, license_)
    TAP.ok('setuptools_scm', 'PKG-INFO', 'template')
    for i in METADATA.spec.python.pkg.info.required:
        v = pkg_info.get(i, None)
        if v is not None:
            TAP.ok(i, v)
        else:  # pragma: no cover
            TAP.not_ok('MISSING', i)
    extra_pkg_info = required_extra_pkg_info(pkg_info)
    name = re.sub(r'[-_.]+', '-', pkg_info.get('Name', '')).lower()
    for k, v in extra_pkg_info.items():  # pragma: no cover
        TAP.ok(k, v)
    return name, extra_pkg_info


def required_files(
    kind: str,
    target: Path,
    name: str,
) -> list[str]:
    """Count missing files required by OZI"""
    found_files = []
    match kind:
        case 'test':
            rel_path = Path('tests')
            expected_files = METADATA.spec.python.src.required.test
        case 'root':
            rel_path = Path('.')
            expected_files = METADATA.spec.python.src.required.root
        case 'source':
            rel_path = Path(underscorify(name).lower())
            expected_files = METADATA.spec.python.src.required.source
        case _:  # pragma: no cover
            rel_path = Path('.')
            expected_files = ()
    for file in expected_files:
        f = rel_path / file
        if not target.joinpath(f).exists():  # pragma: no cover
            TAP.not_ok('MISSING', str(f))
            continue  # pragma: defer to https://github.com/nedbat/coveragepy/issues/198
        TAP.ok(str(f))
        found_files.append(file)
    walk(target, rel_path, found_files=found_files, project_name=underscorify(name).lower())
    return found_files


def report(
    target: Path,
) -> tuple[str, Message | None, list[str], list[str], list[str]]:
    """Report missing OZI project files
    :param target: Relative path to target directory.
    :return: Normalized Name, PKG-INFO, found_root, found_sources, found_tests
    """
    target = Path(target)
    name = None
    pkg_info = None
    extra_pkg_info: dict[str, str] = {}
    try:
        name, extra_pkg_info = required_pkg_info(target)
    except FileNotFoundError:
        name = ''
        TAP.not_ok('MISSING', 'PKG-INFO')
    found_source_files = required_files(
        'source',
        target,
        name,
    )  # pragma: defer to good-issue
    found_test_files = required_files(
        'test',
        target,
        name,
    )  # pragma: defer to good-issue
    found_root_files = required_files(
        'root',
        target,
        name,
    )  # pragma: defer to good-issue
    all_files = (  # pragma: defer to TAP-Consumer
        ['PKG-INFO'],
        extra_pkg_info,
        found_root_files,
        found_source_files,
        found_test_files,
    )
    try:  # pragma: defer to TAP-Consumer
        sum(map(len, all_files))
    except TypeError:  # pragma: defer to TAP-Consumer
        TAP.bail_out('MISSING required files or metadata.')
    return (  # pragma: defer to TAP-Consumer
        name,
        pkg_info,
        found_root_files,
        found_source_files,
        found_test_files,
    )
