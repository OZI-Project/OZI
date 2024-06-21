# ozi/new/parser.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""``ozi-new`` console application.
"""
from __future__ import annotations

import argparse
import sys

from ozi.actions import CloseMatch
from ozi.spec import METADATA

parser = argparse.ArgumentParser(
    prog='ozi-new',
    description=sys.modules[__name__].__doc__,
    add_help=False,
    usage='%(prog)s [options] | [positional args]',  # noqa: B950,E501,RUF100
)
subparser = parser.add_subparsers(help='', metavar='', dest='new')
interactive_parser = subparser.add_parser(
    'interactive',
    aliases=['i'],
    description='Create a new Python project with OZI.',
    help='',
    prog='ozi-new interactive',
)
project_parser = subparser.add_parser(
    'project',
    aliases=['p'],
    description='Create a new Python project with OZI.',
    help='create new OZI project',
    prog='ozi-new project',
    usage='%(prog)s [options] [PKG-INFO required] [PKG-INFO optional] [PKG-INFO defaults] [defaults] target',  # noqa: B950,E501,RUF100
)
interactive_parser.add_argument(
    'target',
    type=str,
    nargs='?',
    default='.',
    help='directory path for new project (default: current working directory)',
)
required = project_parser.add_argument_group('PKG-INFO required')
optional = project_parser.add_argument_group('PKG-INFO optional')
defaults = project_parser.add_argument_group('PKG-INFO defaults')
ozi_defaults = project_parser.add_argument_group('defaults')
ozi_required = project_parser.add_argument_group('required')
ozi_defaults.add_argument(
    '-c',
    '--copyright-head',
    type=str,
    default='',
    help='copyright header string',
    metavar='HEADER',
)
ozi_defaults.add_argument(
    '--ci-provider',
    type=str,
    default='github',
    choices=frozenset(METADATA.spec.python.ci.providers),
    metavar='github',
    help='continuous integration and release provider',
)
required.add_argument(
    '-n',
    '--name',
    type=str,
    help='Name (Single Use)',
)
required.add_argument(
    '-a',
    '--author',
    type=str,
    help='Author (Multiple Use, Single output)',
    action='append',
    default=[],
    metavar='AUTHOR_NAMES',
    nargs='?',
)
required.add_argument(
    '-e',
    '--author-email',
    type=str,
    help='Author-email (Multiple Use, Single output)',
    default=[],
    metavar='AUTHOR_EMAILS',
    nargs='?',
    action='append',
)
required.add_argument(
    '-s',
    '--summary',
    type=str,
    help='Summary (Single Use)',
)
required.add_argument(
    '-p',
    '--home-page',
    type=str,
    help='Home-page (Single Use)',
)
required.add_argument(
    '--license-expression',
    type=str,
    help='Classifier: License Expression (Single Use, SPDX Expression)',
)
required.add_argument(
    '-l',
    '--license',
    type=str,
    help='Classifier: License (Single Use)',
    action=CloseMatch,
)
ozi_required.add_argument(
    'target',
    type=str,
    nargs='?',
    default='.',
    help='directory path for new project',
)
defaults.add_argument(
    '--audience',
    '--intended-audience',
    metavar='AUDIENCE_NAMES',
    type=str,
    help='Classifier: Intended Audience (Multiple Use), default: ["Other Audience"]',
    default=METADATA.spec.python.pkg.info.classifiers.intended_audience,
    nargs='?',
    action=CloseMatch,
)
defaults.add_argument(
    '--typing',
    type=str,
    choices=frozenset(('Typed', 'Stubs Only')),
    nargs='?',
    metavar='PY_TYPED_OR_STUBS',
    help='Classifier: Typing (Multiple Use), default: ["Typed"]',
    default=METADATA.spec.python.pkg.info.classifiers.typing,
)
defaults.add_argument(
    '--environment',
    metavar='ENVIRONMENT_NAMES',
    default=METADATA.spec.python.pkg.info.classifiers.environment,
    help='Classifier: Environment (Multiple Use), default: ["Other Environment"]',
    action=CloseMatch,
    nargs='?',
    type=str,
)
defaults.add_argument(
    '--license-file',
    default='LICENSE.txt',
    metavar='LICENSE_FILENAME',
    choices=frozenset(('LICENSE.txt',)),
    help='Classifier: License File (Single Use), default: "LICENSE.txt"',
    type=str,
)
optional.add_argument(
    '--keywords',
    default='',
    help='Keywords (Single Use, Comma-separated List)',
    type=str,
)
optional.add_argument(
    '--maintainer',
    default=[],
    action='append',
    nargs='?',
    metavar='MAINTAINER_NAMES',
    help='Maintainer (Multiple Use, Single output, if different from Author)',
)
optional.add_argument(
    '--maintainer-email',
    help='Maintainer-Email (Multiple Use, Single output, if different from Author-Email)',
    action='append',
    metavar='MAINTAINER_EMAILS',
    default=[],
    nargs='?',
)
optional.add_argument(
    '--framework',
    help='Classifier: Framework (Multiple Use)',
    metavar='FRAMEWORK_NAMES',
    action=CloseMatch,
    type=str,
    nargs='?',
    default=[],
)
optional.add_argument(
    '--project-url',
    help='Project-URL (Multiple Use, Comma-separated Tuple[name, url])',
    action='append',
    metavar='PROJECT_URLS',
    default=[],
    nargs='?',
)
defaults.add_argument(
    '--language',
    '--natural-language',
    metavar='LANGUAGE_NAMES',
    default=['English'],
    help='Classifier: Natural Language (Multiple Use), default: ["English"]',
    action=CloseMatch,
    type=str,
    nargs='?',
)
optional.add_argument(
    '--topic',
    help='Classifier: Topic (Multiple Use)',
    nargs='?',
    metavar='TOPIC_NAMES',
    action=CloseMatch,
    type=str,
    default=[],
)
defaults.add_argument(
    '--status',
    '--development-status',
    action=CloseMatch,
    default=METADATA.spec.python.pkg.info.classifiers.development_status,
    help='Classifier: Development Status (Single Use), default: "1 - Planning"',
    type=str,
)
defaults.add_argument(
    '--long-description-content-type',
    '--readme-type',
    metavar='README_TYPE',
    default='rst',
    choices=('rst', 'md', 'txt'),
    help='Description-Content-Type',
)
optional.add_argument(
    '-r',
    '--dist-requires',
    help='Dist-Requires (Multiple Use)',
    action='append',
    type=str,
    nargs='?',
    default=[],
    metavar='DIST_REQUIRES',
)
output = parser.add_mutually_exclusive_group()
output.add_argument('-h', '--help', action='help', help='show this help message and exit')
ozi_defaults.add_argument(
    '--verify-email',
    default=False,
    action=argparse.BooleanOptionalAction,
    help='verify email domain deliverability, default: no',
)
ozi_defaults.add_argument(
    '--enable-cython',
    default=False,
    action=argparse.BooleanOptionalAction,
    help='build extension module with Cython, default: no',
)
ozi_defaults.add_argument(
    '--strict',
    default=False,
    action=argparse.BooleanOptionalAction,
    help='strict mode raises warnings to errors, default',
)
ozi_defaults.add_argument(
    '--allow-file',
    help='Add a file to the allow list for new project target folder, default: [templates,.git]',
    action='append',
    type=str,
    nargs='?',
    metavar='ALLOW_FILE_PATTERNS',
    default=METADATA.spec.python.src.allow_files,
)
tools = parser.add_mutually_exclusive_group()  # pragma: no cover
tools.add_argument(  # pragma: no cover
    '-new',
    action='store_true',
    help=argparse.SUPPRESS,
)
