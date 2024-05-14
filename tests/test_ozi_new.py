# noqa: INP001
"""Unit and fuzz tests for ``ozi-new``."""
# Part of ozi.
# See LICENSE.txt in the project root for details.
from __future__ import annotations

import argparse
import typing
from datetime import timedelta

import pytest
from blastpipe.ozi_templates import load_environment  # pyright: ignore
from hypothesis import HealthCheck
from hypothesis import given
from hypothesis import settings
from hypothesis import strategies as st

import ozi.actions  # pyright: ignore
import ozi.new.__main__  # pyright: ignore
from ozi.fix.missing import required_files  # pyright: ignore
from ozi.fix.missing import required_pkg_info  # pyright: ignore
from ozi.spec import METADATA  # pyright: ignore
from ozi.tap import TAP  # pyright: ignore


@settings(
    suppress_health_check=[HealthCheck.too_slow],
    deadline=timedelta(seconds=30),
)
@given(
    project=st.fixed_dictionaries(
        {
            'verify_email': st.just(False),
            'strict': st.booleans(),
            'target': st.data(),
            'keywords': st.from_regex(r'^(([a-z_]*[a-z0-9],)*){2,650}$', fullmatch=True),
            'ci_provider': st.just('github'),
            'name': st.from_regex(
                r'^([A-Za-z]|[A-Za-z][A-Za-z0-9._-]*[A-Za-z0-9]){1,80}$',
                fullmatch=True,
            ),
            'author': st.lists(
                st.text(
                    st.characters(exclude_categories=['C'], exclude_characters='\\"'),
                    min_size=1,
                    max_size=16,
                ),
                min_size=1,
                max_size=8,
                unique=True,
            ),
            'author_email': st.lists(
                st.emails(domains=st.just('phony1.oziproject.dev')),
                min_size=1,
                max_size=8,
            ),
            'maintainer': st.lists(
                st.text(
                    st.characters(exclude_categories=['C'], exclude_characters='\\"'),
                    min_size=1,
                    max_size=16,
                ),
                min_size=1,
                max_size=8,
                unique=True,
            ),
            'maintainer_email': st.lists(
                st.emails(domains=st.just('phony2.oziproject.dev')),
                max_size=8,
            ),
            'home_page': st.one_of(st.just('https://oziproject.dev/')),
            'project_url': st.lists(
                st.just('A, https://oziproject.dev'),
                max_size=1,
            ),
            'summary': st.text(
                st.characters(exclude_categories=['C'], exclude_characters='\\"'),
                max_size=255,
            ),
            'copyright_head': st.text(
                st.characters(exclude_categories=['C'], exclude_characters='\\"'),
                max_size=255,
            ),
            'license_file': st.just('LICENSE.txt'),
            'license_exception_id': st.one_of(
                list(map(st.just, ozi.actions.ExactMatch().license_exception_id)),  # type: ignore
            ),
            'topic': st.lists(st.sampled_from(list(map(st.just, ozi.actions.ExactMatch().topic)))),  # type: ignore
            'audience': st.lists(
                st.sampled_from(list(map(st.just, ozi.actions.ExactMatch().audience))),  # type: ignore
            ),
            'framework': st.lists(
                st.sampled_from(list(map(st.just, ozi.actions.ExactMatch().framework))),  # type: ignore
            ),
            'environment': st.lists(
                st.sampled_from(list(map(st.just, ozi.actions.ExactMatch().environment))),  # type: ignore
            ),
            'status': st.lists(
                st.sampled_from(list(map(st.just, ozi.actions.ExactMatch().status))),  # type: ignore
            ),
            'dist_requires': st.lists(
                st.from_regex(
                    r'^([A-Za-z]|[A-Za-z][A-Za-z0-9._-]*[A-Za-z0-9]){1,80}$',
                    fullmatch=True,
                ),
            ),
            'allow_file': st.just([]),
            'license': st.one_of(
                [
                    st.just(k)
                    for k in METADATA.spec.python.pkg.license.ambiguous.keys()
                    if k not in ['Private']
                ],
            ),
            'long_description_content_type': st.sampled_from(['rst', 'md', 'txt']),
        },
    ),
    license_expression=st.data(),
    license_id=st.data(),
)
def test_fuzz_new_project_good_namespace(  # noqa: DC102, RUF100
    tmp_path_factory: pytest.TempPathFactory,
    project: dict[str, typing.Any],
    license_id: typing.Any,
    license_expression: typing.Any,
) -> None:
    project['target'] = tmp_path_factory.mktemp('new_project_')
    project['license_id'] = license_id.draw(
        st.one_of(map(st.just, METADATA.spec.python.pkg.license.ambiguous.get(project['license']))),  # type: ignore
    )
    project['license_expression'] = license_expression.draw(st.just(project['license_id']))
    namespace = argparse.Namespace(**project)
    preprocessed = ozi.new.__main__.preprocess_arguments(namespace)
    postprocessed = ozi.new.__main__.postprocess_arguments(preprocessed)
    ozi.new.__main__.create_project_files(
        postprocessed,
        env=load_environment(vars(postprocessed), METADATA.asdict()),
    )
    name, _ = required_pkg_info(postprocessed.target)
    required_files('root', postprocessed.target, postprocessed.name)
    required_files('test', postprocessed.target, postprocessed.name)
    required_files(
        'source',
        postprocessed.target,
        postprocessed.name,
    )
    with pytest.raises(SystemExit):
        TAP.end()


@pytest.mark.parametrize(
    'item',
    [
        {'ci_provider': ''},
        {'summary': 'A' * 513},
        {'name': 'OZI Phony'},
        {
            'license': 'DFSG approved',
            'license_expression': 'Private',
            'license_id': 'Private',
        },
        {'author_email': ['foobarbademail']},
        {
            'author_email': ['noreply@oziproject.dev'],
            'maintainer_email': ['noreply@oziproject.dev'],
        },
        {
            'author_email': [],
            'maintainer_email': ['noreply@oziproject.dev'],
        },
        {
            'author': [],
            'maintainer': ['foo'],
        },
        {
            'author': ['Zaphod Beeblebrox'],
            'maintainer': [],
            'author_email': ['noreply@oziproject.dev'],
            'maintainer_email': ['user@example.com'],
        },
        {
            'project_url': [('A' * 33 + ', https://oziproject.dev')],
        },
        {
            'project_url': [('A' * 32 + ', http://oziproject.dev')],
        },
        {
            'project_url': [('A' * 32 + ', https://')],
        },
    ],
)
def test_new_project_bad_args(  # noqa: DC102, RUF100
    item: dict[str, typing.Any],
    tmp_path_factory: pytest.TempPathFactory,
) -> None:
    project_dict = {
        'verify_email': False,
        'strict': False,
        'target': tmp_path_factory.mktemp('new_project_bad_args'),
        'ci_provider': 'github',
        'name': 'ozi.phony',
        'license': 'CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'author': ['Eden Ross Duff'],
        'author_email': ['noreply@oziproject.dev'],
        'keywords': 'foo,bar,baz',
        'maintainer': [],
        'maintainer_email': [],
        'home_page': 'https://oziproject.dev/',
        'project_url': [],
        'summary': '',
        'copyright_head': '',
        'license_expression': 'CC0-1.0',
        'license_id': 'CC0-1.0',
        'license_file': 'LICENSE.txt',
        'license_exception_id': '',
        'topic': ['Utilities'],
        'audience': ['Developers'],
        'framework': ['Pytest'],
        'environment': ['No Input/Output (Daemon)'],
        'status': ['1 - Planning'],
        'dist_requires': [],
        'allow_file': [],
        'long_description_content_type': 'rst',
    }
    project_dict.update(item)
    namespace = argparse.Namespace(**project_dict)
    with pytest.raises(RuntimeWarning):
        ozi.new.__main__.postprocess_arguments(
            ozi.new.__main__.preprocess_arguments(namespace),
        )


def test_new_project_bad_target_not_empty(  # noqa: DC102, RUF100
    tmp_path_factory: pytest.TempPathFactory,
) -> None:
    project_dict = {
        'verify_email': False,
        'strict': False,
        'target': tmp_path_factory.mktemp('new_project_target_not_empty'),
        'ci_provider': 'github',
        'name': 'ozi.phony',
        'license': '',
        'keywords': 'baz,bar,foo',
        'author': ['Eden Ross Duff'],
        'author_email': ['noreply@oziproject.dev'],
        'maintainer': [],
        'maintainer_email': [],
        'home_page': 'https://oziproject.dev/',
        'summary': '',
        'copyright_head': '',
        'project_url': [],
        'license_expression': 'CC0-1.0',
        'license_file': 'LICENSE.txt',
        'license_id': 'CC0-1.0',
        'license_exception_id': '',
        'topic': ['Utilities'],
        'audience': ['Developers'],
        'framework': ['Pytest'],
        'environment': ['No Input/Output (Daemon)'],
        'status': ['1 - Planning'],
        'dist_requires': [],
        'allow_file': [],
        'long_description_content_type': 'rst',
    }
    (project_dict['target'] / 'foobar').touch()  # type: ignore
    namespace = argparse.Namespace(**project_dict)
    with pytest.raises(RuntimeWarning):
        ozi.new.__main__.postprocess_arguments(
            ozi.new.__main__.preprocess_arguments(namespace),
        )


@settings(deadline=timedelta(milliseconds=500))
@given(
    option_strings=st.one_of(
        st.just('--license'),
        st.just('--environment'),
        st.just('--framework'),
        st.just('--license-id'),
        st.just('--license-exception-id'),
        st.just('--audience'),
        st.just('--language'),
        st.just('--topic'),
        st.just('--status'),
    ),
    dest=st.text(min_size=1, max_size=20),
    nargs=st.one_of(st.none()),
    data=st.data(),
)
def test_fuzz_CloseMatch_nargs_None(  # noqa: N802, DC102, RUF100
    option_strings: str,
    dest: str,
    nargs: int | str | None,
    data: typing.Any,
) -> None:
    close_match = ozi.actions.CloseMatch(
        option_strings=[option_strings],
        dest=dest,
        nargs=nargs,
    )
    data = data.draw(
        st.sampled_from(
            ozi.actions.ExactMatch().__getattribute__(
                option_strings.lstrip('-').replace('-', '_'),
            ),
        ),
    )
    close_match(argparse.ArgumentParser(), argparse.Namespace(), data, option_strings)


@settings(deadline=timedelta(milliseconds=500))
@given(
    option_strings=st.one_of(
        st.just('--license'),
        st.just('--environment'),
        st.just('--framework'),
        st.just('--license-id'),
        st.just('--license-exception-id'),
        st.just('--audience'),
        st.just('--language'),
        st.just('--topic'),
        st.just('--status'),
    ),
    dest=st.text(min_size=1, max_size=20),
    nargs=st.one_of(st.just('?')),
    data=st.data(),
)
def test_fuzz_CloseMatch_nargs_append(  # noqa: N802, DC102, RUF100
    option_strings: str,
    dest: str,
    nargs: int | str | None,
    data: typing.Any,
) -> None:
    close_match = ozi.actions.CloseMatch(
        option_strings=[option_strings],
        dest=dest,
        nargs=nargs,
    )
    data = data.draw(
        st.sampled_from(
            ozi.actions.ExactMatch().__getattribute__(
                option_strings.lstrip('-').replace('-', '_'),
            ),
        ),
    )
    close_match(argparse.ArgumentParser(), argparse.Namespace(), [data], option_strings)


@given(
    option_strings=st.one_of(
        st.just('--license'),
        st.just('--environment'),
        st.just('--framework'),
        st.just('--license-id'),
        st.just('--license-exception-id'),
        st.just('--audience'),
        st.just('--language'),
        st.just('--topic'),
        st.just('--status'),
    ),
    dest=st.text(min_size=1, max_size=20),
    nargs=st.one_of(st.just('?')),
    data=st.none(),
)
def test_fuzz_CloseMatch_nargs_append_None_values(  # noqa: N802, DC102, RUF100
    option_strings: str,
    dest: str,
    nargs: int | str | None,
    data: typing.Any,
) -> None:
    close_match = ozi.actions.CloseMatch(
        option_strings=[option_strings],
        dest=dest,
        nargs=nargs,
    )
    close_match(argparse.ArgumentParser(), argparse.Namespace(), data, option_strings)


@settings(deadline=timedelta(milliseconds=500))
@given(
    option_strings=st.one_of(
        st.just('--license'),
        st.just('--environment'),
        st.just('--framework'),
        st.just('--license-id'),
        st.just('--license-exception-id'),
        st.just('--audience'),
        st.just('--language'),
        st.just('--topic'),
        st.just('--status'),
    ),
    dest=st.text(min_size=1, max_size=20),
    nargs=st.one_of(st.just('?')),
    data=st.text(min_size=10, max_size=80),
)
def test_fuzz_CloseMatch_nargs_append_warns(  # noqa: N802, DC102, RUF100
    option_strings: str,
    dest: str,
    nargs: int | str | None,
    data: typing.Any,
) -> None:
    close_match = ozi.actions.CloseMatch(
        option_strings=[option_strings],
        dest=dest,
        nargs=nargs,
    )
    with pytest.warns(RuntimeWarning):
        close_match(argparse.ArgumentParser(), argparse.Namespace(), [data], option_strings)


@settings(deadline=timedelta(milliseconds=500))
@given(
    option_strings=st.one_of(
        st.just('--license'),
        st.just('--environment'),
        st.just('--framework'),
        st.just('--license-id'),
        st.just('--license-exception-id'),
        st.just('--audience'),
        st.just('--language'),
        st.just('--topic'),
        st.just('--status'),
    ),
    dest=st.text(min_size=1, max_size=20),
    nargs=st.one_of(st.just('*')),
    data=st.text(min_size=10, max_size=80),
)
def test_fuzz_CloseMatch_nargs_invalid(  # noqa: N802, DC102, RUF100
    option_strings: str,
    dest: str,
    nargs: int | str | None,
    data: typing.Any,
) -> None:
    with pytest.raises(ValueError, match='nargs'):
        ozi.actions.CloseMatch(option_strings=[option_strings], dest=dest, nargs=nargs)
