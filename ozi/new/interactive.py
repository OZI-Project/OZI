"""
``ozi-new`` interactive prompts
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING
from typing import Sequence

import requests
from prompt_toolkit.shortcuts import button_dialog
from prompt_toolkit.shortcuts import checkboxlist_dialog
from prompt_toolkit.shortcuts import input_dialog
from prompt_toolkit.shortcuts import radiolist_dialog
from prompt_toolkit.shortcuts import yes_no_dialog
from prompt_toolkit.styles import Style
from prompt_toolkit.validation import ValidationError
from prompt_toolkit.validation import Validator

from ozi.spec import METADATA
from ozi.trove import Prefix
from ozi.trove import from_prefix

if TYPE_CHECKING:
    from prompt_toolkit.document import Document


class ProjectNameValidator(Validator):
    def validate(self, document: Document) -> None:  # pragma: no cover  # noqa: ANN101
        if not re.match(
            r'\A([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])\Z',
            document.text,
            flags=re.IGNORECASE,
        ):
            raise ValidationError(0, 'invalid project name')


class PackageValidator(Validator):
    def validate(self, document: Document) -> None:  # pragma: no cover  # noqa: ANN101
        if len(document.text) == 0:
            raise ValidationError(0, 'cannot be empty')
        response = requests.get(
            f'https://pypi.org/simple/{document.text}',
            timeout=15,
        )
        if response.status_code == 200:
            pass
        else:
            raise ValidationError(
                len(document.text),
                f'{response.status_code} package not found',
            )


style = Style.from_dict(
    {
        'button': '#e1e7ef',
        'dialog': 'bg:#030711',
        'dialog label': '#e1e7ef',
        'frame.border': '#192334',
        'dialog.body': 'bg:#000000 #00ff00',
        'dialog shadow': 'bg:#192334',
        'dialog text-area': '#030711',
    },
)


def interactive_prompt() -> list[str]:  # noqa: C901  # pragma: no cover
    output = ['project']
    project_name = input_dialog(
        title='ozi-new interactive prompt',
        text='What is the name of the project?',
        validator=ProjectNameValidator(),
        style=style,
        cancel_text='Skip',
    ).run()
    prefix = f'Name: {project_name if project_name else ""}\n'
    output += [f'--name="{project_name}"'] if project_name else []

    summary = input_dialog(
        title='ozi-new interactive prompt',
        text=prefix + 'What does the project do?\n(a short summary 1-2 sentences)',
        style=style,
        cancel_text='Skip',
    ).run()
    prefix += f'Summary: {summary if summary else ""}\n'
    output += [f'--summary"{summary if summary else ""}"']

    home_page = input_dialog(
        title='ozi-new interactive prompt',
        text=prefix + "What is the project's home-page URL?",
        style=style,
        cancel_text='Skip',
    ).run()
    prefix += f'Home-page: {home_page}\n'
    output += [f'--home-page="{home_page}"'] if home_page else []

    author_names = input_dialog(
        title='ozi-new interactive prompt',
        text=prefix + 'What is the author or authors name?\n(comma-separated list)',
        style=style,
        cancel_text='Skip',
    ).run()
    author_names = author_names.rstrip(',').split(',') if author_names else None  # type: ignore
    prefix += f'Author: {",".join(author_names if author_names else "")}\n'
    output += [f'--author="{a}"' for a in author_names] if author_names else []

    author_emails = input_dialog(
        title='ozi-new interactive prompt',
        text=prefix
        + 'What are the email addresses of the author or authors?\n(comma-separated list)',
        style=style,
        cancel_text='Skip',
    ).run()
    author_emails = author_emails.rstrip(',').split(',') if author_emails else None  # type: ignore
    prefix += f'Author-email: {",".join(author_emails if author_emails else "")}\n'
    output += [f'--author-email="{e}"' for e in author_emails] if author_emails else []

    if yes_no_dialog(
        title='ozi-new interactive prompt',
        text=prefix
        + 'Are there any maintainers of this project?\n(other than the author or authors)',
        style=style,
    ).run():
        maintainer_names = input_dialog(
            title='ozi-new interactive prompt',
            text=prefix
            + 'What is the maintainer or maintainers name?\n(comma-separated list)',
            style=style,
            cancel_text='Skip',
        ).run()
        maintainer_names = (
            maintainer_names.rstrip(',').split(',') if maintainer_names else None  # type: ignore
        )
        prefix += f'Maintainer: {",".join(maintainer_names if maintainer_names else [])}\n'
        output += (
            [f'--maintainer="{a}"' for a in maintainer_names] if maintainer_names else []
        )

        maintainer_emails = input_dialog(
            title='ozi-new interactive prompt',
            text=prefix
            + 'What are the email addresses of the maintainer or maintainers?\n(comma-separated list)',  # noqa: B950
            style=style,
            cancel_text='Skip',
        ).run()
        maintainer_emails = (
            maintainer_emails.rstrip(',').split(',') if maintainer_emails else None  # type: ignore
        )
        prefix += (
            f'Maintainer-email: {",".join(maintainer_emails if maintainer_emails else [])}\n'
        )
        output += (
            [f'--maintainer-email="{e}"' for e in maintainer_emails]
            if maintainer_emails
            else []
        )

    keywords = input_dialog(
        title='ozi-new interactive prompt',
        text=prefix + 'What are some project keywords?\n(comma-separated list)',
        style=style,
        cancel_text='Skip',
    ).run()
    keywords = keywords.rstrip(',').split(',') if keywords else None  # type: ignore
    prefix += f'Keywords: {",".join(keywords if keywords else "")}\n'
    output += [f'--keywords={",".join(keywords if keywords else [])}']

    requires_dist = []
    while button_dialog(
        title='ozi-new interactive prompt',
        text=prefix + 'Do you want to add a dependency requirement?',
        buttons=[
            ('Yes', True),
            ('No', False),
        ],
        style=style,
    ).run():
        requirement = input_dialog(
            title='ozi-new interactive prompt',
            text=prefix + 'Search PyPI packages:',
            validator=PackageValidator(),
            style=style,
            cancel_text='Skip',
        ).run()
        requires_dist += [requirement] if requirement else []
        prefix += f'Requires-Dist: {requirement}\n' if requirement else ''
        output += [f'--requires-dist="{requirement}"'] if requirement else []

    license_ = radiolist_dialog(
        values=sorted((zip(from_prefix(Prefix().license), from_prefix(Prefix().license)))),
        title='ozi-new interactive prompt',
        text=prefix + 'Please select a license classifier:',
        style=style,
        cancel_text='Skip',
    ).run()
    prefix += f'{Prefix().license}{license_}\n'
    output += [f'--license="{license_}"'] if license_ else []

    possible_spdx: Sequence[str] = METADATA.spec.python.pkg.license.ambiguous.get(
        license_,
        (),
    )
    if len(possible_spdx) < 1:
        license_expression = input_dialog(
            title='ozi-new interactive prompt',
            text=prefix + 'Edit SPDX license expression:',
            default='',
            style=style,
            cancel_text='Skip',
        ).run()
    elif len(possible_spdx) == 1:
        license_expression = input_dialog(
            title='ozi-new interactive prompt',
            text=prefix + 'Edit SPDX license expression:',
            default=possible_spdx[0],
            style=style,
            cancel_text='Skip',
        ).run()
    else:
        license_id = radiolist_dialog(
            values=sorted(zip(possible_spdx, possible_spdx)),
            title='ozi-new interactive prompt',
            text=prefix + 'Please select a SPDX license-id:',
            style=style,
            cancel_text='Skip',
        ).run()
        license_expression = input_dialog(
            title='ozi-new interactive prompt',
            text=prefix + 'Edit SPDX license expression:',
            default=license_id if license_id is not None else '',
            style=style,
            cancel_text='Skip',
        ).run()
    output += [f'--license-expression="{license_expression}"'] if license_expression else []
    prefix += f'Extra: License-Expression :: {license_expression}\n'

    if yes_no_dialog(
        title='ozi-new interactive prompt',
        text=prefix
        + 'Do you want to edit default classifiers?\n(audience, language, status, etc.)',
        style=style,
    ).run():
        for i in ['audience', 'environment', 'framework', 'language']:
            classifier = checkboxlist_dialog(
                values=sorted(
                    (
                        zip(
                            from_prefix(getattr(Prefix(), i)),
                            from_prefix(getattr(Prefix(), i)),
                        )
                    ),
                ),
                title='ozi-new interactive prompt',
                text=prefix + f'Please select {i} classifier or classifiers:',
                style=style,
                cancel_text='Skip',
            ).run()
            prefix += f'{getattr(Prefix(), i)}{classifier}\n'
            output += [f'--{i}="{classifier}"'] if classifier else []
        for i in ['topic', 'status']:
            classifier = radiolist_dialog(  # type: ignore
                values=sorted(
                    (
                        zip(
                            from_prefix(getattr(Prefix(), i)),
                            from_prefix(getattr(Prefix(), i)),
                        )
                    ),
                ),
                title='ozi-new interactive prompt',
                text=prefix + f'Please select {i} classifier or classifiers:',
                style=style,
                cancel_text='Skip',
            ).run()
            if classifier:
                prefix += f'{getattr(Prefix(), i)}{classifier}\n'
                output += [f'--{i}="{classifier}"'] if classifier else []
    if yes_no_dialog(
        title='ozi-new interactive prompt',
        text=prefix + 'Do you want to edit default options?\n(readme-type etc.)',
        style=style,
    ).run():
        readme_type = radiolist_dialog(
            values=(
                ('ReStructuredText', 'rst'),
                ('Markdown', 'md'),
                ('plain text', 'txt'),
            ),
            title='ozi-new interactive prompt',
            text=prefix + 'Please select README type:',
            style=style,
            cancel_text='Skip',
        ).run()
        output += [f'--readme-type="{readme_type}"'] if readme_type else []
    if yes_no_dialog(
        title='ozi-new interactive prompt',
        text=prefix + 'Confirm project creation?\n(answering "No" will exit the prompt)',
        style=style,
    ).run():
        return output
    else:
        return ['project']
