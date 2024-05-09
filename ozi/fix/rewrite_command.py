# ozi/fix/rewrite_command.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Primitives for generating meson rewrite commands."""
from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Annotated
from typing import Union
from warnings import warn

from ozi.render import build_child
from ozi.render import build_file
from ozi.render import find_user_template

if TYPE_CHECKING:
    import sys
    from collections.abc import Callable
    from collections.abc import Mapping

    from jinja2 import Environment
    from jinja2 import Template

    if sys.version_info >= (3, 11):
        from typing import Self
    elif sys.version_info < (3, 11):
        from typing_extensions import Self

from ozi.spec import METADATA


@dataclass
class RewriteCommand:  # pragma: defer to meson
    """Meson rewriter command input"""

    active: bool = field(repr=False, default_factory=bool, init=False)
    type: str = 'target'
    target: str = ''
    operation: str = ''
    sources: list[str] = field(default_factory=list)
    subdir: str = ''
    target_type: str = 'executable'

    def add(
        self: RewriteCommand,
        mode: str,
        kind: str,
        source: str,
    ) -> dict[str, Union[str, list[str]]]:
        """Add sources and tests to an OZI project."""
        self.sources += [source]
        self.operation = 'src_add'
        return self._body(mode, kind)

    def rem(
        self: RewriteCommand,
        mode: str,
        kind: str,
        source: str,
    ) -> dict[str, Union[str, list[str]]]:
        """Add sources and tests to an OZI project."""
        self.sources += [source]
        self.operation = 'src_rem'
        return self._body(mode, kind)

    def _body(
        self: RewriteCommand,
        mode: str,
        kind: str,
    ) -> dict[str, Union[str, list[str]]]:
        """The body of the add/rem functions"""
        self.active = True
        target = mode + '_' + kind
        mode_set = self.target == target or self.target == ''
        if mode_set:
            self.target = target
        else:  # pragma: no cover
            raise ValueError(f'target already set to {self.target}')
        return asdict(self)


@dataclass
class Rewriter:
    """Container for Meson rewriter commands for OZI projects."""

    target: str
    name: str
    fix: str
    env: Environment
    commands: list[dict[str, str]] = field(default_factory=list)
    path_map: Mapping[str, Callable[[str], Path]] = field(init=False)
    base_templates: dict[
        Annotated[str, 'fix'],
        Annotated[Template, 'base_template'],
    ] = field(init=False)

    def __post_init__(self: Rewriter) -> None:
        """Setup the path_map"""
        self.path_map = {
            'source': partial(Path, self.target, self.name),
            'test': partial(Path, self.target, 'tests'),
            'root': partial(Path, self.target),
        }
        self.base_templates = {
            'root': self.env.get_template(METADATA.spec.python.src.template.add_root),
            'source': self.env.get_template(METADATA.spec.python.src.template.add_source),
            'test': self.env.get_template(METADATA.spec.python.src.template.add_root),
        }

    def _add_dunder_init(self: Self, filename: str) -> None:
        """Render a :file:`{filename}/__init__.py`."""
        build_file(
            self.env,
            self.fix,
            self.path_map.get(self.fix, partial(Path))(
                *filename.rstrip('/').split('/'),
            )
            / '__init__.py',
            find_user_template(
                self.target,
                filename,
                self.fix,
            ),
        )

    def _add_files(
        self: Self,
        child: Path,
        filename: str,
        cmd_files: RewriteCommand,
    ) -> RewriteCommand:
        """add files to a project if they do not exist."""
        if child.exists():  # pragma: no cover
            pass
        else:
            build_file(
                self.env,
                self.fix,
                child,
                user_template=find_user_template(self.target, filename, self.fix),
            )
        if filename.endswith('.pyx'):  # pragma: no cover
            cmd_files.add('ext', 'files', str(Path(filename)))
        else:
            cmd_files.add(self.fix, 'files', str(Path(filename)))
        return cmd_files

    def _add(
        self: Rewriter,
        child: Path,
        filename: str,
        cmd_files_children: tuple[RewriteCommand, RewriteCommand],
    ) -> tuple[RewriteCommand, RewriteCommand]:
        """Add items to OZI Rewriter"""
        cmd_files, cmd_children = cmd_files_children
        if self.fix not in ['source', 'test', 'root']:
            warn('Invalid fix mode nothing will be added.', RuntimeWarning, stacklevel=0)
        elif filename.endswith('/'):
            if child.exists():  # pragma: no cover
                pass
            else:
                build_child(self.env, filename, child)
                if self.fix == 'source':
                    self._add_dunder_init(filename)
            cmd_children.add(self.fix, 'children', filename.rstrip('/'))
        else:
            cmd_files = self._add_files(child, filename, cmd_files)
        return cmd_files, cmd_children

    def __iadd__(self: Self, other: list[str]) -> Self:
        """Add a list of paths"""
        cmd_files = RewriteCommand()
        cmd_children = RewriteCommand()

        for filename in other:
            child = self.path_map.get(self.fix, partial(Path))(filename)
            cmd_files, cmd_children = self._add(child, filename, (cmd_files, cmd_children))
        if cmd_files.active:
            self.commands += [{k: v for k, v in asdict(cmd_files).items() if k != 'active'}]
        if cmd_children.active:
            self.commands += [
                {k: v for k, v in asdict(cmd_children).items() if k != 'active'},
            ]
        return self

    def _sub(
        self: Rewriter,
        child: Path,
        filename: str,
        cmd_files_children: tuple[RewriteCommand, RewriteCommand],
    ) -> tuple[RewriteCommand, RewriteCommand]:
        """Remove items from OZI Rewriter"""
        cmd_files, cmd_children = cmd_files_children
        if filename.endswith('/'):
            cmd_children.rem(self.fix, 'children', str(child / 'meson.build'))
        else:
            cmd_files.rem(self.fix, 'files', str(Path(filename)))
        return cmd_files, cmd_children

    def __isub__(self: Self, other: list[str]) -> Self:
        """Remove a list of paths"""
        cmd_files = RewriteCommand()
        cmd_children = RewriteCommand()
        for filename in other:
            child = self.path_map.get(self.fix, partial(Path))(filename)
            cmd_files, cmd_children = self._sub(child, filename, (cmd_files, cmd_children))
            self.__rm_dir(filename, child)
        if cmd_files.active:
            self.commands += [{k: v for k, v in asdict(cmd_files).items() if k != 'active'}]
        if cmd_children.active:
            self.commands += [
                {k: v for k, v in asdict(cmd_children).items() if k != 'active'},
            ]
        return self

    def __rm_dir(self: Self, filename: str, child: Path) -> None:
        """Try to remove a directory if empty."""
        if filename.endswith('/'):
            try:
                child.rmdir()
            except OSError:
                warn(
                    f'Could not remove non-empty or non-existing {self.fix}: "{child}".',
                    RuntimeWarning,
                )
