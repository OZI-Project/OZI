"""ozi-fix: Project fix script that outputs a meson rewriter JSON array."""

import argparse
import json
from pathlib import Path
import re
import sys
from typing import NoReturn, Union
from warnings import warn

from pyparsing import Regex


from .assets.structure import root_files, source_files

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
output.add_argument('-p', '--pretty', action='store_true', help='pretty print JSON output')
helpers = parser.add_mutually_exclusive_group()
helpers.add_argument('-h', '--help', action='help', help='show this help message and exit')
helpers.add_argument(
    '-m',
    '--missing',
    action='store_true',
    help='print missing files and exit with code set to miss count',
)


def main() -> Union[NoReturn, None]:
    """Main ozi.fix entrypoint."""
    project = parser.parse_args()
    project.target = Path(project.target).absolute()
    rewriter = []
    src_add = {
        'type': 'target',
        'target': None,
        'operation': 'src_add',
        'sources': None,
        'subdir': '',
        'target_type': '',
    }
    miss_count = 0
    if not project.target.exists():
        raise ValueError(f'target: {project.target}\ntarget does not exist.')
    if not project.target.is_dir():
        raise ValueError(f'target: {project.target}\ntarget is a file.')
    project.add.remove('ozi.phony')
    project.add = list(set(project.add))
    project.remove.remove('ozi.phony')
    project.remove = list(set(project.remove))
    for file in root_files:
        if not project.target.joinpath(file).exists():
            print(f'Missing REQUIRED OZI project file: {file}')
            miss_count += 1
    with project.target.joinpath('PKG-INFO').open() as f:
        line = [next(f) for _ in range(2)][1]
        name = Regex(
            '^(Name: )([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9._-]*[A-Za-z0-9])$',
            as_match=True,
        ).parse_string(line)[0][2]
        project.name = re.sub(r'[-_.]+', '-', name).lower()  # type: ignore

    found_root_files = []
    for file in root_files:
        if not project.target.joinpath(file).exists():
            if project.missing:
                print(Path(file))
            miss_count += 1
            continue
        found_root_files.append(project.target.joinpath(project.name, file))
    extra_root_files = [x for x in project.target.glob('./*') if x.is_file()]
    extra_root_files = list(set(extra_root_files + found_root_files))

    found_source_files = []
    for file in source_files:
        if not project.target.joinpath(project.name, file).exists():
            if project.missing:
                print(Path(project.name, file))
            miss_count += 1
            continue
        found_source_files.append(project.target.joinpath(project.name, file))
    if project.missing:
        if any(project.add):
            warn('--missing is set: Ignoring -a/--add arguments', SyntaxWarning)
        if any(project.remove):
            warn('--missing is set: Ignoring -r/--remove arguments', SyntaxWarning)
        exit(miss_count)
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
    print(json.dumps(rewriter, indent=4))
    print(extra_source_files)


if __name__ == '__main__':
    main()
