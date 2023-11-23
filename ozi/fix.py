# ozi/fix.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""ozi-fix: Project fix script that outputs a meson rewriter JSON array."""
from __future__ import annotations

import gc
import json
import os
import re
import sys
import warnings
from argparse import SUPPRESS
from argparse import ArgumentParser
from argparse import BooleanOptionalAction
from contextlib import contextmanager
from contextlib import suppress
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from email import message_from_file
from functools import partial
from pathlib import Path
from runpy import run_module
from typing import TYPE_CHECKING
from typing import Annotated
from typing import Any
from typing import NoReturn

if sys.version_info >= (3, 11):  # pragma: no cover
    from typing import Self
else:  # pragma: no cover
    from typing_extensions import Self

from typing import Union
from warnings import warn

if TYPE_CHECKING:  # pragma: no cover
    from argparse import Namespace
    from collections.abc import Callable
    from collections.abc import Generator
    from collections.abc import Mapping
    from email.message import Message

    from jinja2 import Template

from ozi.assets import parse_extra_pkg_info
from ozi.filter import underscorify
from ozi.render import env
from ozi.spec import Metadata
from ozi.spec import PythonSupport


def tap_warning_format(  # pragma: no cover
    message: Warning | str,
    category: type[Warning],
    filename: str,
    lineno: int,
    line: str | None = None,
) -> str:
    """Test Anything Protocol formatted warnings."""
    return f'# {filename}:{lineno}: {category.__name__}\nnot ok - {message}\n'  # pragma: no cover


pywarningformat = warnings.formatwarning
warnings.formatwarning = tap_warning_format

metadata = Metadata()
python_support = PythonSupport()
parser = ArgumentParser(description=sys.modules[__name__].__doc__, add_help=False)
subparser = parser.add_subparsers(help='source & test fix', dest='fix')
parser.add_argument('target', type=str, help='target OZI project directory')
source_parser = subparser.add_parser(
    'source',
    aliases=['s'],
    description='Create a new Python source in an OZI project.',
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
    metavar='Part of the NAME project.\\nSee LICENSE...',
)
source_output = source_parser.add_argument_group('output')
source_output.add_argument(
    '--strict',
    default='--no-strict',
    action=BooleanOptionalAction,
    help='strict mode raises warnings to errors.',
)
source_output.add_argument(
    '-p',
    '--pretty',
    action='store_true',
    help='pretty print JSON output',
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
    metavar='Part of the NAME project.\\nSee LICENSE...',
)
test_output = test_parser.add_argument_group('output')
test_output.add_argument(
    '--strict',
    default='--no-strict',
    action=BooleanOptionalAction,
    help='strict mode raises warnings to errors.',
)
test_output.add_argument(
    '-p',
    '--pretty',
    action='store_true',
    help='pretty print JSON output',
)

helpers = parser.add_mutually_exclusive_group()
helpers.add_argument('-h', '--help', action='help', help='show this help message and exit')
missing_parser = subparser.add_parser(
    'missing',
    aliases=['m'],
    description='Create a new Python test in an OZI project.',
    add_help=False,
)
missing_parser.add_argument(
    '--add',
    nargs='?',
    action='append',
    default=['ozi.phony'],
    help=SUPPRESS,
)
missing_parser.add_argument(
    '--remove',
    nargs='?',
    action='append',
    default=['ozi.phony'],
    help=SUPPRESS,
)
missing_parser.add_argument(
    '--strict',
    default='--no-strict',
    action=BooleanOptionalAction,
    help='strict mode raises warnings to errors, default: --no-strict',
)
missing_parser.add_argument(
    '--run-utility',
    default='--run-utility',
    action=BooleanOptionalAction,
    help='run-utility mode runs isort, autoflake, and black with OZI standard arguments,'
    ' default: --run-utlity',
)
missing_parser.add_argument(
    '--pretty',
    default='--no-pretty',
    action=BooleanOptionalAction,
    help='pretty mode outputs indented json, default: --no-pretty',
)


def missing_python_support(
    pkg_info: Message,
    count: int,
    stdout: Callable[..., None],
) -> tuple[int, set[tuple[str, str]]]:
    """Check PKG-INFO Message for python support."""
    remaining_pkg_info = {
        (k, v)
        for k, v in pkg_info.items()
        if k not in metadata.spec.python.pkg.info.required
    }
    for k, v in iter(python_support.classifiers[:4]):
        if (k, v) in remaining_pkg_info:
            count += 1
            stdout('ok', count, '-', f'{k}:', v)
        else:
            warn(f'{count} - "{v}" MISSING', RuntimeWarning, stacklevel=0)
    return count, remaining_pkg_info


def missing_ozi_required(
    pkg_info: Message,
    count: int,
    stdout: Callable[..., None],
) -> tuple[int, Any]:
    """Check missing required OZI extra PKG-INFO"""
    count, remaining_pkg_info = missing_python_support(pkg_info, count, stdout)
    remaining_pkg_info.difference_update(set(iter(python_support.classifiers)))
    for k, v in iter(remaining_pkg_info):
        count += 1
        stdout('ok', count, '-', f'{k}:', v)
    extra_pkg_info, errstr = parse_extra_pkg_info(pkg_info)
    if errstr not in ('', None):  # pragma: defer to good-first-issue
        warn(f'{count} - MISSING {errstr}', RuntimeWarning, stacklevel=0)
    return count, extra_pkg_info


def missing_required(
    target: Path,
    count: int,
    stdout: Callable[..., None],
) -> tuple[int, str, Any]:
    """Find missing required PKG-INFO"""
    with target.joinpath('PKG-INFO').open() as f:
        pkg_info = message_from_file(f)
        count += 1
        stdout('ok', count, '-', 'Parse PKG-INFO')
    for i in metadata.spec.python.pkg.info.required:
        count += 1
        v = pkg_info.get(i, None)
        if v is not None:
            stdout('ok', count, '-', f'{i}:', v)
        else:
            warn(f'{count} - {i} MISSING', RuntimeWarning, stacklevel=0)
    count, extra_pkg_info = missing_ozi_required(pkg_info, count, stdout)
    name = re.sub(r'[-_.]+', '-', pkg_info.get('Name', '')).lower()
    for k, v in extra_pkg_info.items():
        count += 1
        stdout('ok', count, '-', f'{k}:', v)
    return count, name, extra_pkg_info


def count_comments(
    count: int,
    lines: list[str],
    rel_path: Path,
) -> int:  # pragma: defer to good-first-issue
    for i, line in enumerate(lines, start=1):
        if s := re.search(r'(.*?noqa:\s[A-Z0-9]*.*?)', line):
            count += 1
            print('#', 'NOQA', f'{rel_path!s}:{i}', s[0].strip())
        if s := re.search(r'(.*?type:\signore.*?)', line):
            count += 1
            print('#', 'TYPE', f'{rel_path!s}:{i}', s[0].strip())
        if s := re.search(r'(.*?pragma:\sdefer\sto\s[a-z_-]*.*?)', line):
            count += 1
            print(
                '#',
                'PRAGMA',
                f'{rel_path!s}:{i}',
                s[0].strip(),
            )
        if s := re.search(r'(.*?pragma:\sno\scover\s.*?)', line):
            count += 1
            print(
                '#',
                'PRAGMA',
                f'{rel_path!s}:{i}',
                s[0].strip(),
            )
    return count


def missing_required_files(  # noqa: C901
    kind: str,
    target: Path,
    count: int,
    miss_count: int,
    name: str,
    stdout: Callable[..., None],
) -> tuple[int, int, list[str], list[str]]:
    """Count missing files required by OZI"""
    found_files = []
    miss_count = 0
    match kind:
        case 'test':
            rel_path = Path('tests')
            expected_files = metadata.spec.python.src.required.test
        case 'root':
            rel_path = Path()
            expected_files = metadata.spec.python.src.required.root
        case 'source':
            rel_path = Path(underscorify(name))
            expected_files = metadata.spec.python.src.required.source
        case _:  # pragma: no cover
            rel_path = Path()
            expected_files = ()

    for file in expected_files:
        f = rel_path / file
        match f:
            case f if f and not target.joinpath(f).exists():
                count += 1
                warn(f'{count} - {f} MISSING', RuntimeWarning, stacklevel=0)
                miss_count += 1
                continue  # pragma: defer to https://github.com/nedbat/coveragepy/issues/198
            case f if f and str(f).endswith('.py'):
                with open(target.joinpath(f)) as fh:
                    count_comments(count, fh.readlines(), f)
        count += 1
        stdout('ok', count, '-', f)
        found_files.append(file)
    extra_files = [
        file
        for file in os.listdir(target / rel_path)
        if os.path.isfile(target / rel_path / file)
    ]
    extra_files = list(set(extra_files).symmetric_difference(set(found_files)))
    build_files = []
    for file in extra_files:  # pragma: no cover
        pattern = re.compile(f'(.*?[\'|"]{re.escape(file)}[\'|"].*?)')
        with open(str((target / rel_path / file).parent / 'meson.build')) as fh:
            for _ in [i for i in fh.readlines() if re.search(pattern, i)]:
                count += 1
                build_file = str((rel_path / file).parent / 'meson.build')
                stdout(
                    'ok',
                    count,
                    '-',
                    f'{build_file}:',
                    str(rel_path / file),
                )
        build_files += [str(rel_path / file)]
        match file:
            case file if str(file).endswith('.py') and str(
                rel_path / file,
            ) not in build_files:
                build_file = str(rel_path / 'meson.build')
                warn(
                    f'{count} - MISSING {build_file}: {rel_path / file!s}',
                    RuntimeWarning,
                )
                print(f'# SKIP {rel_path / file!s}')
            case file if str(file).endswith('.py'):
                with open(target.joinpath(rel_path) / file) as g:
                    count_comments(count, g.readlines(), rel_path / file)
    return count, miss_count, found_files, extra_files


def report_missing(
    target: Path,
    stdout: Callable[..., None] = print,
) -> Union[
    tuple[str, Message, list[str], list[str], list[str]],
    tuple[None, None, None, None, None],
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
    extra_pkg_info: dict[str, str] = {}
    try:
        count, name, extra_pkg_info = missing_required(target, count, stdout)
    except FileNotFoundError:
        name = ''
        warn(f'{count} - PKG-INFO MISSING', RuntimeWarning, stacklevel=0)
    count, miss_count, found_source_files, extra_source_files = missing_required_files(
        'source',
        target,
        count,
        0,
        name,
        stdout,
    )
    count, miss_count, found_test_files, extra_test_files = missing_required_files(
        'test',
        target,
        count,
        miss_count,
        name,
        stdout,
    )
    count, miss_count, found_root_files, extra_root_files = missing_required_files(
        'root',
        target,
        count,
        miss_count,
        name,
        stdout,
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
    sources: list[str] = field(default_factory=list)
    subdir: str = ''
    target_type: str = ''

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
        else:
            raise ValueError(f'target already set to {self.target}')
        return asdict(self)


@dataclass
class Rewriter:
    """Container for Meson rewriter commands."""

    target: str
    name: str
    fix: str
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
    ) -> tuple[RewriteCommand, RewriteCommand]:
        """Add items to OZI Rewriter"""
        if self.fix not in ['source', 'test', 'root']:
            warn('Invalid fix mode nothing will be added.', RuntimeWarning, stacklevel=0)
        elif file.endswith('/'):
            child.mkdir(parents=True)
            parent = file.rstrip('/')
            heirs = parent.split('/')
            if len(heirs) > 1:
                warn(
                    'Nested folder creation not supported.',
                    RuntimeWarning,
                    stacklevel=0,
                )
            else:
                with open((child / 'meson.build'), 'x') as f:
                    f.write(env.get_template('new_child.j2').render(parent=parent))
            if self.fix == 'source':
                if len(heirs) > 1:
                    warn(
                        'Nested folder creation not supported.',
                        RuntimeWarning,
                        stacklevel=0,
                    )
                else:
                    with open(
                        (self.path_map.get(self.fix, partial(Path))(*heirs) / '__init__.py'),
                        'x',
                    ) as f:
                        f.write(
                            env.get_template('project.name/__init__.py.j2').render(
                                user_template=self.find_user_templates(file),
                            ),
                        )
                    cmd_children.add(self.fix, 'children', parent)
            else:
                cmd_children.add(self.fix, 'children', parent)
        elif file.endswith('.py'):
            child.write_text(
                self.base_templates.get(
                    self.fix,
                    self.base_templates.setdefault(
                        self.fix,
                        env.get_template('project.name/new_module.py.j2'),
                    ),
                ).render(user_template=self.find_user_templates(file)),
            )
            cmd_files.add(self.fix, 'files', str(Path(file)))
        else:
            child.touch()
            cmd_files.add(self.fix, 'files', str(Path(file)))
        return cmd_files, cmd_children

    def __iadd__(self: Self, other: list[str]) -> Self:
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
                {k: v for k, v in asdict(cmd_children).items() if k != 'active'},
            ]
        return self

    def _sub(
        self: Rewriter,
        child: Path,
        file: str,
        cmd_files: RewriteCommand,
        cmd_children: RewriteCommand,
    ) -> tuple[RewriteCommand, RewriteCommand]:
        """Remove items from OZI Rewriter"""
        if file.endswith('/'):
            cmd_children.rem(self.fix, 'children', str(child / 'meson.build'))
        elif file.endswith('.py'):
            cmd_files.rem(self.fix, 'files', str(Path(file)))
        else:
            cmd_files.rem(self.fix, 'files', str(Path(file)))
        return cmd_files, cmd_children

    def __isub__(self: Self, other: list[str]) -> Self:
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
                {k: v for k, v in asdict(cmd_children).items() if k != 'active'},
            ]
        return self

    def __rm_dir(self: Self, file: str, child: Path) -> None:
        """Try to remove a directory if empty."""
        if file.endswith('/'):
            try:
                child.rmdir()
            except OSError:
                warn(
                    f'Could not remove non-empty or non-existing {self.fix}: "{child}".',
                    RuntimeWarning,
                )


def preprocess(project: Namespace) -> Namespace:
    """Remove phony arguments, check target exists and is a directory, set missing flag."""
    project.missing = project.fix == 'missing'
    project.target = Path(os.path.relpath(os.path.join('/', project.target), '/')).absolute()
    if not project.target.exists():
        warn(
            f'Bail out! target: {project.target}\ntarget does not exist.',
            RuntimeWarning,
            stacklevel=0,
        )
    elif not project.target.is_dir():
        warn(
            f'Bail out! target: {project.target}\ntarget is not a directory.',
            RuntimeWarning,
        )
    project.add.remove('ozi.phony')
    project.add = list(set(project.add))
    project.remove.remove('ozi.phony')
    project.remove = list(set(project.remove))
    return project


@contextmanager
def redirect_argv(*args: str) -> Generator[None, None, None]:  # pragma: no cover
    argv = sys.argv[:]
    sys.argv = list(args)
    yield
    sys.argv = argv


@contextmanager
def nogc() -> Generator[None, None, None]:  # pragma: no cover
    gc.freeze()
    if gc.isenabled():
        gc.disable()
    yield
    gc.unfreeze()
    gc.enable()
    gc.collect()


def run_utility(name: str, *args: str) -> None:  # pragma: no cover
    with nogc():
        with redirect_argv(name, *args):
            print('# run-utility:', *sys.argv)
            with suppress(SystemExit):
                run_module(name)


def main() -> NoReturn:  # pragma: no cover
    """Main ozi.fix entrypoint."""
    project = preprocess(parser.parse_args())
    env.globals = env.globals | {'project': vars(project)}
    name, *_ = report_missing(
        project.target,
        stdout=print if project.missing else lambda *_: None,  # type: ignore
    )
    if name is None:
        exit(1)
    if hasattr(project, 'run_utility') and project.run_utility:
        run_utility('isort', '-q', str(project.target))
        for i in [underscorify(name), 'tests']:
            run_utility('autoflake', '-i', str(project.target / i / '**' / '*.py'))
            run_utility('black', '-q', '-S', str(project.target / i))

    project.name = underscorify(name)
    project.license_file = 'LICENSE.txt'
    project.copyright_head = '\n'.join(
        [
            f'Part of {name}.',
            f'See {project.license_file} in the project root for details.',
        ],
    )
    rewriter = Rewriter(project.target, project.name, project.fix)
    rewriter += project.add
    rewriter -= project.remove
    if not project.missing:
        print(json.dumps(rewriter.commands, indent=4 if project.pretty else None))
    exit(0)


if __name__ == '__main__':
    main()
