# ozi/__main__.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""``ozi`` console application.
"""  # pragma: no cover
from __future__ import annotations  # pragma: no cover

import argparse  # pragma: no cover
import sys  # pragma: no cover
from dataclasses import fields  # pragma: no cover

from ozi.actions import ExactMatch  # pragma: no cover
from ozi.actions import check_version  # pragma: no cover
from ozi.actions import info  # pragma: no cover
from ozi.actions import license_expression  # pragma: no cover
from ozi.actions import list_available  # pragma: no cover
from ozi.actions import print_version  # pragma: no cover
from ozi.fix.__main__ import main as fix_main  # pragma: no cover
from ozi.new.__main__ import main as new_main  # pragma: no cover

EPILOG = """
METADATA_FIELD choices:
  | audience
  | environment
  | framework
  | language
  | license
  | license-exception-id
  | license-id
  | status
  | topic

LICENSE_EXPR: :term:`SPDX license expression`
  | See https://spdx.github.io/spdx-spec/v2-draft/SPDX-license-expressions/

project authoring console application:
  | ``ozi-new -h``         show help for the ozi-new command.

project maintainence console application:
  | ``ozi-fix -h``         show help for the ozi-fix command.

continuous integration checkpoints:
  | ``tox -e lint``        run formatting, linting, and typechecking.
  | ``tox -e test``        run testing and coverage.
  | ``tox -e dist``        run distribution and packaging.
"""  # pragma: no cover

parser = argparse.ArgumentParser(
    prog='ozi',
    description=sys.modules[__name__].__doc__,
    add_help=False,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=EPILOG,
    usage="""%(prog)s [options]

The information provided on this application does not, and is not intended to,
constitute legal advice. All information, content, and materials available
on this application are for general informational purposes only.
Information on this application may not constitute the most up-to-date legal
or other information.

THE LICENSE TEMPLATES, LICENSE IDENTIFIERS, LICENSE CLASSIFIERS, AND
LICENSE EXPRESSION PARSING SERVICES, AND ALL OTHER CONTENTS ARE PROVIDED
"AS IS", NO REPRESENTATIONS ARE MADE THAT THE CONTENT IS ERROR-FREE
AND/OR APPLICABLE FOR ANY PURPOSE, INCLUDING MERCHANTABILITY.

Readers of this disclaimer should contact their attorney to obtain advice
with respect to any particular legal matter. The OZI Project is not a
law firm and does not provide legal advice. No reader or user of this
application should act or abstain from acting on the basis of information
on this application without first seeking legal advice from counsel in the
relevant jurisdiction. Legal counsel can ensure that the information
provided in this application is applicable to your particular situation.
Use of, or reading, this application or any of resources contained within
does not create an attorney-client relationship.""",
)  # pragma: no cover
tools = parser.add_mutually_exclusive_group()  # pragma: no cover
tools.add_argument(  # pragma: no cover
    '-fix',
    action='store_const',
    default=lambda: None,
    const=fix_main,
    help='alternate entrypoint for ozi-fix',
)
tools.add_argument(  # pragma: no cover
    '-new',
    action='store_const',
    default=lambda: None,
    const=new_main,
    help='alternate entrypoint for ozi-new',
)
helpers = parser.add_mutually_exclusive_group()  # pragma: no cover
helpers.add_argument(
    '-h',
    '--help',
    action='help',
    help='show this help message and exit',
)  # pragma: no cover
helpers.add_argument(  # pragma: no cover
    '-v',
    '--version',
    action='store_const',
    default=lambda: None,
    const=print_version,
    help=print_version.__doc__,
)
helpers.add_argument(  # pragma: no cover
    '-c',
    '--check-version',
    action='store_const',
    default=lambda: None,
    const=check_version,
    help=check_version.__doc__,
)
helpers.add_argument(  # pragma: no cover
    '-e',
    '--check-license-expr',
    metavar='LICENSE_EXPR',
    action='store',
    help=license_expression.__doc__,
)
helpers.add_argument(  # pragma: no cover
    '-i',
    '--info',
    action='store_const',
    default=lambda: None,
    const=info,
    help=info.__doc__,
)
helpers.add_argument(  # pragma: no cover
    '-l',
    '--list-available',
    help=list_available.__doc__,
    default=None,
    metavar='METADATA_FIELD',
    action='store',
    choices={i.name.replace('_', '-') for i in fields(ExactMatch) if i.repr},
)


def main() -> None:  # pragma: no cover
    """``ozi`` script entrypoint."""
    ozi, _ = parser.parse_known_args()
    ozi.version()
    ozi.check_version()
    ozi.info()
    if ozi.list_available:
        list_available(ozi.list_available)
    if ozi.check_license_expr:
        license_expression(ozi.check_license_expr)
    ozi.fix()
    ozi.new()
    parser.print_help()


if __name__ == '__main__':
    main()
