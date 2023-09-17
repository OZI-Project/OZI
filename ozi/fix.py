# ozi/fix.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""ozi-fix: Project fix script that outputs a meson rewriter JSON array."""
import argparse
import json
import os
import re
import sys
from email import message_from_file
from email.message import Message
from pathlib import Path
from typing import Dict, List, NoReturn, Tuple, Union

from pyparsing import (
    CaselessKeyword,
    Combine,
    Keyword,
    OneOrMore,
    ParseException,
)
from pyparsing import ParseResults, Suppress, White, oneOf

from .assets import underscorify, spdx_license_expression
from .assets.structure import root_files, source_files, test_files

parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__, add_help=False)
parser.add_argument('target', type=str, help='target OZI project directory')
parser.add_argument(
    '-a',
    '--add',
    nargs='?',
    action='append',
    default=['ozi.phony'],
    help='add file or dir/ to project',
)
parser.add_argument(
    '-r',
    '--remove',
    nargs='?',
    action='append',
    default=['ozi.phony'],
    help='remove file or dir/ from project',
)
output = parser.add_argument_group('output')
output.add_argument(
    '--strict',
    default='--no-strict',
    action=argparse.BooleanOptionalAction,
    help='strict mode raises warnings to errors.',
)
output.add_argument('-p', '--pretty', action='store_true', help='pretty print JSON output')
helpers = parser.add_mutually_exclusive_group()
helpers.add_argument('-h', '--help', action='help', help='show this help message and exit')
helpers.add_argument(
    '-m',
    '--missing',
    action='store_true',
    help='print missing files and exit with code set to miss count',
)


def _str_dict_union(toks: ParseResults) -> Dict[str, str]:
    """Parse-time union of Dict[str, str]."""
    return toks[0] | toks[1]  # type: ignore


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
    target: Path, strict: bool, use_tap: bool
) -> Union[Tuple[str, Message, List[Path], List[Path], List[Path]], NoReturn]:
    """Report missing OZI project files

    :param target: Relative path to target directory.
    :param strict: Whether to treat warnings as errors.
    :param use_tap: print using Test Anything Protocol and exit.
    :return: Normalized Name, PKG-INFO, found_root, found_sources, found_tests
    """
    target = Path(target)
    miss_count = 0
    count = 0
    with target.joinpath('PKG-INFO').open() as f:
        pkg_info = message_from_file(f)
        count += 1
        if use_tap:
            print('ok', count, '-', 'Parse PKG-INFO')
    for k, v in pkg_info.items():
        count += 1
        if use_tap:
            print('ok', count, '-', f'{k}:', v)
    name = re.sub(r'[-_.]+', '-', pkg_info['Name']).lower()
    try:
        extra_pkg_info = pkg_info_extra(pkg_info.get_payload()).items()
    except ParseException:
        count += 1
        print('not', 'ok', count, '-', 'PKG-INFO', 'OZI', 'Extra-Content', 'MISSING')
        extra_pkg_info = {}
    for k, v in extra_pkg_info:
        count += 1
        if use_tap:
            print('ok', count, '-', f'{k}:', v)
    found_root_files = []
    for file in root_files:
        count += 1
        if not target.joinpath(file).exists():
            if use_tap:
                print('not', 'ok', count, '-', Path(file))
            miss_count += 1
            continue
        elif use_tap:
            print('ok', count, '-', Path(file))
        found_root_files.append(file)
    extra_root_files = [
        file for file in os.listdir(target) if os.path.isfile(os.path.join(target, file))
    ]
    extra_root_files = list(
        set(extra_root_files).symmetric_difference(set(found_root_files))
    )
    for file in extra_root_files:
        count += 1
        if use_tap:
            print('ok', count, '#', 'SKIP', file)

    found_source_files = []
    for file in source_files:
        count += 1
        if not target.joinpath(underscorify(name), file).exists():
            if use_tap:
                print('not', 'ok', count, Path(underscorify(name), file), 'MISSING')
            miss_count += 1
            continue
        elif use_tap:
            print('ok', count, '-', Path(underscorify(name), file))
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
        if use_tap:
            print('ok', count, '#', 'SKIP', Path(underscorify(name)) / file)

    found_test_files = []
    for file in test_files:
        count += 1
        if not target.joinpath('tests', file).exists():
            if use_tap:
                print('not', 'ok', count, '-', Path('tests', file), 'MISSING')
            miss_count += 1
            continue
        else:
            if use_tap:
                print('ok', count, '-', Path('tests', file))
        found_test_files.append(file)
    try:
        extra_test_files = [
            file
            for file in os.listdir(target / 'tests')
            if os.path.isfile(os.path.join(target, 'tests', file))
        ]
    except FileNotFoundError:
        extra_test_files = []
    extra_test_files = list(
        set(extra_test_files).symmetric_difference(set(found_test_files))
    )
    for file in extra_test_files:
        count += 1
        if use_tap:
            print('ok', count, '#', 'SKIP', Path('tests', file))
    if use_tap:
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
        expected = f'{sum(map(len, all_files))+miss_count}'
        print(f'1..{expected}')
        exit(miss_count)
    return name, pkg_info, found_root_files, found_source_files, found_test_files


def main() -> Union[NoReturn, str]:
    """Main ozi.fix entrypoint."""
    project = parser.parse_args()
    project.target = Path(project.target).absolute()
    rewriter = []
    src_add = {
        'type': 'target',
        'target': '',
        'operation': 'src_add',
        'sources': [''],
        'subdir': '',
        'target_type': '',
    }
    if not project.target.exists():
        raise ValueError(f'target: {project.target}\ntarget does not exist.')
    if not project.target.is_dir():
        raise ValueError(f'target: {project.target}\ntarget is not a directory.')
    project.add.remove('ozi.phony')
    project.add = list(set(project.add))
    project.remove.remove('ozi.phony')
    project.remove = list(set(project.remove))
    name, pkg_info, found_root_files, found_source_files, found_test_files = report_missing(
        project.target, project.strict, project.missing
    )
    extra_source_files = [
        x for x in (project.target / project.name).glob('./*') if x.is_file()
    ]
    extra_source_files = list(set(extra_source_files + found_source_files))
    add_source_files = []
    for file in project.add:
        if file.is_dir():
            (project.target / file).mkdir()
        elif file.is_file():
            add_source_files += [file]
    if len(add_source_files) > 0:
        args = src_add.copy()
        args.update({'target': 'source_files', 'sources': add_source_files})
        rewriter.append(args)
    print(extra_source_files)
    print(json.dumps(rewriter, indent=4))
    return 'ok'


if __name__ == '__main__':
    main()
