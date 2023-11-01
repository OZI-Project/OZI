# ozi/fix.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""ozi-fix: Project fix script that outputs a meson rewriter JSON array."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import warnings
from dataclasses import asdict, dataclass, field
from email import message_from_file
from email.message import Message
from functools import partial
from importlib.metadata import version
from pathlib import Path
from typing import Annotated, Any, Callable, Dict, List, Mapping, NoReturn, Set, Tuple, Union
from warnings import warn

from jinja2 import Environment, PackageLoader, Template, select_autoescape
from pyparsing import (
    CaselessKeyword,
    Combine,
    Forward,
    Keyword,
    Literal,
    ParseException,
    ParseResults,
    Suppress,
    White,
    oneOf,
)

from .assets import (
    python_support_required,
    spdx_license_expression,
    tap_warning_format,
    underscorify,
)
from .assets.structure import (  # noqa: F401
    required_pkg_info,
    root_files,
    source_files,
    test_files,
)

warnings.formatwarning = tap_warning_format  # type: ignore

env = Environment(
    loader=PackageLoader('ozi'),
    autoescape=select_autoescape(),
    enable_async=True,
)
env.filters['underscorify'] = underscorify
env.globals = env.globals | {
    'ozi': {
        'version': version('OZI'),
        'spec': '0.1',
    },
}
parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__, add_help=False)
subparser = parser.add_subparsers(help='source & test fix', dest='fix')
parser.add_argument('target', type=str, help='target OZI project directory')
source_parser = subparser.add_parser(
    'source', aliases=['s'], description='Create a new Python source in an OZI project.'
)
test_parser = subparser.add_parser(
    'test',
    aliases=['t'],
    description='Create a new Python test in an OZI project.',
)
source_parser.add_argument(
    '-a',
    '--add',
    nargs='?',
    action='append',
    default=['ozi.phony'],
    help='add file or dir/ to project',
)
source_parser.add_argument(
    '-r',
    '--remove',
    nargs='?',
    action='append',
    default=['ozi.phony'],
    help='remove file or dir/ from project',
)
source_parser.add_argument(
    '--copyright-head',
    type=str,
    default='',
    help='copyright header string',
    metavar='"Part of the NAME project.\\nSee LICENSE..."',
)
source_output = source_parser.add_argument_group('output')
source_output.add_argument(
    '--strict',
    default='--no-strict',
    action=argparse.BooleanOptionalAction,
    help='strict mode raises warnings to errors.',
)
source_output.add_argument(
    '-p', '--pretty', action='store_true', help='pretty print JSON output'
)
test_parser.add_argument(
    '-a',
    '--add',
    nargs='?',
    action='append',
    default=['ozi.phony'],
    help='add file or dir/ to project',
)
test_parser.add_argument(
    '-r',
    '--remove',
    nargs='?',
    action='append',
    default=['ozi.phony'],
    help='remove file or dir/ from project',
)
test_parser.add_argument(
    '--copyright-head',
    type=str,
    default='',
    help='copyright header string',
    metavar='"Part of the NAME project.\\nSee LICENSE..."',
)
test_output = test_parser.add_argument_group('output')
test_output.add_argument(
    '--strict',
    default='--no-strict',
    action=argparse.BooleanOptionalAction,
    help='strict mode raises warnings to errors.',
)
test_output.add_argument(
    '-p', '--pretty', action='store_true', help='pretty print JSON output'
)

helpers = parser.add_mutually_exclusive_group()
helpers.add_argument('-h', '--help', action='help', help='show this help message and exit')
missing_parser = subparser.add_parser(
    'missing',
    aliases=['m'],
    description='Create a new Python test in an OZI project.',
)
missing_parser.add_argument(
    '--add',
    nargs='?',
    action='append',
    default=['ozi.phony'],
    help=argparse.SUPPRESS,
)
missing_parser.add_argument(
    '--remove',
    nargs='?',
    action='append',
    default=['ozi.phony'],
    help=argparse.SUPPRESS,
)
missing_parser.add_argument(
    '--strict',
    default='--no-strict',
    action=argparse.BooleanOptionalAction,
    help='strict mode raises warnings to errors.',
)
missing_parser.add_argument(
    '--pretty',
    default='--no-pretty',
    action=argparse.BooleanOptionalAction,
    help='strict mode raises warnings to errors.',
)


def _str_dict_union(toks: ParseResults) -> Dict[str, str]:
    """Parse-time union of Dict[str, str]."""
    if len(toks) >= 2:
        return toks[0] | toks[1]  # type: ignore
    else:  # pragma: no cover
        return  # type: ignore


sspace = Suppress(White(' ', exact=1))
dcolon = sspace + Suppress(Literal('::')) + sspace
classifier = Suppress(White(' ', min=2)) + Suppress(Literal('Classifier:')) + sspace
pep639_headers = Forward()
license_expression = classifier + (
    Keyword('License-Expression')
    + dcolon
    + Combine(spdx_license_expression, join_string=' ')
).set_parse_action(lambda t: {str(t[0]): str(t[1])})
license_file = classifier + (
    Keyword('License-File') + dcolon + oneOf(['LICENSE', 'LICENSE.txt'])
).set_parse_action(lambda t: {str(t[0]): str(t[1])})
pep639_headers <<= license_expression + license_file

pep639_parse = Suppress(
    Keyword('..') + CaselessKeyword('ozi')
) + pep639_headers.set_parse_action(_str_dict_union).set_name('pep639')


def pkg_info_extra(payload: str, as_message: bool = True) -> Union[Dict[str, str], Message]:
    """Get extra PKG-INFO Classifiers tacked onto the payload by OZI."""
    pep639: Dict[str, str] = pep639_parse.parse_string(payload)[0]  # pyright: ignore
    if as_message:
        msg = Message()
        for k, v in pep639.items():
            msg.add_header('Classifier', f'{k} :: {v}')
        return msg
    else:
        return pep639


def missing_python_support(
    pkg_info: Message, count: int, stdout: Callable[..., None]
) -> Tuple[int, Set[Tuple[str, str]]]:
    """Check PKG-INFO Message for python support."""
    remaining_pkg_info = {(k, v) for k, v in pkg_info.items() if k not in required_pkg_info}
    for k, v in iter(python_support_required):
        if (k, v) in remaining_pkg_info:
            count += 1
            stdout('ok', count, '-', f'{k}:', v)
        else:
            warn(f'{count} - "{v}" MISSING', RuntimeWarning)
    return count, remaining_pkg_info


def missing_ozi_required(
    pkg_info: Message, count: int, stdout: Callable[..., None]
) -> Tuple[int, Any]:
    """Check missing required OZI extra PKG-INFO"""
    count, remaining_pkg_info = missing_python_support(pkg_info, count, stdout)
    remaining_pkg_info.difference_update(set(iter(python_support_required)))
    for k, v in iter(remaining_pkg_info):
        count += 1
        stdout('ok', count, '-', f'{k}:', v)
    try:
        extra_pkg_info = pkg_info_extra(pkg_info.get_payload()).items()
    except ParseException as e:
        extra_pkg_info = {}  # type: ignore
        newline = '\n'
        errstr = str(e).replace(newline, ' ')
        warn(f'{count} - MISSING {errstr}', RuntimeWarning)
    return count, extra_pkg_info


def missing_required(
    target: Path, count: int, stdout: Callable[..., None]
) -> Tuple[int, str, Any]:
    """Find missing required PKG-INFO"""
    with target.joinpath('PKG-INFO').open() as f:
        pkg_info = message_from_file(f)
        count += 1
        stdout('ok', count, '-', 'Parse PKG-INFO')
    for i in required_pkg_info:
        count += 1
        v = pkg_info.get(i, None)
        if v is not None:
            stdout('ok', count, '-', f'{i}:', v)
        else:
            warn(f'{count} - {i} MISSING', RuntimeWarning)
    count, extra_pkg_info = missing_ozi_required(pkg_info, count, stdout)
    name = re.sub(r'[-_.]+', '-', pkg_info.get('Name', str())).lower()
    for k, v in extra_pkg_info:
        count += 1
        stdout('ok', count, '-', f'{k}:', v)
    return count, name, extra_pkg_info


def missing_required_files(
    kind: str,
    target: Path,
    count: int,
    miss_count: int,
    name: str,
    stdout: Callable[..., None],
) -> Tuple[int, int, List[str], List[str]]:
    """Count missing files required by OZI"""
    found_files = []
    miss_count = 0
    mapping = {
        'test': Path('tests'),
        'source': Path(underscorify(name)),
        'root': Path('.'),
    }
    for file in vars(sys.modules[__name__]).get('_'.join([kind, 'files']), []):
        count += 1
        rel_path = mapping.get(kind, Path('.')) / file
        if not target.joinpath(rel_path).exists():
            warn(f'{count} - {rel_path} MISSING', RuntimeWarning)
            miss_count += 1
            continue  # pragma: defer to https://github.com/nedbat/coveragepy/issues/198
        else:
            stdout('ok', count, '-', rel_path)
        found_files.append(file)
    rel_path = mapping.get(kind, Path('.'))
    extra_files = [
        file
        for file in os.listdir(target / rel_path)
        if os.path.isfile(target / rel_path / file)
    ]
    extra_files = list(set(extra_files).symmetric_difference(set(found_files)))
    for file in extra_files:  # pragma: no cover
        count += 1
        stdout('ok', count, '#', 'SKIP', rel_path / file)

    return count, miss_count, found_files, extra_files


def report_missing(
    target: Path, stdout: Callable[..., None] = print
) -> Union[
    Tuple[str, Message, List[str], List[str], List[str]], Tuple[None, None, None, None, None]
]:
    """Report missing OZI project files
    :param target: Relative path to target directory.
    :return: Normalized Name, PKG-INFO, found_root, found_sources, found_tests
    """
    target = Path(target)
    miss_count = 0
    count = 0
    name = None
    pkg_info = None
    extra_pkg_info: Dict[str, str] = {}
    try:
        count, name, extra_pkg_info = missing_required(target, count, stdout)
    except FileNotFoundError:
        name = ''
        warn(f'{count} - PKG-INFO MISSING', RuntimeWarning)
    count, miss_count, found_source_files, extra_source_files = missing_required_files(
        'source', target, count, 0, name, stdout
    )
    count, miss_count, found_test_files, extra_test_files = missing_required_files(
        'test', target, count, miss_count, name, stdout
    )
    count, miss_count, found_root_files, extra_root_files = missing_required_files(
        'root', target, count, miss_count, name, stdout
    )
    all_files = (
        ['PKG-INFO'],
        extra_pkg_info,
        found_root_files,
        found_source_files,
        found_test_files,
        extra_root_files,
        extra_source_files,
        extra_test_files,
    )
    try:
        sum(map(len, all_files))
    except TypeError:  # pragma: no cover
        warn('Bail out! MISSING required files or metadata.')
        return (None, None, None, None, None)
    stdout(f'1..{count+miss_count}')
    return name, pkg_info, found_root_files, found_source_files, found_test_files  # type: ignore


@dataclass
class RewriteCommand:  # pragma: defer to meson
    """Meson rewriter command input"""

    active: bool = field(repr=False, default_factory=bool, init=False)
    type: str = 'target'
    target: str = ''
    operation: str = ''
    sources: List[str] = field(default_factory=list)
    subdir: str = ''
    target_type: str = ''

    def add(
        self: RewriteCommand, mode: str, kind: str, source: str
    ) -> Dict[str, Union[str, List[str]]]:
        """Add sources and tests to an OZI project."""
        self.sources += [source]
        self.operation = 'src_add'
        return self._body(mode, kind)

    def rem(
        self: RewriteCommand, mode: str, kind: str, source: str
    ) -> Dict[str, Union[str, List[str]]]:
        """Add sources and tests to an OZI project."""
        self.sources += [source]
        self.operation = 'src_rem'
        return self._body(mode, kind)

    def _body(
        self: RewriteCommand, mode: str, kind: str
    ) -> Dict[str, Union[str, List[str]]]:
        """The body of the add/rem functions"""
        self.active = True
        target = mode + '_' + kind
        mode_set = self.target == target or self.target == ''
        if mode_set:
            self.target = target
        else:
            raise ValueError(f'target already set to {self.target}')
        return asdict(self)


@dataclass
class Rewriter:
    """Container for Meson rewriter commands."""

    target: str
    name: str
    fix: str
    commands: List[Dict[str, str]] = field(default_factory=list)
    path_map: Mapping[str, Callable[[str], Path]] = field(init=False)
    base_templates: Dict[
        Annotated[str, 'fix'], Annotated[Template, 'base_template']
    ] = field(init=False)

    def __post_init__(self: Rewriter) -> None:
        """Setup the path_map"""
        self.path_map = {
            'source': partial(Path, self.target, self.name),
            'test': partial(Path, self.target, 'tests'),
            'root': partial(Path, self.target),
        }
        self.base_templates = {
            'root': env.get_template('tests/new_test.py.j2'),
            'source': env.get_template('project.name/new_module.py.j2'),
            'test': env.get_template('tests/new_test.py.j2'),
        }

    def find_user_templates(self: Rewriter, file: str) -> str | None:
        try:
            with open(Path(self.target, 'templates', self.fix, file)) as template:
                user_template = template.read()
        except OSError:
            user_template = None
        return user_template

    def _add(  # noqa: C901
        self: Rewriter,
        child: Path,
        file: str,
        cmd_files: RewriteCommand,
        cmd_children: RewriteCommand,
    ) -> Tuple[RewriteCommand, RewriteCommand]:
        """Add items to OZI Rewriter"""
        if self.fix not in ['source', 'test', 'root']:
            warn('Invalid fix mode nothing will be added.', RuntimeWarning)
        else:
            if file.endswith('/'):
                child.mkdir(parents=True)
                parent = file.rstrip('/')
                heirs = parent.split('/')
                if len(heirs) > 1:
                    warn('Nested folder creation not supported.', RuntimeWarning)
                else:
                    with open((child / 'meson.build'), 'x') as f:
                        f.write(env.get_template('new_child.j2').render(parent=parent))
                if self.fix == 'source':
                    if len(heirs) > 1:
                        warn('Nested folder creation not supported.', RuntimeWarning)
                    else:
                        with open(
                            (
                                self.path_map.get(self.fix, partial(Path))(*heirs)
                                / '__init__.py'
                            ),
                            'x',
                        ) as f:
                            f.write(
                                env.get_template('project.name/__init__.py.j2').render(
                                    user_template=self.find_user_templates(file)
                                )
                            )
                        cmd_children.add(self.fix, 'children', parent)
                else:
                    cmd_children.add(self.fix, 'children', parent)
            elif file.endswith('.py'):
                child.write_text(
                    self.base_templates.get(
                        self.fix,
                        self.base_templates.setdefault(
                            self.fix, env.get_template('project.name/new_module.py.j2')
                        ),
                    ).render(user_template=self.find_user_templates(file))
                )
                cmd_files.add(self.fix, 'files', str(Path(file)))
            else:
                child.touch()
                cmd_files.add(self.fix, 'files', str(Path(file)))
        return cmd_files, cmd_children

    def __iadd__(self: Rewriter, other: List[str]) -> Rewriter:
        """Add a list of paths"""
        cmd_files = RewriteCommand()
        cmd_children = RewriteCommand()

        for file in other:
            child = self.path_map.get(self.fix, partial(Path))(file)
            cmd_files, cmd_children = self._add(child, file, cmd_files, cmd_children)
        if cmd_files.active:
            self.commands += [{k: v for k, v in asdict(cmd_files).items() if k != 'active'}]
        if cmd_children.active:
            self.commands += [
                {k: v for k, v in asdict(cmd_children).items() if k != 'active'}
            ]
        return self

    def _sub(
        self: Rewriter,
        child: Path,
        file: str,
        cmd_files: RewriteCommand,
        cmd_children: RewriteCommand,
    ) -> Tuple[RewriteCommand, RewriteCommand]:
        """Remove items from OZI Rewriter"""
        if file.endswith('/'):
            cmd_children.rem(self.fix, 'children', str(child / 'meson.build'))
        elif file.endswith('.py'):
            cmd_files.rem(self.fix, 'files', str(Path(file)))
        else:
            cmd_files.rem(self.fix, 'files', str(Path(file)))
        return cmd_files, cmd_children

    def __isub__(self: Rewriter, other: List[str]) -> Rewriter:
        """Remove a list of paths"""
        cmd_files = RewriteCommand()
        cmd_children = RewriteCommand()
        for file in other:
            child = self.path_map.get(self.fix, partial(Path))(file)
            cmd_files, cmd_children = self._sub(child, file, cmd_files, cmd_children)
            self.__rm_dir(file, child)
        if cmd_files.active:
            self.commands += [{k: v for k, v in asdict(cmd_files).items() if k != 'active'}]
        if cmd_children.active:
            self.commands += [
                {k: v for k, v in asdict(cmd_children).items() if k != 'active'}
            ]
        return self

    def __rm_dir(self: Rewriter, file: str, child: Path) -> None:
        """Try to remove a directory if empty."""
        if file.endswith('/'):
            try:
                child.rmdir()
            except OSError:
                warn(
                    f'Could not remove non-empty or non-existing {self.fix}: "{child}".',
                    RuntimeWarning,
                )


def preprocess(project: argparse.Namespace) -> argparse.Namespace:
    """Remove phony arguments, check target exists and is a directory, set missing flag."""
    project.missing = project.fix == 'missing'
    project.target = Path(project.target).absolute()
    if not project.target.exists():
        warn(f'Bail out! target: {project.target}\ntarget does not exist.', RuntimeWarning)
    elif not project.target.is_dir():
        warn(
            f'Bail out! target: {project.target}\ntarget is not a directory.', RuntimeWarning
        )
    project.add.remove('ozi.phony')
    project.add = list(set(project.add))
    project.remove.remove('ozi.phony')
    project.remove = list(set(project.remove))
    return project


def main() -> NoReturn:  # pragma: no cover
    """Main ozi.fix entrypoint."""
    project = preprocess(parser.parse_args())
    env.globals = env.globals | {
        'project': vars(project),
    }
    name, *_ = report_missing(
        project.target, stdout=print if project.missing else lambda *_: None  # type: ignore
    )

    if name is None:
        exit(1)

    project.name = underscorify(name)
    project.license_file = 'LICENSE.txt'
    project.copyright_head = '\n'.join(
        [
            f'Part of {name}.',
            f'See {project.license_file} in the project root for details.',
        ]
    )
    rewriter = Rewriter(project.target, project.name, project.fix)
    rewriter += project.add
    rewriter -= project.remove
    if not project.missing:
        print(json.dumps(rewriter.commands, indent=4 if project.pretty else None))
    exit(0)


if __name__ == '__main__':
    main()
