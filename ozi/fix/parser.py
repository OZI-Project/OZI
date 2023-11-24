import sys
from argparse import SUPPRESS
from argparse import ArgumentParser
from argparse import BooleanOptionalAction

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
    allow_abbrev=True,
    description='Check for missing files and run utilities in an OZI project.',
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
