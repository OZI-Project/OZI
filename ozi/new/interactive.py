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
from typing import Any
from typing import Sequence
from typing import TypeVar

import requests
from prompt_toolkit import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.document import Document
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding import merge_key_bindings
from prompt_toolkit.key_binding.bindings.focus import focus_next
from prompt_toolkit.key_binding.bindings.focus import focus_previous
from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.layout import HSplit
from prompt_toolkit.layout import Layout
from prompt_toolkit.shortcuts import button_dialog
from prompt_toolkit.shortcuts import checkboxlist_dialog
from prompt_toolkit.shortcuts import input_dialog
from prompt_toolkit.shortcuts import message_dialog
from prompt_toolkit.shortcuts import radiolist_dialog
from prompt_toolkit.shortcuts import yes_no_dialog
from prompt_toolkit.styles import BaseStyle
from prompt_toolkit.styles import Style
from prompt_toolkit.validation import DynamicValidator
from prompt_toolkit.validation import ThreadedValidator
from prompt_toolkit.validation import ValidationError
from prompt_toolkit.validation import Validator
from prompt_toolkit.widgets import Button
from prompt_toolkit.widgets import Dialog
from prompt_toolkit.widgets import Label
from prompt_toolkit.widgets import RadioList

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


_style_dict = {
    'dialog': 'bg:#030711 fg:#030711',
    'dialog.body checkbox-list': '#e1e7ef',
    'dialog.body checkbox': '#e1e7ef',
    'dialog.body checkbox-selected': 'bg:#192334',
    'dialog.body checkbox-checked': '#e1e7ef',
    'dialog.body radio-list': '#e1e7ef',
    'dialog.body radio': '#e1e7ef',
    'dialog.body radio-selected': 'bg:#192334',
    'dialog.body radio-checked': '#e1e7ef',
    'button': '#e1e7ef',
    'dialog label': '#e1e7ef',
    'frame.border': '#192334',
    'dialog.body': 'bg:#030711',
    'dialog shadow': 'bg:#192334',
}

_style = Style.from_dict(_style_dict)

_T = TypeVar('_T')


class Admonition(RadioList[_T]):
    """Simple scrolling text dialog."""

    open_character = ''
    close_character = ''
    container_style = 'class:admonition-list'
    default_style = 'class:admonition'
    selected_style = 'class:admonition-selected'
    checked_style = 'class:admonition-checked'
    multiple_selection = False

    def __init__(
        self,  # noqa: ANN101
        values: Sequence[tuple[_T, Any]],
        default: _T | None = None,
    ) -> None:
        super().__init__(values, default)  # pragma: no cover

    def _handle_enter(self) -> None:  # noqa: ANN101
        pass  # pragma: no cover


def admonition_dialog(
    title: str = '',
    text: str = '',
    ok_text: str = '✔ Ok',
    cancel_text: str = '✘ Exit',
    style: BaseStyle | None = None,
) -> Application[list[Any]]:  # pragma: no cover
    """Admonition dialog shortcut.
    The focus can be moved between the list and the Ok/Cancel button with tab.
    """

    def _return_none() -> None:
        """Button handler that returns None."""
        get_app().exit()

    if style is None:
        style_dict = _style_dict
        style_dict.update(
            {
                'dialog.body admonition-list': '#e1e7ef',
                'dialog.body admonition': '#e1e7ef',
                'dialog.body admonition-selected': '#030711',
                'dialog.body admonition-checked': '#030711',
            },
        )
        style = Style.from_dict(style_dict)

    def ok_handler() -> None:
        get_app().exit(result=True)

    lines = text.splitlines()

    cb_list = Admonition(values=list(zip(lines, lines)), default=None)

    dialog = Dialog(
        title=title,
        body=HSplit(
            [Label(text='Disclaimer', dont_extend_height=True), cb_list],
            padding=1,
        ),
        buttons=[
            Button(text=ok_text, handler=ok_handler),
            Button(text=cancel_text, handler=_return_none),
        ],
        with_background=True,
        width=len(max(lines, key=len)) + 8,
    )
    bindings = KeyBindings()
    bindings.add('tab')(focus_next)
    bindings.add('s-tab')(focus_previous)

    return Application(
        layout=Layout(dialog),
        key_bindings=merge_key_bindings([load_key_bindings(), bindings]),
        mouse_support=True,
        style=style,
        full_screen=True,
    )


def validate_message(
    text: str,
    validator: Validator,
) -> tuple[bool, str]:  # pragma: no cover
    """Validate a string.

    :param text: string to validate
    :type text: str
    :param validator: validator instance
    :type validator: Validator
    :return: validation, error message
    :rtype: tuple[bool, str]
    """
    try:
        validator.validate(Document(text))
    except ValidationError as e:
        return False, e.message
    return True, ''


def classifier_checkboxlist(key: str) -> list[str] | None:  # pragma: no cover
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
        style=_style,
        ok_text='✔ Ok',
        cancel_text='← Back',
    ).run()


def header_input(
    label: str,
    output: list[str],
    prefix: dict[str, str],
    *args: str,
    validator: Validator | None = None,
    split_on: str | None = None,
) -> tuple[bool | None | list[str], list[str], dict[str, str]]:  # pragma: no cover
    header = input_dialog(
        title='ozi-new interactive prompt',
        text='\n'.join(('\n'.join(prefix.values()), '\n', *args)),
        validator=validator,
        style=_style,
        cancel_text='☰  Menu',
        ok_text='✔ Ok',
    ).run()
    if header is None:
        result, output, prefix = menu_loop(output, prefix)
        return result, output, prefix
    else:
        if validator is not None:
            valid, errmsg = validate_message(header, validator)
            if valid:
                prefix.update({label: f'{label}: {header}'})
                if split_on:
                    header = header.rstrip(split_on).split(split_on)  # type: ignore
                    output += [f'--author="{i}"' for i in header]
                else:
                    output += [f'--{label.lower()}="{header}"']
                return True, output, prefix
            message_dialog(
                title='ozi-new interactive prompt',
                text=f'Invalid input "{header}"\n{errmsg}\nPress ENTER to continue.',
                style=_style,
                ok_text='✔ Ok',
            ).run()
    return None, output, prefix


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
            style=_style,
        ).run():
            case True:
                break
            case False:
                if yes_no_dialog(
                    title='ozi-new interactive prompt',
                    text='Reset prompt and start over?',
                    style=_style,
                ).run():
                    return ['interactive', '.'], output, prefix
            case None:
                if yes_no_dialog(
                    title='ozi-new interactive prompt',
                    text='Exit the prompt?',
                    style=_style,
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
                        style=_style,
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
                                style=_style,
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
                            classifier = classifier_checkboxlist(x)
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

    if (
        admonition_dialog(
            title='ozi-new interactive prompt',
            text="""
The information provided on this prompt does not, and is not intended
to, constitute legal advice. All information, content, and materials
available on this prompt are for general informational purposes only.
Information on this prompt may not constitute the most up-to-date
legal or other information.

THE LICENSE TEMPLATES, LICENSE IDENTIFIERS, LICENSE CLASSIFIERS,
AND LICENSE EXPRESSION PARSING SERVICES, AND ALL OTHER CONTENTS ARE
PROVIDED "AS IS", NO REPRESENTATIONS ARE MADE THAT THE CONTENT IS
ERROR-FREE AND/OR APPLICABLE FOR ANY PURPOSE, INCLUDING MERCHANTABILITY.

Readers of this prompt should contact their attorney to obtain advice
with respect to any particular legal matter. The OZI Project is not a
law firm and does not provide legal advice. No reader or user of this
prompt should act or abstain from acting on the basis of information
on this prompt without first seeking legal advice from counsel in the
relevant jurisdiction. Legal counsel can ensure that the information
provided in this prompt is applicable to your particular situation.
Use of, or reading, this prompt or any of the resources contained
within does not create an attorney-client relationship.
""",
        ).run()
        is None
    ):
        return []

    prefix: dict[str, str] = {}
    output = ['project']
    while True:
        result, output, prefix = header_input(
            'Name',
            output,
            prefix,
            'What is the name of the project?',
            '(PyPI package name: no spaces, alphanumeric words, ".-_" as delimiters)',
            validator=DynamicValidator(check_package_exists),
        )
        if result is True:
            break
        if isinstance(result, list):
            return result

    while True:
        result, output, prefix = header_input(
            'Summary',
            output,
            prefix,
            'What does the project do?',
            '(a short summary 1-2 sentences)',
            validator=LengthValidator(),
        )
        if result is True:
            break
        if isinstance(result, list):
            return result

    while True:
        result, output, prefix = header_input(
            'Keywords',
            output,
            prefix,
            'What are some project keywords?\n(comma-separated list)',
            validator=LengthValidator(),
        )
        if result is True:
            break
        if isinstance(result, list):
            return result

    while True:
        result, output, prefix = header_input(
            'Home-page',
            output,
            prefix,
            "What is the project's home-page URL?",
            validator=LengthValidator(),
        )
        if result is True:
            break
        if isinstance(result, list):
            return result

    while True:
        result, output, prefix = header_input(
            'Author',
            output,
            prefix,
            'What is the author or authors name?\n(comma-separated list)',
            validator=LengthValidator(),
            split_on=',',
        )
        if result is True:
            break
        if isinstance(result, list):
            return result

    while True:
        result, output, prefix = header_input(
            'Author-email',
            output,
            prefix,
            'What are the email addresses of the author or authors?\n(comma-separated list)',
            validator=LengthValidator(),
            split_on=',',
        )
        if result is True:
            break
        if isinstance(result, list):
            return result

    while True:
        license_ = radiolist_dialog(
            values=sorted(
                (zip(from_prefix(Prefix().license), from_prefix(Prefix().license))),
            ),
            title='ozi-new interactive prompt',
            text='\n'.join(
                ('\n'.join(prefix.values()), '\n', 'Please select a license classifier:'),
            ),
            style=_style,
            cancel_text='☰  Menu',
            ok_text='✔ Ok',
        ).run()
        if license_ is None:
            result, output, prefix = menu_loop(output, prefix)
            if result is not None:
                return result
        else:
            if validate_message(license_ if license_ else '', LengthValidator())[0]:
                break
            message_dialog(
                style=_style,
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
                style=_style,
                cancel_text='Skip',
            ).run()
        elif len(possible_spdx) == 1:
            license_expression = input_dialog(
                title='ozi-new interactive prompt',
                text='\n'.join(
                    ('\n'.join(prefix.values()), '\n', 'Edit SPDX license expression:'),
                ),
                default=possible_spdx[0],
                style=_style,
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
                style=_style,
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
                    style=_style,
                    cancel_text='Skip',
                    ok_text='✔ Ok',
                ).run()
                if validate_message(license_id if license_id else '', LengthValidator())[0]:
                    break
                else:
                    message_dialog(
                        style=_style,
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
        style=_style,
    ).run():
        while True:
            result, output, prefix = header_input(
                'Maintainer',
                output,
                prefix,
                'What is the maintainer or maintainers name?\n(comma-separated list)',
                validator=LengthValidator(),
                split_on=',',
            )
            if result is True:
                break
            if isinstance(result, list):
                return result
        while True:
            result, output, prefix = header_input(
                'Maintainer-email',
                output,
                prefix,
                'What are the email addresses of the maintainer or maintainers?\n(comma-separated list)',  # noqa: B950, RUF100, E501
                validator=LengthValidator(),
                split_on=',',
            )
            if result is True:
                break
            if isinstance(result, list):
                return result

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
        style=_style,
    ).run():
        requirement = input_dialog(
            title='ozi-new interactive prompt',
            text='\n'.join(('\n'.join(prefix.values()), '\n', 'Search PyPI packages:')),
            validator=PackageValidator(),
            style=_style,
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
        style=_style,
    ).run():
        result, output, prefix = menu_loop(output, prefix)
        if result is not None:
            return result

    return output
