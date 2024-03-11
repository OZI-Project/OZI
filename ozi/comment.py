# ozi/comment.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Linter comment check utilities."""
import re
from functools import lru_cache
from pathlib import Path  # noqa: TC003, RUF100
from typing import Generator
from typing import Sequence

from ozi.spec import METADATA
from ozi.tap import TAP


@lru_cache
def pattern_cache(key: str) -> re.Pattern[str]:
    """Cached OZI specification linter comment pattern lookup.

    :param key: key in :ref:`ozi.spec.CommentPatterns`
    :type key: str
    :return: compiled regular expression pattern
    :rtype: re.Pattern[str]
    """
    if pattern := METADATA.spec.python.src.comments.asdict().get(key):
        return re.compile(str(pattern).encode('raw_unicode_escape').decode('unicode_escape'))
    return re.Pattern()  # pragma: no cover


def pattern_search(
    line: str,
) -> Generator[tuple[str, str], None, None]:
    """Search for OZI specification comment patterns.

    :param line: line text verbatim
    :type line: str
    :yield: key, match for key in :ref:`ozi.spec.CommentPatterns` excluding ``help``
    :rtype: Generator[tuple[str, str], None, None]
    """
    for key in METADATA.spec.python.src.comments.asdict().keys():
        if found := key != 'help' and re.search(pattern_cache(key), line):
            yield key, found[0].strip()  # pragma: defer to TAP-Consumer


def diagnose(line: str, rel_path: Path, line_no: int) -> None:
    """Diagnose OZI comment pattern for a single line.

    :param line: line text verbatim
    :type line: str
    :param rel_path: file relative to OZI project root
    :type rel_path: Path
    :param line_no: current line number
    :type line_no: int
    """
    for key, found in pattern_search(line):
        TAP.diagnostic(
            key,
            f'{rel_path!s}:{line_no}',
            found,
        )  # pragma: defer to TAP-Consumer


def diagnostic(
    lines: Sequence[str],
    rel_path: Path,
    start: int = 1,
) -> None:
    """Diagnose OZI comment pattern for a sequence of lines.

    :param lines: lines to check
    :type lines: list[str]
    :param rel_path: file relative to OZI project root
    :type rel_path: Path
    :param start: starting line number for asynchronous chunking, defaults to 1
    :type start: int, optional
    """
    for line_no, line in enumerate(lines, start=start):
        diagnose(line, rel_path, line_no)
