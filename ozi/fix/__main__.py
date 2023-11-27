from __future__ import annotations

import json
import os
import re
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from email import message_from_file
from email.message import Message
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Annotated
from typing import Any
from typing import NoReturn
from typing import Union
from warnings import warn

if TYPE_CHECKING:
    import sys
    from argparse import Namespace
    from collections.abc import Callable
    from collections.abc import Mapping

    from jinja2 import Template

    if sys.version_info >= (3, 11):
        from typing import Self
    elif sys.version_info <= (3, 10):
        from typing_extensions import Self

from pyparsing import CaselessKeyword
from pyparsing import Combine
from pyparsing import Forward
from pyparsing import Keyword
from pyparsing import Literal
from pyparsing import ParseException
from pyparsing import ParseResults
from pyparsing import Suppress
from pyparsing import White
from pyparsing import oneOf

from ozi.experimental import run_utility
from ozi.filter import underscorify
from ozi.fix.parser import parser
from ozi.render import env
from ozi.spdx import spdx_license_expression
from ozi.spec import Metadata
from ozi.spec import PythonSupport
from ozi.tap import TAP

python_support = PythonSupport()

metadata = Metadata()


def _str_dict_union(toks: ParseResults) -> Any | ParseResults:
    """Parse-time union of dict[str, str]."""
    if len(toks) >= 2:
        return dict(toks[0]) | dict(toks[1])
    else:  # pragma: no cover
        return None


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
    Keyword('..') + CaselessKeyword('ozi'),
) + pep639_headers.set_parse_action(_str_dict_union).set_name('pep639')


def pkg_info_extra(payload: str, as_message: bool = True) -> dict[str, str] | Message:
    """Get extra PKG-INFO Classifiers tacked onto the payload by OZI."""
    pep639: dict[str, str] = pep639_parse.parse_string(payload)[0]  # pyright: ignore
    if as_message:
        msg = Message()
        for k, v in pep639.items():
            msg.add_header('Classifier', f'{k} :: {v}')
        return msg
    return pep639


def parse_extra_pkg_info(pkg_info: Message) -> tuple[dict[str, str], str | None]:
    errstr = None
    try:
        extra_pkg_info = dict(pkg_info_extra(pkg_info.get_payload()))
    except ParseException as e:  # pragma: defer to good-first-issue
        extra_pkg_info = {}
        newline = '\n'
        errstr = str(e).replace(newline, ' ')
    return extra_pkg_info, errstr


def missing_python_support(pkg_info: Message) -> set[tuple[str, str]]:
    """Check PKG-INFO Message for python support."""
    remaining_pkg_info = {
        (k, v)
        for k, v in pkg_info.items()
        if k not in metadata.spec.python.pkg.info.required
    }
    for k, v in iter(python_support.classifiers[:4]):
        if (k, v) in remaining_pkg_info:
            TAP.ok(k, v)
        else:
            TAP.not_ok('MISSING', v)
    return remaining_pkg_info


def missing_ozi_required(pkg_info: Message) -> dict[str, str]:
    """Check missing required OZI extra PKG-INFO"""
    remaining_pkg_info = missing_python_support(pkg_info)
    remaining_pkg_info.difference_update(set(iter(python_support.classifiers)))
    for k, v in iter(remaining_pkg_info):
        TAP.ok(k, v)
    extra_pkg_info, errstr = parse_extra_pkg_info(pkg_info)
    if errstr not in ('', None):  # pragma: defer to good-first-issue
        TAP.not_ok('MISSING', str(errstr))
    return extra_pkg_info


def missing_required(
    target: Path,
) -> tuple[str, dict[str, str]]:
    """Find missing required PKG-INFO"""
    with target.joinpath('PKG-INFO').open() as f:
        pkg_info = message_from_file(f)
        TAP.ok('Parse PKG-INFO')
    for i in metadata.spec.python.pkg.info.required:
        v = pkg_info.get(i, None)
        if v is not None:
            TAP.ok(i, v)
        else:
            TAP.not_ok('MISSING', i)
    extra_pkg_info = missing_ozi_required(pkg_info)
    name = re.sub(r'[-_.]+', '-', pkg_info.get('Name', '')).lower()
    for k, v in extra_pkg_info.items():
        TAP.ok(k, v)
    return name, extra_pkg_info


@TAP
def comment_diagnostic(  # pragma: defer to TAP-Consumer
    lines: list[str],
    rel_path: Path,
) -> None:
    for i, line in enumerate(lines, start=1):
        if s := re.search(
            metadata.spec.python.src.comments.noqa,
            line,
        ):  # pragma: defer to TAP-Consumer
            TAP.diagnostic('noqa  ', f'{rel_path!s}:{i}', s[0].strip())
            continue
        if s := re.search(
            metadata.spec.python.src.comments.type,
            line,
        ):  # pragma: defer to TAP-Consumer
            TAP.diagnostic('type  ', f'{rel_path!s}:{i}', s[0].strip())
            continue
        if s := re.search(
            metadata.spec.python.src.comments.pragma_defer_to,
            line,
        ):  # pragma: defer to TAP-Consumer
            TAP.diagnostic('defer ', f'{rel_path!s}:{i}', s[0].strip())
            continue
        if s := re.search(
            metadata.spec.python.src.comments.pragma_no_cover,
            line,
        ):  # pragma: defer to TAP-Consumer
            TAP.diagnostic('no cov', f'{rel_path!s}:{i}', s[0].strip())
            continue


def missing_required_files(  # noqa: C901
    kind: str,
    target: Path,
    name: str,
) -> tuple[list[str], list[str]]:
    """Count missing files required by OZI"""
    found_files = []
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
                TAP.not_ok('MISSING', str(f))
                continue  # pragma: defer to https://github.com/nedbat/coveragepy/issues/198
            case f if f and str(f).endswith('.py'):
                with open(target.joinpath(f)) as fh:
                    comment_diagnostic(fh.readlines(), f)
        TAP.ok(str(f))
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
                build_file = str((rel_path / file).parent / 'meson.build')
                TAP.ok(f'{build_file} lists {rel_path / file}')
        build_files += [str(rel_path / file)]
        match file:
            case file if str(file).endswith('.py') and str(
                rel_path / file,
            ) not in build_files:
                build_file = str(rel_path / 'meson.build')
                TAP.not_ok('MISSING', '{build_file}: {rel_path / file!s}')
            case file if str(file).endswith('.py'):
                with open(target.joinpath(rel_path) / file) as g:
                    comment_diagnostic(g.readlines(), rel_path / file)
    return found_files, extra_files


@TAP
def report_missing(
    target: Path,
) -> tuple[str, Message | None, list[str], list[str], list[str]] | NoReturn:
    """Report missing OZI project files
    :param target: Relative path to target directory.
    :return: Normalized Name, PKG-INFO, found_root, found_sources, found_tests
    """
    target = Path(target)
    name = None
    pkg_info = None
    extra_pkg_info: dict[str, str] = {}
    try:
        name, extra_pkg_info = missing_required(target)
    except FileNotFoundError:
        name = ''
        TAP.not_ok('MISSING', 'PKG-INFO')
    found_source_files, extra_source_files = missing_required_files('source', target, name)
    found_test_files, extra_test_files = missing_required_files('test', target, name)
    found_root_files, extra_root_files = missing_required_files('root', target, name)
    all_files = (  # pragma: defer to TAP-Consumer
        ['PKG-INFO'],
        extra_pkg_info,
        found_root_files,
        found_source_files,
        found_test_files,
        extra_root_files,
        extra_source_files,
        extra_test_files,
    )
    try:  # pragma: defer to TAP-Consumer
        sum(map(len, all_files))
    except TypeError:  # pragma: defer to TAP-Consumer
        TAP.bail_out('MISSING required files or metadata.')
    return (  # pragma: defer to TAP-Consumer
        name,
        pkg_info,
        found_root_files,
        found_source_files,
        found_test_files,
    )


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
            'root': env.get_template(metadata.spec.python.src.template.add_root),
            'source': env.get_template(metadata.spec.python.src.template.add_source),
            'test': env.get_template(metadata.spec.python.src.template.add_root),
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
    project.missing = project.fix == 'missing' or project.fix == 'm'
    project.target = Path(os.path.relpath(os.path.join('/', project.target), '/')).absolute()
    if not project.target.exists():
        TAP.bail_out(f'target: {project.target} does not exist.')
    elif not project.target.is_dir():
        TAP.bail_out(f'target: {project.target} is not a directory.')
    project.add.remove('ozi.phony')
    project.add = list(set(project.add))
    project.remove.remove('ozi.phony')
    project.remove = list(set(project.remove))
    return project


def main() -> NoReturn:  # pragma: no cover
    """Main ozi.fix entrypoint."""
    project = preprocess(parser.parse_args())
    env.globals = env.globals | {'project': vars(project)}

    match [project.missing, project.strict]:
        case [True, False]:
            name, *_ = report_missing(project.target)
            if hasattr(project, 'run_utility') and project.run_utility:
                run_utility('ruff', 'check', '--fix', str(project.target))
                run_utility('isort', '-q', str(project.target))
                for i in [underscorify(name), 'tests']:
                    run_utility('autoflake', '-i', str(project.target / i / '**' / '*.py'))
                    run_utility('black', '-q', '-S', str(project.target / i))
            TAP.end()
        case [False, _]:
            with TAP.suppress():
                name, *_ = report_missing(project.target)
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
            print(json.dumps(rewriter.commands, indent=4 if project.pretty else None))
        case [True, True]:
            with TAP.strict():
                name, *_ = report_missing(project.target)
            TAP.end()
        case [_, _]:
            TAP.bail_out('Name discovery failed.')
    exit(0)


if __name__ == '__main__':
    main()
