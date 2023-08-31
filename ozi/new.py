"""OZI Standard API project creation script.
Required-only:
    project.author

Validated:
    project.name
    project.email
    project.summary
    project.license_spdx
    project.license
    project.topic
    project.status

"""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import re
from typing import NoReturn, Union
from urllib.parse import urlparse

from jinja2 import Environment, FileSystemLoader, select_autoescape
from spdx_license_list import LICENSES
from email_validator import validate_email, EmailNotValidError
from pyparsing import Regex, ParseException

from assets import status, topic

root_templates = [
    '.gitignore',
    'meson.build',
    'meson.options',
    'PKG-INFO',
    'pyproject.toml',
    'README.rst',
]
source_templates = [
    'project.name/__init__.py',
    'project.name/__init__.pyi',
    'project.name/meson.build',
]
env = Environment(
    loader=FileSystemLoader(['templates', 'templates/project.name']),
    autoescape=select_autoescape(),
    enable_async=True,
)
parser = argparse.ArgumentParser(description='OZI Python Project Packaging Quick-start')
parser.add_argument('--name', type=str, help='name of project', required=True)
parser.add_argument('--author', type=str, help='author of project', required=True)
parser.add_argument('--email', type=str, help='valid author email', required=True)
parser.add_argument('--summary', type=str, help='short summary', required=True)
parser.add_argument('--homepage', type=str, help='homepage URL', required=True)
parser.add_argument(
    'target', type=str, help='target directory for new project',
)
parser.add_argument(
    '--license-spdx',
    type=str,
    choices=[k for k, v in LICENSES.items() if v.deprecated_id is False],
    metavar='ID',
    help='SPDX short ID',
)
parser.add_argument(
    '--license', type=str, help='license classifier (Pending PEP 639 Deprecation)'
)
parser.add_argument(
    '--copyright-head',
    type=str,
    default='',
    help='copyright header string',
    metavar='COPYRIGHT_HEAD="Copyright {year}, {project.author}\\nSee LICENSE..."',
)
parser.add_argument(
    '--topic',
    choices=topic.choices,
    default='Utilities',
    help='Python package topic',
    metavar='TOPIC="Utilities"',
    type=str,
)
parser.add_argument(
    '--status',
    choices=status.choices,
    default='1 - Planning',
    help='Python package status',
    metavar='STATUS="1 - Planning"',
    type=str,
)


def main() -> Union[NoReturn, None]:
    """Main ozi.new entrypoint."""
    project = parser.parse_args()

    if len(project.copyright_head) == 0:
        copyright_year = datetime.now(tz=datetime.now(timezone.utc).astimezone().tzinfo).year
        project.copyright_head = '\n'.join(
            [
                f'Copyright {copyright_year}, {project.author}',
                'See LICENSE.txt in the project root for details.',
            ]
        )

    if len(project.summary) > 512:
        raise ValueError('Project summary exceeds 512 characters in length.')

    try:
        emailinfo = validate_email(project.email, check_deliverability=True)
    except EmailNotValidError as e:
        raise ValueError(str(e), 'Invalid maintainer email format or domain unreachable.')

    try:
        Regex('^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$', re.IGNORECASE).parse_string(
            project.name
        )
    except ParseException as e:
        raise ValueError(str(e), 'Invalid project name.')

    home_url = urlparse(project.homepage).geturl
    if home_url.scheme != 'https':
        raise ValueError('Homepage url scheme unsupported.')

    if home_url.netloc == '':
        raise ValueError('Homepage url netloc cound not be parsed.')

    project.name = re.sub(r'[-_.]+', '-', project.name).lower()
    project.email = emailinfo.normalized
    project.target = Path(project.target)

    env.globals = {'project': vars(project)}
    Path(project.target, project.name).mkdir()
    Path(project.target, '.github', 'workflows').mkdir(parents=True)
    Path(project.target, 'subprojects').mkdir()
    Path(project.target, 'tests').mkdir()

    for filename in root_templates:
        template = env.get_template(f'{filename}.j2')
        with open(project.target / filename, 'w') as f:
            f.write(template.render())

    for filename in source_templates:
        template = env.get_template(f'{filename}.j2')
        with open(project.target / filename, 'w') as f:
            f.write(template.render())


if __name__ == '__main__':
    main()
