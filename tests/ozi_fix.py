# noqa: INP001
"""Unit and fuzz tests for ``ozi-fix`` utility script"""
# Part of ozi.
# See LICENSE.txt in the project root for details.
import argparse
import os
import pathlib
from copy import deepcopy
from datetime import timedelta

import pytest
from hypothesis import given
from hypothesis import settings
from hypothesis import strategies as st

import ozi.assets
import ozi.fix
import ozi.new
from ozi.fix import env
from ozi.spec import Metadata

metadata = Metadata()

required_pkg_info_patterns = (
    'Author',
    'Author-email',
    'Description-Content-Type',
    'Home-page',
    'License',
    'License-Expression',
    'License-File',
    'Metadata-Version',
    'Name',
    'Programming Language :: Python',
    'Summary',
    'Version',
)

bad_namespace = argparse.Namespace(
    strict=False,
    verify_email=True,
    name='OZI-phony',
    keywords='foo,bar,baz',
    maintainer=[],
    maintainer_email=[],
    author=['foo'],
    author_email=['noreply@oziproject.dev'],
    home_page='foobar',
    summary='A' * 512,
    copyright_head='',
    license_expression='CC0-1.0',
    license_file='LICENSE.txt',
    license='CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
    license_id='ITWASAFICTION',
    license_exception_id='WEMADEITUP',
    topic=['Utilities'],
    status=['7 - Inactive'],
    environment=['Other Environment'],
    framework=['Pytest'],
    audience=['Other Audience'],
    ci_provider='github',
    project_url=['A' * 33 + ', https://oziproject.dev'],
    fix='',
    add=['ozi.phony'],
    remove=['ozi.phony'],
    dist_requires=[],
    allow_file=[],
)


@pytest.fixture()
def bad_project(tmp_path_factory: pytest.TempPathFactory) -> pathlib.Path:
    """Fixture to wrap the ``ozi-new project`` functionality."""
    fn = tmp_path_factory.mktemp('project_')
    namespace = deepcopy(bad_namespace)
    namespace.target = fn
    with pytest.warns(RuntimeWarning):
        ozi.new.project(namespace)
    return fn


@pytest.mark.parametrize('key', required_pkg_info_patterns)
def test_report_missing_required(bad_project: pathlib.Path, key: str) -> None:
    """Check that we warn on missing requirements"""
    with bad_project.joinpath('PKG-INFO').open() as f:
        content = f.read()
    with bad_project.joinpath('PKG-INFO').open('w') as f:
        content = content.replace(key, '')
        f.write(content)
    with pytest.raises(RuntimeWarning):
        ozi.fix.report_missing(bad_project)


@pytest.mark.parametrize(
    'key', [i for i in metadata.spec.python.src.required.root if i not in ['PKG-INFO']]
)
def test_report_missing_required_root_file(bad_project: pathlib.Path, key: str) -> None:
    """Check that we warn on missing files."""
    os.remove(bad_project.joinpath(key))
    with pytest.warns(RuntimeWarning):
        ozi.fix.report_missing(bad_project)


@pytest.mark.parametrize('key', ['PKG-INFO'])
def test_report_missing_required_pkg_info_file(bad_project: pathlib.Path, key: str) -> None:
    """Check that we warn on missing files."""
    os.remove(bad_project.joinpath(key))
    with pytest.raises((SystemExit, RuntimeWarning)):
        ozi.fix.report_missing(bad_project)


@pytest.mark.parametrize('key', metadata.spec.python.src.required.test)
def test_report_missing_required_test_file(bad_project: pathlib.Path, key: str) -> None:
    """Check that we warn on missing files."""
    os.remove(bad_project.joinpath('tests') / key)
    with pytest.warns(RuntimeWarning):
        ozi.fix.report_missing(bad_project)


@pytest.mark.parametrize('key', metadata.spec.python.src.required.source)
def test_report_missing_required_source_file(bad_project: pathlib.Path, key: str) -> None:
    """Check that we warn on missing files."""
    os.remove(bad_project.joinpath('ozi_phony') / key)
    with pytest.warns(RuntimeWarning):
        ozi.fix.report_missing(bad_project)


@given(
    type=st.just('target'),
    target=st.text(),
    operation=st.text(),
    sources=st.lists(st.text()),
    subdir=st.just(''),
    target_type=st.just('executable'),
)
def test_fuzz_RewriteCommand(
    type: str,
    target: str,
    operation: str,
    sources: list[str],
    subdir: str,
    target_type: str,
) -> None:
    ozi.fix.RewriteCommand(
        type=type,
        target=target,
        operation=operation,
        sources=sources,
        subdir=subdir,
        target_type=target_type,
    )


@given(
    target=st.just('.'),
    name=st.text(),
    fix=st.sampled_from(('test', 'source', 'root')),
    commands=st.lists(st.dictionaries(keys=st.text(), values=st.text())),
)
def test_fuzz_Rewriter(
    target: str,
    name: str,
    fix: str,
    commands: list[dict[str, str]],
) -> None:
    ozi.fix.Rewriter(target=target, name=name, fix=fix, commands=commands)


@pytest.mark.parametrize('fix', ['test', 'root', 'source'])
def test_Rewriter_bad_project__iadd__dir_nested_warns(
    bad_project: pytest.FixtureRequest,
    fix: str,
) -> None:
    env.globals = env.globals | {'project': vars(bad_namespace)}
    rewriter = ozi.fix.Rewriter(target=str(bad_project), name='ozi_phony', fix=fix)
    with pytest.warns(RuntimeWarning):
        rewriter += ['foo/foo/baz/']


@pytest.mark.parametrize('fix', ['test', 'root', 'source'])
def test_Rewriter_bad_project__iadd__dir(
    bad_project: pytest.FixtureRequest,
    fix: str,
) -> None:
    env.globals = env.globals | {'project': vars(bad_namespace)}
    rewriter = ozi.fix.Rewriter(target=str(bad_project), name='ozi_phony', fix=fix)
    rewriter += ['foo/']
    assert len(rewriter.commands) == 1


def test_Rewriter_bad_project__iadd__bad_fix(
    bad_project: pytest.FixtureRequest,
) -> None:
    env.globals = env.globals | {'project': vars(bad_namespace)}
    rewriter = ozi.fix.Rewriter(target=str(bad_project), name='ozi_phony', fix='')
    with pytest.warns(RuntimeWarning):
        rewriter += ['foo/']
    assert len(rewriter.commands) == 0


def test_Rewriter_bad_project__isub__bad_fix(
    bad_project: pytest.FixtureRequest,
) -> None:
    env.globals = env.globals | {'project': vars(bad_namespace)}
    rewriter = ozi.fix.Rewriter(target=str(bad_project), name='ozi_phony', fix='')
    rewriter -= ['foo.py']
    assert len(rewriter.commands) == 1


@pytest.mark.parametrize('fix', ['test', 'root', 'source'])
def test_Rewriter_bad_project__isub__non_existing_child(
    bad_project: pytest.FixtureRequest,
    fix: str,
) -> None:
    env.globals = env.globals | {'project': vars(bad_namespace)}
    rewriter = ozi.fix.Rewriter(target=str(bad_project), name='ozi_phony', fix=fix)
    with pytest.raises(RuntimeWarning):
        rewriter -= ['foo/']
    assert len(rewriter.commands) == 0


@pytest.mark.parametrize('fix', ['test', 'root', 'source'])
def test_Rewriter_bad_project__isub__child(
    bad_project: pytest.FixtureRequest,
    fix: str,
) -> None:
    env.globals = env.globals | {'project': vars(bad_namespace)}
    rewriter = ozi.fix.Rewriter(target=str(bad_project), name='ozi_phony', fix=fix)
    if fix == 'root':
        pathlib.Path(str(bad_project), 'foo').mkdir()
    elif fix == 'source':
        pathlib.Path(str(bad_project), 'ozi_phony', 'foo').mkdir()
    elif fix == 'test':
        pathlib.Path(str(bad_project), 'tests', 'foo').mkdir()
    rewriter -= ['foo/']
    assert len(rewriter.commands) == 1


@pytest.mark.parametrize('fix', ['test', 'root', 'source'])
def test_Rewriter_bad_project__isub__python_file(
    bad_project: pytest.FixtureRequest,
    fix: str,
) -> None:
    env.globals = env.globals | {'project': vars(bad_namespace)}
    rewriter = ozi.fix.Rewriter(target=str(bad_project), name='ozi_phony', fix=fix)
    if fix == 'root':
        pathlib.Path(str(bad_project), 'foo.py').touch()
    elif fix == 'source':
        pathlib.Path(str(bad_project), 'ozi_phony', 'foo.py').touch()
    elif fix == 'test':
        pathlib.Path(str(bad_project), 'tests', 'foo.py').touch()
    rewriter -= ['foo.py']
    assert len(rewriter.commands) == 1


@pytest.mark.parametrize('fix', ['test', 'root', 'source'])
def test_Rewriter_bad_project__isub__file(
    bad_project: pytest.FixtureRequest,
    fix: str,
) -> None:
    env.globals = env.globals | {'project': vars(bad_namespace)}
    rewriter = ozi.fix.Rewriter(target=str(bad_project), name='ozi_phony', fix=fix)
    if fix == 'root':
        pathlib.Path(str(bad_project), 'foo').touch()
    elif fix == 'source':
        pathlib.Path(str(bad_project), 'ozi_phony', 'foo').touch()
    elif fix == 'test':
        pathlib.Path(str(bad_project), 'tests', 'foo').touch()
    rewriter -= ['foo']
    assert len(rewriter.commands) == 1


@pytest.mark.parametrize('fix', ['test', 'root', 'source'])
def test_Rewriter_bad_project__iadd__file(
    bad_project: pytest.FixtureRequest,
    fix: str,
) -> None:
    env.globals.update({'project': vars(bad_namespace)})
    rewriter = ozi.fix.Rewriter(target=str(bad_project), name='ozi_phony', fix=fix)
    rewriter += ['foo.py']
    assert len(rewriter.commands) == 1


@pytest.mark.parametrize('fix', ['test', 'root', 'source'])
def test_Rewriter_bad_project__iadd__file_from_template(
    bad_project: pytest.FixtureRequest,
    fix: str,
) -> None:
    env.globals.update({'project': vars(bad_namespace)})
    rewriter = ozi.fix.Rewriter(target=str(bad_project), name='ozi_phony', fix=fix)
    pathlib.Path(bad_project / 'templates').mkdir()
    pathlib.Path(bad_project / 'templates' / 'foo.py').touch()
    pathlib.Path(bad_project / 'templates' / 'source').mkdir()
    pathlib.Path(bad_project / 'templates' / 'source' / 'foo.py').touch()
    pathlib.Path(bad_project / 'templates' / 'test').mkdir()
    pathlib.Path(bad_project / 'templates' / 'test' / 'foo.py').touch()
    rewriter += ['foo.py']
    assert len(rewriter.commands) == 1


@pytest.mark.parametrize('fix', ['test', 'root', 'source'])
def test_Rewriter_bad_project__iadd__non_python_file(
    bad_project: pytest.FixtureRequest,
    fix: str,
) -> None:
    env.globals.update({'project': vars(bad_namespace)})
    rewriter = ozi.fix.Rewriter(target=str(bad_project), name='ozi_phony', fix=fix)
    rewriter += ['foo']
    assert len(rewriter.commands) == 1


header = """.. OZI
  Classifier: License-Expression :: Apache-2.0 WITH LLVM-exception
  Classifier: License-File :: LICENSE.txt
"""


def test_preprocess_warns_non_existing_target() -> None:
    namespace = deepcopy(bad_namespace)
    namespace.target = 'temp/foobar'
    with pytest.warns(RuntimeWarning):
        ozi.fix.preprocess(namespace)


def test_preprocess_warns_file_target() -> None:
    namespace = deepcopy(bad_namespace)
    namespace.target = 'temp/foobar.txt'
    pathlib.Path(namespace.target).touch()
    with pytest.warns(RuntimeWarning):
        ozi.fix.preprocess(namespace)


def test_preprocess_existing_target() -> None:
    namespace = deepcopy(bad_namespace)
    namespace.target = '..'
    namespace = ozi.fix.preprocess(namespace)
    assert 'ozi.phony' not in namespace.add
    assert 'ozi.phony' not in namespace.remove


@given(add_items=st.lists(st.text()), remove_items=st.lists(st.text()))
def test_fuzz_preprocess_existing_target(
    add_items: list[str],
    remove_items: list[str],
) -> None:
    namespace = deepcopy(bad_namespace)
    namespace.add.extend(add_items)
    namespace.remove.extend(remove_items)
    namespace.target = '.'
    namespace = ozi.fix.preprocess(namespace)
    assert 'ozi.phony' not in namespace.add
    assert 'ozi.phony' not in namespace.remove


@settings(deadline=timedelta(milliseconds=500))
@given(payload=st.text(max_size=65535).map(header.__add__), as_message=st.booleans())
def test_fuzz_pkg_info_extra(payload: str, as_message: bool) -> None:
    ozi.assets.pkg_info_extra(payload=payload, as_message=as_message)


@given(s=st.from_regex(r'^([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9._-]*[A-Za-z0-9])$'))
def test_fuzz_underscorify(s: str) -> None:
    ozi.fix.underscorify(s=s)
