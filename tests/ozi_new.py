# noqa: INP001
"""Unit and fuzz tests for ``ozi-new``."""
# Part of ozi.
# See LICENSE.txt in the project root for details.
import argparse
import operator
import typing
from datetime import timedelta
from itertools import zip_longest

import pytest
from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st

import ozi.assets
import ozi.fix
import ozi.new


@settings(
    deadline=timedelta(milliseconds=1000), suppress_health_check=[HealthCheck.too_slow]
)
@given(
    project=st.fixed_dictionaries(
        {
            'verify_email': st.just(False),
            'strict': st.just(False),
            'target': st.data(),
            'keywords': st.from_regex(r'^([a-z_]*[a-z0-9],)*$', fullmatch=True),
            'ci_provider': st.just('github'),
            'name': st.from_regex(
                r'^([A-Za-z]|[A-Za-z][A-Za-z0-9._-]*[A-Za-z0-9])$',
                fullmatch=True,
            ),
            'author': st.text(min_size=1, max_size=128),
            'author_email': st.lists(
                st.emails(domains=st.just('phony1.oziproject.dev')), max_size=8
            ),
            'maintainer': st.text(min_size=1, max_size=64),
            'maintainer_email': st.lists(
                st.emails(domains=st.just('phony2.oziproject.dev')), max_size=8
            ),
            'home_page': st.one_of(st.just('https://oziproject.dev/')),
            'project_url': st.lists(
                st.just('A, https://oziproject.dev'),
                max_size=1,
            ),
            'summary': st.text(max_size=512),
            'copyright_head': st.text(max_size=512),
            'license_file': st.just('LICENSE.txt'),
            'license_exception_id': st.one_of(
                list(map(st.just, ozi.new.CloseMatch.license_exception_id))
            ),
            'topic': st.one_of(list(map(st.just, ozi.new.CloseMatch.topic))),
            'audience': st.one_of(list(map(st.just, ozi.new.CloseMatch.audience))),
            'framework': st.one_of(list(map(st.just, ozi.new.CloseMatch.framework))),
            'environment': st.one_of(list(map(st.just, ozi.new.CloseMatch.environment))),
            'status': st.one_of(list(map(st.just, ozi.new.CloseMatch.status))),
            'dist_requires': st.lists(st.text(max_size=16)),
            'allow_file': st.just([]),
        },
    ),
    license=st.data(),
    license_expression=st.data(),
    license_id=st.data(),
)
def test_fuzz_new_project_good_namespace(  # noqa: DC102
    tmp_path_factory: pytest.TempPathFactory,
    project: typing.Dict,
    license: typing.Any,
    license_id: typing.Any,
    license_expression: typing.Any,
) -> None:
    assume(project['author_email'] != project['maintainer_email'])
    assume(len(project['author_email']))
    assume(
        map(
            operator.ne,
            *[
                i
                for i in zip_longest(project['author_email'], project['maintainer_email'])
                if any(i)
            ],
        )
    )
    assume(project['author'] != project['maintainer'])
    project['target'] = tmp_path_factory.mktemp('new_project_')
    project['license'] = license.draw(
        st.one_of(
            [
                st.just(k)
                for k, v in ozi.assets.spdx_options.items()
                if len(v) != 0 and k not in ['Private']
            ]
        )
    )
    project['license_id'] = license_id.draw(
        st.one_of(map(st.just, ozi.assets.spdx_options.get(project['license'])))  # type: ignore
    )
    project['license_expression'] = license_expression.draw(st.just(project['license_id']))
    namespace = argparse.Namespace(**project)
    ozi.new.new_project(project=namespace)


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
            'author': '',
            'maintainer': 'foo',
        },
        {
            'author': 'Zaphod Beeblebrox',
            'maintainer': '',
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
def test_new_project_bad_args(  # noqa: DC102
    item: dict,
    tmp_path_factory: pytest.TempPathFactory,
) -> None:
    project_dict = {
        'verify_email': False,
        'strict': False,
        'target': tmp_path_factory.mktemp('new_project_bad_args'),
        'ci_provider': 'github',
        'name': 'ozi.phony',
        'license': 'CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'author': 'Ross J. Duff',
        'author_email': ['noreply@oziproject.dev'],
        'keywords': '',
        'maintainer': '',
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
    }
    project_dict.update(item)
    namespace = argparse.Namespace(**project_dict)
    with pytest.warns(RuntimeWarning):
        ozi.new.new_project(project=namespace)


def test_new_project_bad_target_not_empty(  # noqa: DC102
    tmp_path_factory: pytest.TempPathFactory,
) -> None:
    project_dict = {
        'verify_email': False,
        'strict': False,
        'target': tmp_path_factory.mktemp('new_project_target_not_empty'),
        'ci_provider': 'github',
        'name': 'ozi.phony',
        'license': '',
        'keywords': '',
        'author': 'Ross J. Duff',
        'author_email': ['noreply@oziproject.dev'],
        'maintainer': '',
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
    }
    (project_dict['target'] / 'foobar').touch()
    namespace = argparse.Namespace(**project_dict)
    with pytest.warns(RuntimeWarning):
        ozi.new.new_project(project=namespace)


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
    dest=st.text(),
    nargs=st.one_of(st.none()),
    data=st.data(),
)
def test_fuzz_CloseMatch_nargs_None(  # noqa: DC102
    option_strings: str,
    dest: str,
    nargs: typing.Union[int, str, None],
    data: typing.Any,
) -> None:
    close_match = ozi.new.CloseMatch(option_strings=[option_strings], dest=dest, nargs=nargs)
    data = data.draw(
        st.sampled_from(
            close_match.__getattribute__(option_strings.lstrip('-').replace('-', '_'))
        )
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
    dest=st.text(),
    nargs=st.one_of(st.just('?')),
    data=st.data(),
)
def test_fuzz_CloseMatch_nargs_append(  # noqa: DC102
    option_strings: str,
    dest: str,
    nargs: typing.Union[int, str, None],
    data: typing.Any,
) -> None:
    close_match = ozi.new.CloseMatch(option_strings=[option_strings], dest=dest, nargs=nargs)
    data = data.draw(
        st.sampled_from(
            close_match.__getattribute__(option_strings.lstrip('-').replace('-', '_'))
        )
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
    dest=st.text(),
    nargs=st.one_of(st.just('?')),
    data=st.none(),
)
def test_fuzz_CloseMatch_nargs_append_None_values(  # noqa: DC102
    option_strings: str,
    dest: str,
    nargs: typing.Union[int, str, None],
    data: typing.Any,
) -> None:
    close_match = ozi.new.CloseMatch(option_strings=[option_strings], dest=dest, nargs=nargs)
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
    dest=st.text(),
    nargs=st.one_of(st.just('?')),
    data=st.text(min_size=100),
)
def test_fuzz_CloseMatch_nargs_append_warns(  # noqa: DC102
    option_strings: str,
    dest: str,
    nargs: typing.Union[int, str, None],
    data: typing.Any,
) -> None:
    close_match = ozi.new.CloseMatch(option_strings=[option_strings], dest=dest, nargs=nargs)
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
    dest=st.text(),
    nargs=st.one_of(st.just('*')),
    data=st.text(min_size=100),
)
def test_fuzz_CloseMatch_nargs_invalid(  # noqa: DC102
    option_strings: str,
    dest: str,
    nargs: typing.Union[int, str, None],
    data: typing.Any,
) -> None:
    with pytest.raises(ValueError, match='nargs'):
        ozi.new.CloseMatch(option_strings=[option_strings], dest=dest, nargs=nargs)


@given(
    msg=st.text(),
    category=st.just(Warning),
    filename=st.text(),
    lineno=st.integers(),
    line=st.one_of(st.none(), st.text()),
)
def test_fuzz_tap_warning_format(  # noqa: DC102
    msg: str, category: type, filename: str, lineno: int, line: typing.Optional[str]
) -> None:
    ozi.new.tap_warning_format(
        msg=msg, category=category, filename=filename, lineno=lineno, line=line
    )
