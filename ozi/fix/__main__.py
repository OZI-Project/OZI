# ozi/fix/__main__.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""ozi-fix entrypoint script."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import NoReturn

from ozi_spec import METADATA  # pyright: ignore
from ozi_templates import load_environment  # type: ignore
from ozi_templates.filter import underscorify  # type: ignore

from ozi.fix.missing import report
from ozi.fix.parser import parser
from ozi.fix.rewrite_command import Rewriter
from ozi.tap import TAP


def main() -> NoReturn:  # pragma: no cover
    """Main ozi.fix entrypoint."""
    project = parser.parse_args()
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
    env = load_environment(vars(project), METADATA.asdict())

    match [project.missing, project.strict]:
        case [True, False]:
            name, *_ = report(project.target)
            TAP.end()
        case [False, _]:
            with TAP.suppress():
                name, *_ = report(project.target)
                project.name = underscorify(name)
                project.license_file = 'LICENSE.txt'
                project.copyright_head = '\n'.join(
                    [
                        f'Part of {name}.',
                        f'See {project.license_file} in the project root for details.',
                    ],
                )
                rewriter = Rewriter(str(project.target), project.name, project.fix, env)
                rewriter += project.add
                rewriter -= project.remove
            if len(project.add) > 0 or len(project.remove) > 0:
                print(json.dumps(rewriter.commands, indent=4 if project.pretty else None))
            else:
                parser.print_help()
        case [True, True]:
            with TAP.strict():
                name, *_ = report(project.target)
            TAP.end()
        case [_, _]:
            TAP.bail_out('Name discovery failed.')
    exit(0)


if __name__ == '__main__':
    main()
