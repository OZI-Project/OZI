# ozi/fix/build_definition.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Build definition check utilities."""
import os
from pathlib import Path
from typing import Generator

from ozi import comment
from ozi.meson import get_items_by_suffix
from ozi.meson import query_build_value
from ozi.spec import METADATA
from ozi.tap import TAP

IGNORE_MISSING = {
    'subprojects',
    *METADATA.spec.python.src.repo.hidden_dirs,
    *METADATA.spec.python.src.repo.ignore_dirs,
    *METADATA.spec.python.src.allow_files,
}


def inspect_files(
    target: Path,
    rel_path: Path,
    found_files: list[str],
    extra_files: list[str],
) -> None:
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
        comment.comment_diagnostic(target, rel_path, file)


def process(
    target: Path,
    rel_path: Path,
    found_files: list[str] | None = None,
) -> None:
    """Process an OZI project build definition's files."""
    extra_files = [
        file
        for file in os.listdir(target / rel_path)
        if os.path.isfile(target / rel_path / file)
    ]
    found_files = found_files if found_files else []
    extra_files = list(set(extra_files).symmetric_difference(set(found_files)))
    inspect_files(
        target=target,
        rel_path=rel_path,
        found_files=found_files,
        extra_files=extra_files,
    )


def validate(
    target: Path,
    rel_path: Path,
    subdirs: list[str],
    children: set[str] | None,
) -> Generator[Path, None, None]:
    """Validate an OZI standard build definition's directories."""
    for directory in subdirs:
        match directory, children:
            case directory, children if children and directory in children:
                TAP.ok(  # pragma: no cover
                    str(rel_path / 'meson.build'),
                    'subdir',
                    str(directory),
                )
            case directory, _ if directory not in IGNORE_MISSING:
                TAP.ok(
                    str(rel_path / 'meson.build'),
                    'subdir',
                    str(directory),
                )
                yield Path(rel_path / directory)
            case directory, _:
                TAP.ok(
                    str(rel_path / 'meson.build'),
                    'subdir',
                    str(directory),
                    skip=True,
                )
            case _:  # pragma: no cover
                TAP.diagnostic('build_definition.validate', 'invalid arguments')


def walk(
    target: Path,
    rel_path: Path,
    found_files: list[str] | None = None,
) -> None:
    """Walk an OZI standard build definition's directories."""
    children = list(
        validate(
            target,
            rel_path,
            subdirs=[
                directory
                for directory in os.listdir(target / rel_path)
                if os.path.isdir(target / rel_path / directory)
            ],
            children=get_items_by_suffix(str((target / rel_path)), 'children'),
        ),
    )
    process(target, rel_path, found_files)
    for child in children:
        walk(target, child)
