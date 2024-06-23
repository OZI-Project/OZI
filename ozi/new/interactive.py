"""
``ozi-new`` interactive prompts
"""

from __future__ import annotations

import curses
import os
import re
import sys
from functools import lru_cache
from typing import TYPE_CHECKING
from typing import Sequence

import requests
from prompt_toolkit.document import Document
from prompt_toolkit.shortcuts import button_dialog
from prompt_toolkit.shortcuts import checkboxlist_dialog
from prompt_toolkit.shortcuts import input_dialog
from prompt_toolkit.shortcuts import message_dialog
from prompt_toolkit.shortcuts import radiolist_dialog
from prompt_toolkit.shortcuts import yes_no_dialog
from prompt_toolkit.styles import Style
from prompt_toolkit.validation import DynamicValidator
from prompt_toolkit.validation import ThreadedValidator
from prompt_toolkit.validation import ValidationError
from prompt_toolkit.validation import Validator

from ozi.spec import METADATA
from ozi.trove import Prefix
from ozi.trove import from_prefix

if TYPE_CHECKING:
    from argparse import Namespace


@lru_cache
def pypi_package_exists(package: str) -> bool:  # pragma: no cover
    return (
        requests.get(
            f'https://pypi.org/simple/{package}',
            timeout=15,
        ).status_code
        == 200
    )


class ProjectNameValidator(Validator):
    def validate(self, document: Document) -> None:  # pragma: no cover  # noqa: ANN101
        if len(document.text) == 0:
            raise ValidationError(0, 'cannot be empty')
        if not re.match(
            '^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$',
            document.text,
            flags=re.IGNORECASE,
        ):
            raise ValidationError(len(document.text), 'invalid project name')


class NotReservedValidator(ThreadedValidator):
    def validate(self, document: Document) -> None:  # pragma: no cover  # noqa: ANN101
        self.validator.validate(document)
        if pypi_package_exists(document.text):
            raise ValidationError(len(document.text), 'project with that name exists')


class LengthValidator(Validator):
    def validate(self, document: Document) -> None:  # pragma: no cover  # noqa: ANN101
        if len(document.text) == 0:
            raise ValidationError(0, 'must not be empty')
        if len(document.text) > 512:
            raise ValidationError(512, 'input is too long')


class PackageValidator(Validator):
    def validate(self, document: Document) -> None:  # pragma: no cover  # noqa: ANN101
        if len(document.text) == 0:
            raise ValidationError(0, 'cannot be empty')
        if pypi_package_exists(document.text):
            pass
        else:
            raise ValidationError(len(document.text), 'package not found')


style = Style.from_dict(
    {
        'dialog': 'bg:#030711 fg:#030711',
        'dialog.body checkbox-list': '#e1e7ef',
        'dialog.body checkbox': '#e1e7ef',
        'dialog.body checkbox-selected': '#e1e7ef',
        'dialog.body checkbox-checked': '#e1e7ef',
        'dialog.body radio-list': '#e1e7ef',
        'dialog.body radio': '#e1e7ef',
        'dialog.body radio-selected': '#e1e7ef',
        'dialog.body radio-checked': '#e1e7ef',
        'button': '#e1e7ef',
        'dialog label': '#e1e7ef',
        'frame.border': '#192334',
        'dialog.body': 'bg:#030711',
        'dialog shadow': 'bg:#192334',
    },
)


def validate_message(text: str, validator: Validator) -> bool:  # pragma: no cover
    """Validate a string.

    :param text: string to validate
    :type text: str
    :param validator: validator instance
    :type validator: Validator
    :return: False if invalid
    :rtype: bool
    """
    try:
        validator.validate(Document(text))
    except ValidationError:
        return False
    return True


def classifier_radiolist(key: str) -> list[str] | None:  # pragma: no cover
    return checkboxlist_dialog(
        values=sorted(
            (
                zip(
                    from_prefix(getattr(Prefix(), key)),
                    from_prefix(getattr(Prefix(), key)),
                )
            ),
        ),
        title='ozi-new interactive prompt',
        text=f'Please select {key} classifier or classifiers:',
        style=style,
        ok_text='✔ Ok',
        cancel_text='← Back',
    ).run()


def menu_loop(
    output: list[str],
    prefix: dict[str, str],
) -> tuple[None | list[str], list[str], dict[str, str]]:  # pragma: no cover
    while True:
        match button_dialog(
            title='ozi-new interactive prompt',
            text='\n'.join(
                ('\n'.join(prefix.values()), '\n', 'Main menu, select an action:'),
            ),
            buttons=[
                ('⚙ Options', 0),
                ('↺ Reset', False),
                ('✘ Exit', None),
                ('← Back', True),
            ],
            style=style,
        ).run():
            case True:
                break
            case False:
                if yes_no_dialog(
                    title='ozi-new interactive prompt',
                    text='Reset prompt and start over?',
                    style=style,
                ).run():
                    return ['interactive', '.'], output, prefix
            case None:
                if yes_no_dialog(
                    title='ozi-new interactive prompt',
                    text='Exit the prompt?',
                    style=style,
                ).run():
                    return [], output, prefix
            case 0:
                while True:
                    match button_dialog(
                        title='ozi-new interactive prompt',
                        text='\n'.join(
                            (
                                '\n'.join(prefix.values()),
                                '\n',
                                'Options menu, select an option:',
                            ),
                        ),
                        buttons=[
                            ('Audience', 'audience'),
                            ('Environ.', 'environment'),
                            ('Framework', 'framework'),
                            ('Language', 'language'),
                            ('README', 0),
                            ('← Back', True),
                        ],
                        style=style,
                    ).run():
                        case True:
                            break
                        case 0:
                            readme_type = radiolist_dialog(
                                values=(
                                    ('rst', 'ReStructuredText'),
                                    ('md', 'Markdown'),
                                    ('txt', 'Plaintext'),
                                ),
                                title='ozi-new interactive prompt',
                                text='\n'.join(
                                    (
                                        '\n'.join(prefix.values()),
                                        '\n',
                                        'Please select README type:',
                                    ),
                                ),
                                style=style,
                                ok_text='✔ Ok',
                                cancel_text='← Back',
                            ).run()
                            output += (
                                [f'--readme-type="{readme_type}"'] if readme_type else []
                            )
                            prefix.update(
                                (
                                    {
                                        'Description-Content-Type:': f'Description-Content-Type: {readme_type}',  # noqa: B950, RUF100, E501
                                    }
                                    if readme_type
                                    else {}
                                ),
                            )
                        case x if x and isinstance(x, str):
                            classifier = classifier_radiolist(x)
                            output += [f'--{x}="{classifier}"'] if classifier else []
                            prefix.update(
                                (
                                    {
                                        f'{getattr(Prefix(), x)}': f'{getattr(Prefix(), x)}{classifier}',  # noqa: B950, RUF100, E501
                                    }
                                    if classifier
                                    else {}
                                ),
                            )
    return None, output, prefix


def interactive_prompt(project: Namespace) -> list[str]:  # noqa: C901  # pragma: no cover
    curses.setupterm()
    e3 = curses.tigetstr('E3') or b''
    clear_screen_seq = curses.tigetstr('clear') or b''
    os.write(sys.stdout.fileno(), e3 + clear_screen_seq)

    def check_package_exists() -> Validator:
        nonlocal project
        if project.check_package_exists:
            return NotReservedValidator(ProjectNameValidator())
        else:
            return ProjectNameValidator()

    prefix: dict[str, str] = {}
    output = ['project']
    while True:
        project_name = input_dialog(
            title='ozi-new interactive prompt',
            text='\n'.join(
                (
                    '\n'.join(prefix.values()),
                    '\n',
                    'What is the name of the project?',
                    '(PyPI package name: no spaces, alphanumeric words, ".-_" as delimiters)',
                ),
            ),
            validator=DynamicValidator(check_package_exists),
            style=style,
            cancel_text='☰  Menu',
            ok_text='✔ Ok',
        ).run()
        if project_name is None:
            result, output, prefix = menu_loop(output, prefix)
            if result is not None:
                return result
        else:
            if validate_message(project_name, DynamicValidator(check_package_exists)):
                break
            message_dialog(
                title='ozi-new interactive prompt',
                text=f'Invalid input "{project_name}"\nPress ENTER to continue.',
                style=style,
                ok_text='✔ Ok',
            ).run()
    prefix.update({'Name:': f'Name: {project_name if project_name else ""}'})
    output += [f'--name="{project_name}"'] if project_name else []

    while True:
        summary = input_dialog(
            title='ozi-new interactive prompt',
            text='\n'.join(
                (
                    '\n'.join(prefix.values()),
                    '\n',
                    'What does the project do?',
                    '(a short summary 1-2 sentences)',
                ),
            ),
            validator=LengthValidator(),
            style=style,
            cancel_text='☰  Menu',
            ok_text='✔ Ok',
        ).run()
        if summary is None:
            result, output, prefix = menu_loop(output, prefix)
            if result is not None:
                return result
        else:
            if validate_message(summary, LengthValidator()):
                break
            message_dialog(
                style=style,
                title='ozi-new interactive prompt',
                text=f'Invalid input "{summary}"\nPress ENTER to continue.',
                ok_text='✔ Ok',
            ).run()
    prefix.update({'Summary:': f'Summary: {summary if summary else ""}'})
    output += [f'--summary="{summary if summary else ""}"']

    while True:
        keywords = input_dialog(
            title='ozi-new interactive prompt',
            text='\n'.join(
                (
                    '\n'.join(prefix.values()),
                    '\n',
                    'What are some project keywords?\n(comma-separated list)',
                ),
            ),
            style=style,
            cancel_text='☰  Menu',
        ).run()
        if keywords is None:
            result, output, prefix = menu_loop(output, prefix)
            if result is not None:
                return result
        else:
            keywords = keywords.rstrip(',').split(',') if keywords else None  # type: ignore
            if validate_message(','.join(keywords) if keywords else '', LengthValidator()):
                break
            message_dialog(
                style=style,
                title='ozi-new interactive prompt',
                text=f'Invalid input "{keywords}"\nPress ENTER to continue.',
                ok_text='✔ Ok',
            ).run()
    prefix.update({'Keywords:': f'Keywords: {",".join(keywords if keywords else "")}'})
    output += [f'--keywords={",".join(keywords if keywords else [])}']

    while True:
        home_page = input_dialog(
            title='ozi-new interactive prompt',
            text='\n'.join(
                ('\n'.join(prefix.values()), '\n', "What is the project's home-page URL?"),
            ),
            style=style,
            cancel_text='☰  Menu',
            ok_text='✔ Ok',
        ).run()
        if home_page is None:
            result, output, prefix = menu_loop(output, prefix)
            if result is not None:
                return result
        else:
            if validate_message(home_page, LengthValidator()):
                break
            message_dialog(
                style=style,
                title='ozi-new interactive prompt',
                text=f'Invalid input "{home_page}"\nPress ENTER to continue.',
                ok_text='✔ Ok',
            ).run()
    prefix.update({'Home-page:': f'Home-page: {home_page if home_page else ""}'})
    output += [f'--home-page="{home_page}"'] if home_page else []

    while True:
        author_names = input_dialog(
            title='ozi-new interactive prompt',
            text='\n'.join(
                (
                    '\n'.join(prefix.values()),
                    '\n',
                    'What is the author or authors name?\n(comma-separated list)',
                ),
            ),
            style=style,
            cancel_text='☰  Menu',
            ok_text='✔ Ok',
        ).run()
        if author_names is None:
            result, output, prefix = menu_loop(output, prefix)
            if result is not None:
                return result
        else:
            author_names = author_names.rstrip(',').split(',') if author_names else None  # type: ignore
            if validate_message(
                (','.join(author_names) if author_names else ''),
                LengthValidator(),
            ):
                break
            message_dialog(
                title='ozi-new interactive prompt',
                text=f'Invalid input "{author_names}"\nPress ENTER to continue.',
                style=style,
                ok_text='✔ Ok',
            ).run()
    prefix.update({'Author:': f'Author: {",".join(author_names if author_names else "")}'})
    output += [f'--author="{a}"' for a in author_names] if author_names else []

    while True:
        author_emails = input_dialog(
            title='ozi-new interactive prompt',
            text='\n'.join(
                (
                    '\n'.join(prefix.values()),
                    '\n',
                    'What are the email addresses of the author or authors?\n(comma-separated list)',
                ),
            ),
            style=style,
            cancel_text='☰  Menu',
            ok_text='✔ Ok',
        ).run()
        if author_emails is None:
            result, output, prefix = menu_loop(output, prefix)
            if result is not None:
                return result
        else:
            author_emails = author_emails.rstrip(',').split(',') if author_emails else None  # type: ignore
            if validate_message(
                ','.join(author_emails) if author_emails else '',
                LengthValidator(),
            ):
                break
            message_dialog(
                style=style,
                title='ozi-new interactive prompt',
                text=f'Invalid input "{author_emails}"\nPress ENTER to continue.',
                ok_text='✔ Ok',
            ).run()
    prefix.update(
        {
            'Author-email:': f'Author-email: {",".join(author_emails if author_emails else "")}',
        },
    )
    output += [f'--author-email="{e}"' for e in author_emails] if author_emails else []

    while True:
        license_ = radiolist_dialog(
            values=sorted(
                (zip(from_prefix(Prefix().license), from_prefix(Prefix().license))),
            ),
            title='ozi-new interactive prompt',
            text='\n'.join(
                ('\n'.join(prefix.values()), '\n', 'Please select a license classifier:'),
            ),
            style=style,
            cancel_text='☰  Menu',
            ok_text='✔ Ok',
        ).run()
        if license_ is None:
            result, output, prefix = menu_loop(output, prefix)
            if result is not None:
                return result
        else:
            if validate_message(license_ if license_ else '', LengthValidator()):
                break
            message_dialog(
                style=style,
                title='ozi-new interactive prompt',
                text=f'Invalid input "{license_}"\nPress ENTER to continue.',
                ok_text='✔ Ok',
            ).run()
    prefix.update(
        {f'{Prefix().license}': f'{Prefix().license}{license_ if license_ else ""}'},
    )
    output += [f'--license="{license_}"'] if license_ else []

    while True:
        possible_spdx: Sequence[str] = METADATA.spec.python.pkg.license.ambiguous.get(
            license_,
            (),
        )
        if len(possible_spdx) < 1:
            license_expression = input_dialog(
                title='ozi-new interactive prompt',
                text='\n'.join(
                    ('\n'.join(prefix.values()), '\n', 'Edit SPDX license expression:'),
                ),
                default='',
                style=style,
                cancel_text='Skip',
            ).run()
        elif len(possible_spdx) == 1:
            license_expression = input_dialog(
                title='ozi-new interactive prompt',
                text='\n'.join(
                    ('\n'.join(prefix.values()), '\n', 'Edit SPDX license expression:'),
                ),
                default=possible_spdx[0],
                style=style,
                cancel_text='Skip',
                ok_text='✔ Ok',
            ).run()
        else:
            license_id = radiolist_dialog(
                values=sorted(zip(possible_spdx, possible_spdx)),
                title='ozi-new interactive prompt',
                text='\n'.join(
                    ('\n'.join(prefix.values()), '\n', 'Please select a SPDX license-id:'),
                ),
                style=style,
                cancel_text='☰  Menu',
                ok_text='✔ Ok',
            ).run()
            if license_id is None:
                result, output, prefix = menu_loop(output, prefix)
                if result is not None:
                    return result
            else:
                license_expression = input_dialog(
                    title='ozi-new interactive prompt',
                    text='\n'.join(
                        ('\n'.join(prefix.values()), '\n', 'Edit SPDX license expression:'),
                    ),
                    default=license_id if license_id is not None else '',
                    style=style,
                    cancel_text='Skip',
                    ok_text='✔ Ok',
                ).run()
                if validate_message(license_id if license_id else '', LengthValidator()):
                    break
                else:
                    message_dialog(
                        style=style,
                        title='ozi-new interactive prompt',
                        text=f'Invalid input "{license_id}"\nPress ENTER to continue.',
                        ok_text='✔ Ok',
                    ).run()
        break

    output += (
        [f'--license-expression="{license_expression}"']
        if license_expression  # pyright: ignore
        else []
    )
    prefix.update(
        {
            'Extra: License-Expression ::': f'Extra: License-Expression :: {license_expression if license_expression else ""}',  # pyright: ignore  # noqa: B950, RUF100, E501
        },
    )  # pyright: ignore  # noqa: B950, RUF100

    if yes_no_dialog(
        title='ozi-new interactive prompt',
        text='\n'.join(
            (
                '\n'.join(prefix.values()),
                '\n',
                'Are there any maintainers of this project?\n(other than the author or authors)',
            ),
        ),
        style=style,
    ).run():
        while True:
            maintainer_names = input_dialog(
                title='ozi-new interactive prompt',
                text='\n'.join(
                    (
                        '\n'.join(prefix.values()),
                        '\n',
                        'What is the maintainer or maintainers name?\n(comma-separated list)',
                    ),
                ),
                style=style,
                cancel_text='☰  Menu',
                ok_text='✔ Ok',
            ).run()
            if maintainer_names is None:
                result, output, prefix = menu_loop(output, prefix)
                if result is not None:
                    return result
            else:
                maintainer_names = (
                    maintainer_names.rstrip(',').split(',') if maintainer_names else None  # type: ignore
                )
                if validate_message(
                    ','.join(maintainer_names) if maintainer_names else '',
                    LengthValidator(),
                ):
                    break
                message_dialog(
                    style=style,
                    title='ozi-new interactive prompt',
                    text=f'Invalid input "{maintainer_names}"\nPress ENTER to continue.',
                    ok_text='✔ Ok',
                ).run()
        prefix.update(
            {
                'Maintainer:': f'Maintainer: {",".join(maintainer_names if maintainer_names else [])}',  # noqa: B950, RUF100, E501
            },
        )
        output += (
            [f'--maintainer="{a}"' for a in maintainer_names] if maintainer_names else []
        )

        while True:
            maintainer_emails = input_dialog(
                title='ozi-new interactive prompt',
                text='\n'.join(
                    (
                        '\n'.join(prefix.values()),
                        '\n',
                        'What are the email addresses of the maintainer or maintainers?\n(comma-separated list)',  # noqa: B950, RUF100, E501
                    ),
                ),
                style=style,
                cancel_text='☰  Menu',
                ok_text='✔ Ok',
            ).run()
            if maintainer_emails is None:
                result, output, prefix = menu_loop(output, prefix)
                if result is not None:
                    return result
            else:
                maintainer_emails = (
                    maintainer_emails.rstrip(',').split(',') if maintainer_emails else None  # type: ignore
                )
                if validate_message(
                    ','.join(maintainer_emails) if maintainer_emails else '',
                    LengthValidator(),
                ):
                    break
                message_dialog(
                    style=style,
                    title='ozi-new interactive prompt',
                    text=f'Invalid input "{maintainer_emails}"\nPress ENTER to continue.',
                    ok_text='✔ Ok',
                ).run()
        prefix.update(
            {
                'Maintainer-email:': f'Maintainer-email: {",".join(maintainer_emails if maintainer_emails else [])}\n',  # noqa: B950, RUF100, E501
            },
        )
        output += (
            [f'--maintainer-email="{e}"' for e in maintainer_emails]
            if maintainer_emails
            else []
        )

    requires_dist = []
    while button_dialog(
        title='ozi-new interactive prompt',
        text='\n'.join(
            (
                '\n'.join(prefix.values()),
                '\n',
                'Do you want to add a dependency requirement?',
            ),
        ),
        buttons=[
            ('Yes', True),
            ('No', False),
        ],
        style=style,
    ).run():
        requirement = input_dialog(
            title='ozi-new interactive prompt',
            text='\n'.join(('\n'.join(prefix.values()), '\n', 'Search PyPI packages:')),
            validator=PackageValidator(),
            style=style,
            cancel_text='← Back',
        ).run()
        requires_dist += [requirement] if requirement else []
        prefix.update(
            {
                f'Requires-Dist: {requirement}': (
                    f'Requires-Dist: {requirement}\n' if requirement else ''
                ),
            },
        )
        output += [f'--requires-dist="{requirement}"'] if requirement else []

    while not yes_no_dialog(
        title='ozi-new interactive prompt',
        text='\n'.join(
            (
                '\n'.join(prefix.values()),
                '\n',
                'Confirm project creation?',
            ),
        ),
        yes_text='✔ Ok',
        no_text='☰  Menu',
        style=style,
    ).run():
        result, output, prefix = menu_loop(output, prefix)
        if result is not None:
            return result

    return output
