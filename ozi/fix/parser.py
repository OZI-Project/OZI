# ozi/fix/parser.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""``ozi-fix`` console application."""
import argparse
import sys
from argparse import SUPPRESS
from argparse import ArgumentParser
from argparse import BooleanOptionalAction

parser = ArgumentParser(
    prog='ozi-fix',
    description=sys.modules[__name__].__doc__,
    add_help=False,
    usage="""%(prog)s [options] | [positional arguments]

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
does not create an attorney-client relationship.
""",
)
parser.add_argument('target', default='.', type=str, nargs='?', help=argparse.SUPPRESS)
parser.add_argument(
    '--add',
    metavar='FILENAME',
    nargs='?',
    action='append',
    default=['ozi.phony'],
    help=SUPPRESS,
)
parser.add_argument(
    '--remove',
    metavar='FILENAME',
    nargs='?',
    action='append',
    default=['ozi.phony'],
    help=SUPPRESS,
)
parser.add_argument(
    '--strict',
    default=False,
    action=BooleanOptionalAction,
    help=SUPPRESS,
)
parser.add_argument(
    '--pretty',
    default=False,
    action=BooleanOptionalAction,
    help=SUPPRESS,
)
subparser = parser.add_subparsers(help='', metavar='', dest='fix')

helpers = parser.add_mutually_exclusive_group()
helpers.add_argument('-h', '--help', action='help', help='show this help message and exit')
missing_parser = subparser.add_parser(
    'missing',
    prog='ozi-fix missing',
    aliases=['m', 'mis'],
    usage='%(prog)s [options] [output] target',
    allow_abbrev=True,
    help='Check for missing files in an OZI project.',
)
missing_parser.add_argument(
    '--add',
    metavar='FILENAME',
    nargs='?',
    action='append',
    default=['ozi.phony'],
    help=SUPPRESS,
)
missing_parser.add_argument(
    '--remove',
    metavar='FILENAME',
    nargs='?',
    action='append',
    default=['ozi.phony'],
    help=SUPPRESS,
)
missing_output = missing_parser.add_argument_group('output')
missing_output.add_argument(
    '--strict',
    default=False,
    action=BooleanOptionalAction,
    help='strict mode raises warnings to errors, default: no',
)
missing_output.add_argument(
    '--pretty',
    default=False,
    action=BooleanOptionalAction,
    help='pretty mode outputs indented json, default: no',
)
missing_parser.add_argument(
    'target',
    type=str,
    nargs='?',
    default='.',
    help='target OZI project directory',
)
source_parser = subparser.add_parser(
    'source',
    aliases=['s', 'src'],
    prog='ozi-fix source',
    usage='%(prog)s [options] [output] target',
    allow_abbrev=True,
    help='Create a new Python source in an OZI project.',
)
test_parser = subparser.add_parser(
    'test',
    prog='ozi-fix test',
    usage='%(prog)s [options] [output] target',
    aliases=['t', 'tests'],
    allow_abbrev=True,
    help='Create a new Python test in an OZI project.',
)
source_parser.add_argument(
    '-a',
    '--add',
    metavar='FILENAME',
    nargs='?',
    action='append',
    default=['ozi.phony'],
    help='add file or dir/ to project',
)
source_parser.add_argument(
    '-r',
    '--remove',
    metavar='FILENAME',
    nargs='?',
    action='append',
    default=['ozi.phony'],
    help='remove file or dir/ from project',
)
source_parser.add_argument(
    '-c',
    '--copyright-head',
    metavar='HEADER',
    type=str,
    default='',
    help='copyright header string',
)
source_parser.add_argument(
    'target',
    type=str,
    nargs='?',
    default='.',
    help='target OZI project directory',
)
source_output = source_parser.add_argument_group('output')
source_output.add_argument(
    '--strict',
    default=False,
    action=BooleanOptionalAction,
    help='strict mode raises warnings to errors, default: no',
)
source_output.add_argument(
    '--pretty',
    default=False,
    action=BooleanOptionalAction,
    help='pretty mode outputs indented json, default: no',
)
test_parser.add_argument(
    '-a',
    '--add',
    metavar='FILENAME',
    nargs='?',
    action='append',
    default=['ozi.phony'],
    help='add file or dir/ to project',
)
test_parser.add_argument(
    '-r',
    '--remove',
    metavar='FILENAME',
    nargs='?',
    action='append',
    default=['ozi.phony'],
    help='remove file or dir/ from project',
)
test_parser.add_argument(
    '-c',
    '--copyright-head',
    metavar='HEADER',
    type=str,
    default='',
    help='copyright header string',
)
test_parser.add_argument(
    'target',
    type=str,
    nargs='?',
    default='.',
    help='target OZI project directory',
)
test_output = test_parser.add_argument_group('output')
test_output.add_argument(
    '--strict',
    default=False,
    action=BooleanOptionalAction,
    help='strict mode raises warnings to errors, default: no',
)
test_output.add_argument(
    '--pretty',
    default=False,
    action=BooleanOptionalAction,
    help='pretty mode outputs indented json, default: no',
)
tools = parser.add_mutually_exclusive_group()  # pragma: no cover
tools.add_argument(  # pragma: no cover
    '-fix',
    action='store_true',
    help=argparse.SUPPRESS,
)
