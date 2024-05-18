# ozi/comment.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Linter comment check utilities."""
from __future__ import annotations

import re
from collections import Counter
from enum import IntFlag
from functools import lru_cache
from math import log
from math import log10
from typing import TYPE_CHECKING
from typing import Generator
from typing import Sequence

from ozi.spec import METADATA
from ozi.tap import TAP

if TYPE_CHECKING:
    from pathlib import Path

TIER3_COMMENTS = [
    'nosec',
    'pragma_defer_to',
    'pragma_no_cover',
    'type_ignore',
    'mypy',
    'pyright_ignore',
]
TIER2_COMMENTS = [
    'flake8_noqa',
    'noqa',
]
TIER1_COMMENTS = [
    'fmt_off',
    'fmt_on',
    'fmt_skip',
    'isort_dont_add_import',
    'isort_dont_add_imports',
    'isort_off',
    'isort_on',
    'isort_skip_file',
    'isort_split',
]


class CommentQuality(IntFlag):
    """Comment tiers for scoring project quality."""

    TIER1 = 11
    TIER2 = 2
    TIER3 = 1


def calculate_score(lines: int, t1: int, t2: int, t3: int) -> float:  # pragma: no cover
    """Calculate a quality score out of five.
    Comments have more impact on the score when lines is higher.

    :param lines: total line count
    :type lines: int
    :param t1: low-impact comments
    :type t1: int
    :param t2: intermediate-impact comments
    :type t2: int
    :param t3: high-impact comments
    :type t3: int
    :return: comment quality score out of 5.0
    :rtype: float
    """
    b = 5.0
    x = log(lines + 1, b) - log10(
        lines
        + 1
        ** (
            log10(CommentQuality.TIER3 + t3 + 1)
            - log10(CommentQuality.TIER3)
            + log10(log10(CommentQuality.TIER2 + t2 + 1))
            - log10(log10(CommentQuality.TIER2))
            + log10(log10(log10(CommentQuality.TIER1 + t1 + 1)))
            - log10(log10(log10(CommentQuality.TIER1)))
        ),
    )
    if x > 0:
        return b
    else:
        return round(b + x, 1)


@lru_cache
def pattern_cache(key: str) -> re.Pattern[str]:  # pragma: no cover
    """Cached OZI specification linter comment pattern lookup.

    :param key: key in :ref:`ozi.spec.CommentPatterns`
    :type key: str
    :return: compiled regular expression pattern
    :rtype: re.Pattern[str]
    """
    if pattern := METADATA.spec.python.src.comments.asdict().get(key):
        return re.compile(str(pattern).encode('raw_unicode_escape').decode('unicode_escape'))
    return re.Pattern()


def pattern_search(
    line: str,
) -> Generator[tuple[str, str], None, None]:  # pragma: defer to TAP-Consumer
    """Search for OZI specification comment patterns.

    :param line: line text verbatim
    :type line: str
    :yield: key, match for key in :ref:`ozi.spec.CommentPatterns` excluding ``help``
    :rtype: Generator[tuple[str, str], None, None]
    """
    for key in METADATA.spec.python.src.comments.asdict().keys():
        if found := key != 'help' and re.search(pattern_cache(key), line):
            yield key, found[0].strip()


def diagnose(line: str, rel_path: Path, line_no: int) -> Generator[str, None, None]:
    """Diagnose OZI comment pattern for a single line.

    :param line: line text verbatim
    :type line: str
    :param rel_path: file relative to OZI project root
    :type rel_path: Path
    :param line_no: current line number
    :type line_no: int
    """
    for key, found in pattern_search(line):  # pragma: defer to TAP-Consumer
        TAP.diagnostic(
            key,
            f'{rel_path!s}:{line_no}',
            found,
        )
        yield key


def diagnostic(  # pragma: no cover
    lines: Sequence[str],
    rel_path: Path,
    start: int = 1,
) -> Counter[str]:
    """Diagnose OZI comment pattern for a sequence of lines (usually a single file).

    :param lines: lines to check
    :type lines: list[str]
    :param rel_path: file relative to OZI project root
    :type rel_path: Path
    :param start: starting line number for asynchronous chunking, defaults to 1
    :type start: int, optional
    :rtype: Counter[str]
    :return: count of lines and comment pattern matches
    """
    count: Counter[str] = Counter()
    for line_no, line in enumerate(lines, start=start):
        count.update(Counter(lines=1))
        for key in diagnose(line, rel_path, line_no):
            count.update({key: 1})  # pragma: no cover
    return count


def score_file(rel_path: Path, count: Counter[str]) -> float:  # pragma: no cover
    """Score a single file comment diagnostic.

    :param rel_path: path to the file scored
    :type rel_path: Path
    :param count: count of lines and comments
    :type count: Counter[str]
    :return: file comment score out of 5.0
    :rtype: float
    """
    t1 = sum(count[i] for i in TIER1_COMMENTS)
    t2 = sum(count[i] for i in TIER2_COMMENTS)
    t3 = sum(count[i] for i in TIER3_COMMENTS)
    return calculate_score(count['lines'], t1, t2, t3)


def comment_diagnostic(target: Path, rel_path: Path, file: str) -> None:  # pragma: no cover
    """Run a scored comment diagnostic on a python file."""
    if str(file).endswith('.py'):
        with open(target.joinpath(rel_path) / file, 'r') as g:
            count = diagnostic(g.readlines(), rel_path / file)
            if count.total() > 0:
                TAP.diagnostic(
                    'comment_diagnostic',
                    str(rel_path / file),
                    *(f'{k}: {v}' for k, v in count.items()),
                )
            else:  # pragma: no cover
                pass
            TAP.diagnostic(
                'comment_diagnostic',
                str(rel_path / file),
                'quality score',
                f'{score_file(rel_path / file, count)}/5.0',
            )
