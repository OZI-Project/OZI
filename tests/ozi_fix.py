# noqa: INP001
"""Unit and fuzz tests for ``ozi-fix`` utility script"""
# Part of ozi.
# See LICENSE.txt in the project root for details.
import pytest
import ozi.fix
import pathlib
import typing
from hypothesis import given, strategies as st


@given(
    type=st.just('target'),
    target=st.text(),
    operation=st.text(),
    sources=st.lists(st.text()),
    subdir=st.just(''),
    target_type=st.just('executable'),
)
def test_fuzz_RewriteCommand(  # noqa: DC102
    type: str,
    target: str,
    operation: str,
    sources: typing.List[str],
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
    target=st.sampled_from(
        (
            'source_files',
            'source_children',
            'root_files',
            'root_children',
            'test_files',
            'test_children',
        )
    ),
    name=st.text(),
    fix=st.text(),
    commands=st.lists(st.dictionaries(keys=st.text(), values=st.text())),
)
def test_fuzz_Rewriter(  # noqa: DC102
    target: str, name: str, fix: str, commands: typing.List[typing.Dict[str, str]]
) -> None:
    ozi.fix.Rewriter(target=target, name=name, fix=fix, commands=commands)


header = """.. OZI
  Classifier: License-Expression :: Apache-2.0 WITH LLVM-exception
  Classifier: License-File :: LICENSE.txt
"""


@given(payload=st.text().map(header.__add__), as_message=st.booleans())
def test_fuzz_pkg_info_extra(payload: str, as_message: bool) -> None:  # noqa: DC102
    ozi.fix.pkg_info_extra(payload=payload, as_message=as_message)


@given(target=st.just('.'), strict=st.booleans(), use_tap=st.booleans())
def test_fuzz_report_missing(  # noqa: DC102
    target: pathlib.Path, strict: bool, use_tap: bool
) -> None:
    if use_tap:
        with pytest.raises(SystemExit):
            ozi.fix.report_missing(target=target, strict=strict, use_tap=use_tap)
    else:
        ozi.fix.report_missing(target=target, strict=strict, use_tap=use_tap)


@given(s=st.from_regex(r'^([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9._-]*[A-Za-z0-9])$'))
def test_fuzz_underscorify(s: str) -> None:  # noqa: DC102
    ozi.fix.underscorify(s=s)
