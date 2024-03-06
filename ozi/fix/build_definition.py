# ozi/fix/build_definition.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Build definition check utilities."""
import os
import re
import sys
from pathlib import Path

if sys.version_info >= (3, 11):  # pragma: no cover
    pass
elif sys.version_info < (3, 11):  # pragma: no cover
    pass

from ozi.meson import get_items_by_suffix
from ozi.meson import query_build_value
from ozi.spec import Metadata
from ozi.spec import PythonSupport
from ozi.tap import TAP

python_support = PythonSupport()

metadata = Metadata()


def comment_diagnostic(
    lines: list[str],
    rel_path: Path,
) -> None:  # pragma: defer to TAP-Consumer
    for i, line in enumerate(lines, start=1):
        if s := re.search(
            metadata.spec.python.src.comments.noqa.encode('raw_unicode_escape').decode(
                'unicode_escape',
            ),
            line,
        ):  # pragma: defer to TAP-Consumer
            TAP.diagnostic('noqa  ', f'{rel_path!s}:{i}', s[0].strip())
            continue
        if s := re.search(
            metadata.spec.python.src.comments.type.encode('raw_unicode_escape').decode(
                'unicode_escape',
            ),
            line,
        ):  # pragma: defer to TAP-Consumer
            TAP.diagnostic('type  ', f'{rel_path!s}:{i}', s[0].strip())
            continue
        if s := re.search(
            metadata.spec.python.src.comments.pragma_defer_to.encode(
                'raw_unicode_escape',
            ).decode('unicode_escape'),
            line,
        ):  # pragma: defer to TAP-Consumer
            TAP.diagnostic('defer ', f'{rel_path!s}:{i}', s[0].strip())
            continue
        if s := re.search(
            metadata.spec.python.src.comments.pragma_no_cover.encode(
                'raw_unicode_escape',
            ).decode('unicode_escape'),
            line,
        ):  # pragma: defer to TAP-Consumer
            TAP.diagnostic('no cov', f'{rel_path!s}:{i}', s[0].strip())
            continue


IGNORE_MISSING = {
    'subprojects',
    *metadata.spec.python.src.repo.hidden_dirs,
    *metadata.spec.python.src.repo.ignore_dirs,
    *metadata.spec.python.src.allow_files,
}


def process(
    target: Path,
    rel_path: Path,
    found_files: list[str] | None = None,
) -> None:  # pragma: no cover
    """Process an OZI project build definition's files."""
    extra_files = [
        file
        for file in os.listdir(target / rel_path)
        if os.path.isfile(target / rel_path / file)
    ]
    found_files = found_files if found_files else []
    extra_files = list(set(extra_files).symmetric_difference(set(found_files)))
    build_files = [str(rel_path / 'meson.build'), str(rel_path / 'meson.options')]
    for file in extra_files:  # pragma: no cover
        found_literal = query_build_value(
            str((target / rel_path / file).parent),
            file,
        )
        if found_literal:
            build_file = str((rel_path / file).parent / 'meson.build')
            TAP.ok(f'{build_file} lists {rel_path / file}')
            build_files += [str(rel_path / file)]
        if str(rel_path / file) not in build_files and file not in found_files:
            build_file = str(rel_path / 'meson.build')
            TAP.not_ok('MISSING', f'{build_file}: {rel_path / file!s}')
        if str(file).endswith('.py'):  # pragma: no cover
            with open(target.joinpath(rel_path) / file) as g:
                comment_diagnostic(g.readlines(), rel_path / file)


def walk(
    target: Path,
    rel_path: Path,
    found_files: list[str] | None = None,
) -> None:  # pragma: no cover
    """Walk an OZI standard build definition's directories."""
    subdirs = [
        directory
        for directory in os.listdir(target / rel_path)
        if os.path.isdir(target / rel_path / directory)
    ]
    children = get_items_by_suffix(str((target / rel_path)), 'children')
    for directory in subdirs:
        if children and directory in children:  # pragma: defer to good-issue
            TAP.ok(str(rel_path / 'meson.build'), 'subdir', str(directory))
            if rel_path != Path('.'):
                walk(target / rel_path, Path(directory))
        elif children and directory not in IGNORE_MISSING:  # pragma: defer to good-issue
            TAP.not_ok(
                str(rel_path / 'meson.build'),
                'subdir',
                str(directory),
                'MISSING',
                skip=True,
            )
        else:  # pragma: no cover
            TAP.ok(
                str(rel_path / 'meson.build'),
                'subdir',
                str(directory),
                'IGNORED',
                skip=True,
            )
    process(target, rel_path, found_files)
