# ozi/__main__.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""``ozi`` console application."""  # pragma: no cover
from __future__ import annotations  # pragma: no cover

import argparse  # pragma: no cover
import sys  # pragma: no cover
from dataclasses import fields  # pragma: no cover

from ozi_core._i18n import TRANSLATION  # pragma: no cover  # pyright: ignore
from ozi_core.actions import ExactMatch  # pragma: no cover  # pyright: ignore
from ozi_core.actions import check_version  # pragma: no cover  # pyright: ignore
from ozi_core.actions import info  # pragma: no cover  # pyright: ignore
from ozi_core.actions import license_expression  # pragma: no cover  # pyright: ignore
from ozi_core.actions import list_available  # pragma: no cover  # pyright: ignore
from ozi_core.actions import uninstall_user_files  # pragma: no cover  # pyright: ignore

from ozi import __version__

EPILOG = f"""
METADATA_FIELD {TRANSLATION('term-choices')}:
  | audience
  | environment
  | framework
  | language
  | license
  | license-exception-id
  | license-id
  | status
  | topic

LICENSE_EXPR: :term:`SPDX license expression` {TRANSLATION('term-spdx-license-expression')}
  | {TRANSLATION('term-see-ref')} https://spdx.github.io/spdx-spec/v2-draft/SPDX-license-expressions/

{TRANSLATION('term-project-authoring-console-app')}:
  | ``ozi-new -h``         {TRANSLATION('term-help-new')}

{TRANSLATION('term-project-maintenance-console-app')}:
  | ``ozi-fix -h``         {TRANSLATION('term-help-fix')}

{TRANSLATION('term-continuous-integration-checkpoints')}:
  | ``tox -e lint``        {TRANSLATION('term-tox-e-lint')}
  | ``tox -e test``        {TRANSLATION('term-tox-e-test')}
  | ``tox -e dist``        {TRANSLATION('term-tox-e-dist')}
"""  # pragma: no cover

parser = argparse.ArgumentParser(
    prog='ozi',
    description=sys.modules[__name__].__doc__,
    add_help=False,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=EPILOG,
    usage=f"""%(prog)s [{TRANSLATION('term-options')}]

{TRANSLATION('adm-disclaimer-text')}""",
)  # pragma: no cover
tools = parser.add_mutually_exclusive_group()  # pragma: no cover
helpers = parser.add_mutually_exclusive_group()  # pragma: no cover
helpers.add_argument(
    '-h',
    '--help',
    action='help',
    help=TRANSLATION('term-help-help'),
)  # pragma: no cover
helpers.add_argument(  # pragma: no cover
    '-v',
    '--version',
    action='store_const',
    default=lambda: None,
    const=lambda: print(__version__) or exit(0),
    help=TRANSLATION('term-help-version'),
)
helpers.add_argument(  # pragma: no cover
    '-c',
    '--check-version',
    action='store_const',
    default=lambda: None,
    const=lambda: check_version(__version__),
    help=TRANSLATION('term-help-check-version'),
)
helpers.add_argument(  # pragma: no cover
    '-e',
    '--check-license-expr',
    metavar='LICENSE_EXPR',
    action='store',
    help=TRANSLATION('term-help-valid-license-expression'),
)
helpers.add_argument(  # pragma: no cover
    '-i',
    '--info',
    action='store_const',
    default=lambda: None,
    const=lambda: info(__version__),
    help=TRANSLATION('term-help-info'),
)
helpers.add_argument(  # pragma: no cover
    '-l',
    '--list-available',
    help=TRANSLATION('term-help-list-available'),
    default=None,
    metavar='METADATA_FIELD',
    action='store',
    choices={i.name.replace('_', '-') for i in fields(ExactMatch) if i.repr},
)
helpers.add_argument(
    '--uninstall-user-files',
    help=TRANSLATION('term-help-uninstall-user-files'),
    action='store_const',
    default=lambda: None,
    const=lambda: uninstall_user_files(),
)


def main() -> None:  # pragma: no cover
    """``ozi`` script entrypoint."""
    ozi, _ = parser.parse_known_args()
    ozi.version()
    ozi.check_version()
    ozi.info()
    ozi.uninstall_user_files()
    if ozi.list_available:
        list_available(ozi.list_available)
    if ozi.check_license_expr:
        license_expression(ozi.check_license_expr)
    parser.print_help()


if __name__ == '__main__':
    main()
