"""ozi-fix: Project fix script that outputs a meson rewriter JSON array."""

import argparse
from pathlib import Path
import re
import sys
from typing import NoReturn, Union

from pyparsing import Regex


from .assets.structure import root_files, source_files

parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__)
parser.add_argument('target', type=str, help='target project directory')
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
        'target_type': ''
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
            '^(Name: )([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9._-]*[A-Za-z0-9])$', as_match=True,
        ).parse_string(line)[0][2]
        project.name = re.sub(r'[-_.]+', '-', name).lower()  # type: ignore
    for file in source_files:
        if not project.target.joinpath(project.name, file).exists():
            print(f'Missing REQUIRED OZI project file: {file}')
            miss_count += 1

    add_source_files = []
    for file in project.add:
        if str(file).startswith(f'{project.name}/'):
            add_source_files += [file]
    if len(add_source_files) > 0:
        args = src_add.copy()
        args.update({
            'id': 'source_files',
            'sources': add_source_files})
        rewriter.append(args)
    print('total missing files: ', miss_count)
    print(rewriter)


if __name__ == '__main__':
    main()
