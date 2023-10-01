# noqa: INP001
"""Unit and fuzz tests for ``ozi-new``."""
# Part of ozi.
# See LICENSE.txt in the project root for details.
import argparse
import typing

import pytest
from hypothesis import given
from hypothesis import strategies as st

import ozi.fix
import ozi.new


@given(
    project=st.fixed_dictionaries(
        {
            'verify_email': st.just(False),
            'strict': st.just(False),
            'target': st.just('.'),
            'name': st.from_regex(r'^([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9._-]*[A-Za-z0-9])$')
            | st.just('OZI~phony'),
            'author': st.text(max_size=128),
            'email': st.emails() | st.just('OZI.phony'),
            'homepage': st.one_of(
                st.just('https://oziproject.dev/'),
                st.just('http://oziproject.dev/'),
            ),
            'summary': st.text(max_size=512) | st.text(min_size=512),
            'copyright_head': st.text(),
            'license_expression': st.data(),
            'license': st.one_of(list(map(st.just, ozi.new.CloseMatch.license))),
            'license_id': st.one_of(list(map(st.just, ozi.new.CloseMatch.license_id))),
            'license_exception_id': st.one_of(
                list(map(st.just, ozi.new.CloseMatch.license_exception_id))
            ),
            'topic': st.one_of(list(map(st.just, ozi.new.CloseMatch.topic))),
            'audience': st.one_of(list(map(st.just, ozi.new.CloseMatch.audience))),
            'framework': st.one_of(list(map(st.just, ozi.new.CloseMatch.framework))),
            'environment': st.one_of(list(map(st.just, ozi.new.CloseMatch.environment))),
            'status': st.one_of(list(map(st.just, ozi.new.CloseMatch.status))),
        }
    ).map(lambda d: argparse.Namespace(**d))
)
def test_fuzz_new_project(project: argparse.Namespace) -> None:
    """Fuzz new project creation function."""
    project.license_expression = project.license_expression.draw(
        st.just(f'{project.license_id} WITH {project.license_exception_id}') | st.text()
    )
    if (
        project.license in ozi.new.ambiguous_licenses
        or len(project.summary) > 512
        or project.name == 'OZI~phony'
        or project.email == 'OZI.phony'
        or 'WITH' not in project.license_expression
        or project.homepage.startswith('http://')
    ):
        with pytest.warns(RuntimeWarning):
            ozi.new.new_project(project=project)
    else:
        ozi.new.new_project(project=project)


@given(
    option_strings=st.lists(st.from_regex(r'--[a-z]*-?[a-z*]')),
    dest=st.text(),
    nargs=st.one_of(st.none(), st.text()),
    data=st.one_of(
        st.just('license'),
        st.just('environment'),
        st.just('framework'),
        st.just('license-id'),
        st.just('license-exception-id'),
        st.just('audience'),
        st.just('language'),
        st.just('topic'),
        st.just('status'),
        st.none(),
    ),
)
def test_fuzz_CloseMatch(  # noqa: DC102
    option_strings: typing.List[str],
    dest: str,
    nargs: typing.Union[int, str, None],
    data: typing.Any,
) -> None:
    if nargs is not None:
        with pytest.raises(ValueError, match='nargs not allowed'):
            ozi.new.CloseMatch(option_strings=option_strings, dest=dest, nargs=nargs)
    else:
        close_match = ozi.new.CloseMatch(
            option_strings=option_strings, dest=dest, nargs=nargs
        )
        if data not in [None, 'topic', 'status']:
            close_match(argparse.ArgumentParser(), argparse.Namespace(), data, f'--{data}')
        else:
            with pytest.warns(RuntimeWarning):
                close_match(
                    argparse.ArgumentParser(),
                    argparse.Namespace(),
                    data,
                    f'--{data}' if data is not None else None,
                )


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
