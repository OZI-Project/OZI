# ozi/fix/parser.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""``ozi-fix`` argparse argument parser."""
import argparse
import sys
from argparse import SUPPRESS
from argparse import ArgumentParser
from argparse import BooleanOptionalAction

parser = ArgumentParser(description=sys.modules[__name__].__doc__, add_help=False)
subparser = parser.add_subparsers(help='source & test fix', dest='fix')

helpers = parser.add_mutually_exclusive_group()
helpers.add_argument('-h', '--help', action='help', help='show this help message and exit')
missing_parser = subparser.add_parser(
    'missing',
    aliases=['m'],
    allow_abbrev=True,
    help='Check for missing files in an OZI project.',
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
    default=False,
    action=BooleanOptionalAction,
    help='strict mode raises warnings to errors default: --no-strict',
)
missing_parser.add_argument(
    '--pretty',
    default=False,
    action=BooleanOptionalAction,
    help='pretty mode outputs indented json, default: --no-pretty',
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
    aliases=['s'],
    allow_abbrev=True,
    help='Create a new Python source in an OZI project.',
)
test_parser = subparser.add_parser(
    'test',
    aliases=['t'],
    allow_abbrev=True,
    help='Create a new Python test in an OZI project.',
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
    help='strict mode raises warnings to errors.',
)
test_output.add_argument(
    '-p',
    '--pretty',
    action='store_true',
    help='pretty print JSON output',
)
tools = parser.add_mutually_exclusive_group()  # pragma: no cover
tools.add_argument(  # pragma: no cover
    '-fix',
    action='store_true',
    help=argparse.SUPPRESS,
)
