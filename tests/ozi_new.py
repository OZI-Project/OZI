# noqa: INP001
"""Unit and fuzz tests for ``ozi-new``."""
# Part of ozi.
# See LICENSE.txt in the project root for details.
import argparse
import pytest
import ozi.new
import typing
from hypothesis import given, strategies as st


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
        if data not in ['topic', 'status', None]:
            close_match(argparse.ArgumentParser(), argparse.Namespace(), data, f'--{data}')
        else:
            with pytest.raises(RuntimeWarning):
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
