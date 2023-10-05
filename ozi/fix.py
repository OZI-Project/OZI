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
from importlib.metadata import version
from pathlib import Path
from typing import Callable, Dict, List, NoReturn, Tuple, Union
from warnings import warn

from jinja2 import Environment, PackageLoader, select_autoescape
from pyparsing import (
    CaselessKeyword,
    Combine,
    Keyword,
    OneOrMore,
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
from .assets.structure import required_pkg_info, root_files, source_files, test_files

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
    else:
        return toks[0]  # type: ignore


dcolon = Suppress(Keyword('::'))
pep639_parse = Suppress(Keyword('..') + CaselessKeyword('ozi')) + OneOrMore(
    Suppress(White(' ', min=2))
    + Suppress(Keyword('Classifier:'))
    + Suppress(White(' ', exact=1))
    + (
        Keyword('License-Expression')
        + dcolon
        + Combine(spdx_license_expression, join_string=' ')
        | Keyword('License-File') + dcolon + oneOf(['LICENSE', 'LICENSE.txt'])
    ).set_parse_action(lambda t: {str(t[0]): str(t[1])})
).set_parse_action(_str_dict_union).set_name('pep639')


def pkg_info_extra(payload: str, as_message: bool = True) -> Union[Dict[str, str], Message]:
    """Get extra PKG-INFO Classifiers tacked onto the payload by OZI."""
    pep639 = pep639_parse.set_parse_action().parse_string(payload)[0]
    if as_message:
        msg = Message()
        for k, v in pep639.items():
            msg.add_header('Classifier', f'{k} :: {v}')
        return msg
    else:
        return pep639  # type: ignore


def report_missing(
    target: Path, stdout: Callable = print
) -> Tuple[str, Message, List[str], List[str], List[str]]:
    """Report missing OZI project files
    :param target: Relative path to target directory.
    :return: Normalized Name, PKG-INFO, found_root, found_sources, found_tests
    """
    target = Path(target)
    miss_count = 0
    count = 0
    name = None
    pkg_info = None
    extra_pkg_info = None
    extra_source_files = None
    try:
        with target.joinpath('PKG-INFO').open() as f:
            pkg_info = message_from_file(f)
            count += 1
            stdout('ok', count, '-', 'Parse PKG-INFO')
        for i in required_pkg_info:
            count += 1
            v = pkg_info.get(i, None)
            if v is not None:
                stdout('ok', count, '-', f'{i}:', v)
            elif v is None:  # pragma: no cover
                warn(f'{count} - {i} MISSING', RuntimeWarning)
        remaining_pkg_info = set(
            (k, v) for k, v in pkg_info.items() if k not in required_pkg_info
        )
        for k,v in iter(python_support_required):
            if (k, v) in remaining_pkg_info:
                count += 1
                stdout('ok', count, '-', f'{k}:', v)
            else:
                warn(f'{count} - "{v}" MISSING', RuntimeWarning)
        for k, v in iter(remaining_pkg_info):
            count += 1
            stdout('ok', count, '-', f'{k}:', v)
        name = re.sub(r'[-_.]+', '-', pkg_info.get('Name', str())).lower()
        try:
            extra_pkg_info = pkg_info_extra(pkg_info.get_payload()).items()
        except ParseException:  # pragma: defer to good-first-issue
            count += 1
            extra_pkg_info = {}
            warn(f'{count} - PKG-INFO OZI-Extra MISSING', RuntimeWarning)
        for k, v in extra_pkg_info:
            count += 1
            stdout('ok', count, '-', f'{k}:', v)
        found_source_files = []
        for file in source_files:
            count += 1
            if not target.joinpath(underscorify(name), file).exists(): # pragma: defer to good-first-issue
                warn(f'{count} - {Path(underscorify(name)) / file} MISSING', RuntimeWarning)
                miss_count += 1
                continue
            else:
                stdout('ok', count, '-', Path(underscorify(name), file))
            found_source_files.append(file)
        extra_source_files = [
            file
            for file in os.listdir(target / underscorify(name))
            if os.path.isfile(os.path.join(target, underscorify(name), file))
        ]
        extra_source_files = list(
            set(extra_source_files).symmetric_difference(set(found_source_files))
        )
        for file in extra_source_files:
            count += 1
            stdout('ok', count, '#', 'SKIP', Path(underscorify(name)) / file)
    except FileNotFoundError:
        warn(f'{count} - PKG-INFO MISSING', RuntimeWarning)
    found_root_files = []
    for file in root_files:
        count += 1
        if not target.joinpath(file).exists():
            warn(f'{count} - {Path(file)} MISSING', RuntimeWarning)
            miss_count += 1
            continue
        else:
            stdout('ok', count, '-', Path(file))
        found_root_files.append(file)
    extra_root_files = [
        file for file in os.listdir(target) if os.path.isfile(os.path.join(target, file))
    ]
    extra_root_files = list(
        set(extra_root_files).symmetric_difference(set(found_root_files))
    )
    for file in extra_root_files:
        count += 1
        stdout('ok', count, '#', 'SKIP', file)

    found_test_files = []
    for file in test_files:
        count += 1
        if not target.joinpath('tests', file).exists():
            warn(f"{count} - {Path('tests', file)} MISSING", RuntimeWarning)
            miss_count += 1
            continue
        else:
            stdout('ok', count, '-', Path('tests', file))
        found_test_files.append(file)
    extra_test_files = [
        file
        for file in os.listdir(target / 'tests')
        if os.path.isfile(os.path.join(target, 'tests', file))
    ]
    extra_test_files = list(
        set(extra_test_files).symmetric_difference(set(found_test_files))
    )
    for file in extra_test_files:
        count += 1
        stdout('ok', count, '#', 'SKIP', Path('tests', file))
    all_files = (
        ['PKG-INFO'],
        pkg_info,
        extra_pkg_info,
        root_files,
        source_files,
        test_files,
        extra_root_files,
        extra_source_files,
        extra_test_files,
    )
    try:
        expected = f'{sum(map(len, all_files))+miss_count}'  # type: ignore
    except TypeError:  # pragma: no cover
        warn('Bail out! MISSING required files or metadata.')
        return
    stdout(f'1..{expected}')
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

    def _add(
        self: Rewriter,
        child: Path,
        file: str,
        cmd_files: RewriteCommand,
        cmd_children: RewriteCommand,
    ) -> Tuple[RewriteCommand, RewriteCommand]:
        """Add items to OZI Rewriter"""
        templates = {
            'root': env.get_template('project.name/new_module.py.j2'),
            'source': env.get_template('project.name/new_module.py.j2'),
            'test': env.get_template('tests/new_test.py.j2'),
        }
        if self.fix not in ['source', 'test', 'root']:
            warn('Invalid fix mode nothing will be added.', RuntimeWarning)
        else:
            if file.endswith('/'):
                child.mkdir()
                (child / 'meson.build').touch()
                with open((child / 'meson.build'), 'w') as f:
                    f.write(env.get_template('new_child.j2').render())
                cmd_children.add(self.fix, 'children', 'meson.build')
            elif file.endswith('.py'):
                child.write_text(
                    templates.get(
                        self.fix,
                        templates.setdefault(
                            self.fix, env.get_template('project.name/new_module.py.j2')
                        ),
                    ).render()
                )
            else:
                child.touch()
            cmd_files.add(self.fix, 'files', str(Path(file)))
        return cmd_files, cmd_children

    def __iadd__(self: Rewriter, other: List[str]) -> Rewriter:
        """Add a list of paths"""
        cmd_files = RewriteCommand()
        cmd_children = RewriteCommand()

        for file in other:
            if self.fix == 'source':
                child = Path(self.target, self.name, file)
            elif self.fix == 'test':
                child = Path(self.target, 'tests', file)
            elif self.fix == 'root':
                child = Path(self.target, file)
            else:
                child = Path()
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
            child = Path(self.target, file)
            if self.fix == 'source':
                child = Path(self.target, self.name, file)
            elif self.fix == 'root':
                child = Path(self.target, file)
            elif self.fix == 'test':
                child = Path(self.target, 'tests', file)
            else:
                child = Path()
            cmd_files, cmd_children = self._sub(child, file, cmd_files, cmd_children)
            if file.endswith('/'):
                try:
                    child.rmdir()
                except OSError:
                    warn(
                        f'Could not remove non-empty or non-existing {self.fix} child.',
                        RuntimeWarning,
                    )
        if cmd_files.active:
            self.commands += [{k: v for k, v in asdict(cmd_files).items() if k != 'active'}]
        if cmd_children.active:
            self.commands += [
                {k: v for k, v in asdict(cmd_children).items() if k != 'active'}
            ]
        return self


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
        project.target, stdout=print if project.missing else lambda *_: None
    )
    project.name = underscorify(name)
    project.copyright_head = '\n'.join(
        [
            f'Part of {name}.',
            'See LICENSE.txt in the project root for details.',
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
