# ozi/fix/missing.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
import re
import sys
from email import message_from_string
from email.message import Message  # noqa: TC003, RUF100
from pathlib import Path

if sys.version_info >= (3, 11):  # pragma: no cover
    import tomllib as toml
elif sys.version_info < (3, 11):  # pragma: no cover
    import tomli as toml


from ozi.filter import underscorify
from ozi.fix.build_definition import comment_diagnostic
from ozi.fix.build_definition import walk
from ozi.meson import load_ast
from ozi.meson import project_metadata
from ozi.pkg_extra import parse_extra_pkg_info
from ozi.spec import Metadata
from ozi.spec import PythonSupport
from ozi.tap import TAP

python_support = PythonSupport()
metadata = Metadata()


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


def missing_python_support(pkg_info: Message) -> set[tuple[str, str]]:  # pragma: no cover
    """Check PKG-INFO Message for python support."""
    remaining_pkg_info = {
        (k, v)
        for k, v in pkg_info.items()
        if k not in metadata.spec.python.pkg.info.required
    }
    for k, v in iter(python_support.classifiers[:4]):
        if (k, v) in remaining_pkg_info:
            TAP.ok(k, v)
        else:
            TAP.not_ok('MISSING', v)  # pragma: defer to good-issue
    return remaining_pkg_info


def missing_ozi_required(pkg_info: Message) -> dict[str, str]:  # pragma: no cover
    """Check missing required OZI extra PKG-INFO"""
    remaining_pkg_info = missing_python_support(pkg_info)
    remaining_pkg_info.difference_update(set(iter(python_support.classifiers)))
    for k, v in iter(remaining_pkg_info):
        TAP.ok(k, v)
    extra_pkg_info, errstr = parse_extra_pkg_info(pkg_info)
    if errstr not in ('', None):  # pragma: defer to good-issue
        TAP.not_ok('MISSING', str(errstr))
    return extra_pkg_info


def missing_required(
    target: Path,
) -> tuple[str, dict[str, str]]:
    """Find missing required PKG-INFO"""
    ast = load_ast(str(target))
    name = ''
    license_ = ''
    if ast:
        name, license_ = project_metadata(ast)
    with target.joinpath('pyproject.toml').open('rb') as f:
        setuptools_scm = toml.load(f).get('tool', {}).get('setuptools_scm', {})
        pkg_info = message_from_string(
            setuptools_scm.get('version_file_template', '@README_TEXT@')
            .replace(
                '@README_TEXT@',
                target.joinpath('README.rst').read_text(),
            )
            .replace('@PROJECT_NAME@', name)
            .replace('@LICENSE@', license_)
            .replace('@REQUIREMENTS_IN@\n', render_requirements(target))
            .replace('@SCM_VERSION@', '{version}'),
        )
        TAP.ok('setuptools_scm', 'PKG-INFO', 'template')
    for i in metadata.spec.python.pkg.info.required:
        v = pkg_info.get(i, None)
        if v is not None:
            TAP.ok(i, v)
        else:
            TAP.not_ok('MISSING', i)  # pragma: defer to good-issue
    extra_pkg_info = missing_ozi_required(pkg_info)  # pragma: defer to good-issue
    name = re.sub(
        r'[-_.]+',
        '-',
        pkg_info.get('Name', ''),
    ).lower()  # pragma: defer to good-issue
    for k, v in extra_pkg_info.items():  # pragma: defer to good-issue
        TAP.ok(k, v)
    return name, extra_pkg_info  # pragma: defer to good-issue


def missing_required_files(
    kind: str,
    target: Path,
    name: str,
) -> list[str]:  # pragma: no cover
    """Count missing files required by OZI"""
    found_files = []
    match kind:
        case 'test':
            rel_path = Path('tests')
            expected_files = metadata.spec.python.src.required.test
        case 'root':
            rel_path = Path('.')
            expected_files = metadata.spec.python.src.required.root
        case 'source':
            rel_path = Path(underscorify(name))
            expected_files = metadata.spec.python.src.required.source
        case _:  # pragma: no cover
            rel_path = Path('.')
            expected_files = ()
    for file in expected_files:
        f = rel_path / file
        if not target.joinpath(f).exists():
            TAP.not_ok('MISSING', str(f))
            continue  # pragma: defer to https://github.com/nedbat/coveragepy/issues/198
        if str(f).endswith('.py'):
            with open(target.joinpath(f)) as fh:
                comment_diagnostic(fh.readlines(), f)
        TAP.ok(str(f))
        found_files.append(file)
    walk(target, rel_path, found_files=found_files)
    return found_files


def report_missing(
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
        name, extra_pkg_info = missing_required(target)
    except FileNotFoundError:
        name = ''
        TAP.not_ok('MISSING', 'PKG-INFO')
    found_source_files = missing_required_files(
        'source',
        target,
        name,
    )  # pragma: defer to good-issue
    found_test_files = missing_required_files(
        'test',
        target,
        name,
    )  # pragma: defer to good-issue
    found_root_files = missing_required_files(
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
