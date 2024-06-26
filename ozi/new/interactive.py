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
from prompt_toolkit.filters import Condition
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding import merge_key_bindings
from prompt_toolkit.key_binding.bindings.focus import focus_next
from prompt_toolkit.key_binding.bindings.focus import focus_previous
from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.layout import ConditionalMargin
from prompt_toolkit.layout import HSplit
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout import ScrollbarMargin
from prompt_toolkit.layout import Window
from prompt_toolkit.layout.controls import FormattedTextControl
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

    from prompt_toolkit.key_binding.key_processor import KeyPressEvent


class Project:  # pragma: no cover
    @staticmethod
    def name(
        output: list[str],
        prefix: dict[str, str],
        check_package_exists: bool = True,
    ) -> tuple[None | list[str] | str | bool, list[str], dict[str, str]]:

        def _check_package_exists() -> Validator:
            if check_package_exists:
                return NotReservedValidator(ProjectNameValidator())
            else:
                return ProjectNameValidator()

        while True:
            result, output, prefix = header_input(
                'Name',
                output,
                prefix,
                'What is the name of the project?',
                '(PyPI package name: no spaces, alphanumeric words, ".-_" as delimiters)',
                validator=DynamicValidator(_check_package_exists),
            )
            if result is True:
                return prefix.get('Name', '').replace('Name', '').strip(': '), output, prefix
            if isinstance(result, list):
                return result, output, prefix

    @staticmethod
    def summary(
        project_name: str,
        output: list[str],
        prefix: dict[str, str],
    ) -> tuple[None | list[str] | str | bool, list[str], dict[str, str]]:
        while True:
            result, output, prefix = header_input(
                'Summary',
                output,
                prefix,
                f'What does the project, {project_name}, do?',
                '(a short summary 1-2 sentences)',
                validator=LengthValidator(),
            )
            if result is True:
                return result, output, prefix
            if isinstance(result, list):
                return result, output, prefix

    @staticmethod
    def keywords(
        project_name: str,
        output: list[str],
        prefix: dict[str, str],
    ) -> tuple[None | list[str] | str | bool, list[str], dict[str, str]]:
        while True:
            result, output, prefix = header_input(
                'Keywords',
                output,
                prefix,
                f'What are some keywords used to describe {project_name}?\n(comma-separated list)',
                validator=LengthValidator(),
            )
            if result is True:
                return result, output, prefix
            if isinstance(result, list):
                return result, output, prefix

    @staticmethod
    def home_page(
        project_name: str,
        output: list[str],
        prefix: dict[str, str],
    ) -> tuple[None | list[str] | str | bool, list[str], dict[str, str]]:
        while True:
            result, output, prefix = header_input(
                'Home-page',
                output,
                prefix,
                f'What is the home-page URL for {project_name}?',
                validator=LengthValidator(),
            )
            if result is True:
                return result, output, prefix
            if isinstance(result, list):
                return result, output, prefix

    @staticmethod
    def author(
        project_name: str,
        output: list[str],
        prefix: dict[str, str],
    ) -> tuple[None | list[str] | str | bool, list[str], dict[str, str]]:
        while True:
            result, output, prefix = header_input(
                'Author',
                output,
                prefix,
                f'Who is the author or authors of {project_name}?\n(comma-separated list)',
                validator=LengthValidator(),
                split_on=',',
            )
            if result is True:
                return result, output, prefix
            if isinstance(result, list):
                return result, output, prefix

    @staticmethod
    def author_email(
        project_name: str,
        output: list[str],
        prefix: dict[str, str],
    ) -> tuple[None | list[str] | str | bool, list[str], dict[str, str]]:
        while True:
            result, output, prefix = header_input(
                'Author-email',
                output,
                prefix,
                f'What are the email addresses of the author or authors of {project_name}?\n(comma-separated list)',  # noqa: B950, RUF100, E501
                validator=LengthValidator(),
                split_on=',',
            )
            if result is True:
                return result, output, prefix
            if isinstance(result, list):
                return result, output, prefix

    @staticmethod
    def license_(
        project_name: str,
        output: list[str],
        prefix: dict[str, str],
    ) -> tuple[None | list[str] | str, list[str], dict[str, str]]:
        while True:
            license_ = radiolist_dialog(
                values=sorted(
                    (zip(from_prefix(Prefix().license), from_prefix(Prefix().license))),
                ),
                title='ozi-new interactive prompt',
                text=f'Please select a license classifier for {project_name}:',
                style=_style,
                cancel_text='☰  Menu',
                ok_text='✔ Ok',
            ).run()
            if license_ is None:
                result, output, prefix = menu_loop(output, prefix)
                if isinstance(result, list):
                    return result, output, prefix
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
        return license_, output, prefix

    @staticmethod
    def license_expression(  # noqa: C901
        project_name: str,
        _license: str,
        output: list[str],
        prefix: dict[str, str],
    ) -> tuple[None | list[str] | str, list[str], dict[str, str]]:
        _license_expression: str = ''
        while True:
            possible_spdx: Sequence[str] = METADATA.spec.python.pkg.license.ambiguous.get(
                _license,
                (),
            )
            if len(possible_spdx) < 1:
                _license_expression = input_dialog(
                    title='ozi-new interactive prompt',
                    text=f'License: {_license}\nEdit SPDX license expression for {project_name}:',
                    default='',
                    style=_style,
                    cancel_text='Skip',
                ).run()
            elif len(possible_spdx) == 1:
                _license_expression = input_dialog(
                    title='ozi-new interactive prompt',
                    text=f'License: {_license}\nEdit SPDX license expression for {project_name}:',
                    default=possible_spdx[0],
                    style=_style,
                    cancel_text='Skip',
                    ok_text='✔ Ok',
                ).run()
            else:
                license_id = radiolist_dialog(
                    values=sorted(zip(possible_spdx, possible_spdx)),
                    title='ozi-new interactive prompt',
                    text=f'License: {_license}\nPlease select a SPDX license-id for {project_name}:',
                    style=_style,
                    cancel_text='☰  Menu',
                    ok_text='✔ Ok',
                ).run()
                if license_id is None:
                    result, output, prefix = menu_loop(output, prefix)
                    if isinstance(result, list):
                        return result, output, prefix
                else:
                    _license_expression = input_dialog(
                        title='ozi-new interactive prompt',
                        text=f'License: {_license}\nEdit SPDX license expression for {project_name}:',
                        default=license_id if license_id is not None else '',
                        style=_style,
                        cancel_text='Skip',
                        ok_text='✔ Ok',
                    ).run()
                    if validate_message(license_id if license_id else '', LengthValidator())[
                        0
                    ]:
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
            [f'--license-expression="{_license_expression}"']
            if _license_expression  # pyright: ignore
            else []
        )
        prefix.update(
            {
                'Extra: License-Expression ::': f'Extra: License-Expression :: {_license_expression if _license_expression else ""}',  # pyright: ignore  # noqa: B950, RUF100, E501
            },
        )  # pyright: ignore  # noqa: B950, RUF100
        return _license_expression, output, prefix

    @staticmethod
    def maintainer(
        project_name: str,
        output: list[str],
        prefix: dict[str, str],
    ) -> tuple[None | list[str] | str | bool, list[str], dict[str, str]]:
        while True:
            result, output, prefix = header_input(
                'Maintainer',
                output,
                prefix,
                f'What is the maintainer or maintainers name of {project_name}?\n(comma-separated list)',  # noqa: B950, RUF100, E501
                validator=LengthValidator(),
                split_on=',',
            )
            if result is True:
                return result, output, prefix
            if isinstance(result, list):
                return result, output, prefix

    @staticmethod
    def maintainer_email(
        project_name: str,
        output: list[str],
        prefix: dict[str, str],
    ) -> tuple[None | list[str] | str | bool, list[str], dict[str, str]]:
        while True:
            result, output, prefix = header_input(
                'Maintainer-email',
                output,
                prefix,
                f'What are the email addresses of the maintainer or maintainers of {project_name}?\n(comma-separated list)',  # noqa: B950, RUF100, E501
                validator=LengthValidator(),
                split_on=',',
            )
            if result is True:
                return result, output, prefix
            if isinstance(result, list):
                return result, output, prefix

    @staticmethod
    def requires_dist(
        project_name: str,
        output: list[str],
        prefix: dict[str, str],
    ) -> tuple[list[str] | str | bool | None, list[str], dict[str, str]]:
        _requires_dist: list[str] = []
        while True:
            match button_dialog(
                title='ozi-new interactive prompt',
                text='\n'.join(
                    (
                        'Requires-Dist:',
                        '\n'.join(_requires_dist),
                        '\n',
                        f'Add or remove dependency requirements to {project_name}:',
                    ),
                ),
                buttons=[
                    ('Add', True),
                    ('Remove', False),
                    ('✔ Ok', 'ok'),
                    ('☰  Menu', None),
                ],
                style=_style,
            ).run():
                case True:
                    requirement = input_dialog(
                        title='ozi-new interactive prompt',
                        text='Search PyPI packages:',
                        validator=PackageValidator(),
                        style=_style,
                        cancel_text='← Back',
                    ).run()
                    if requirement:
                        _requires_dist += [requirement] if requirement else []
                        prefix.update(
                            {
                                f'Requires-Dist: {requirement}': (
                                    f'Requires-Dist: {requirement}\n' if requirement else ''
                                ),
                            },
                        )
                        output += [f'--requires-dist="{requirement}"'] if requirement else []
                case False:
                    if len(_requires_dist) != 0:
                        del_requirement = checkboxlist_dialog(
                            title='ozi-new interactive prompt',
                            text='Select packages to delete:',
                            values=list(zip(_requires_dist, _requires_dist)),
                            style=_style,
                            cancel_text='← Back',
                        ).run()
                        if del_requirement:
                            _requires_dist = list(
                                set(_requires_dist).symmetric_difference(
                                    set(del_requirement),
                                ),
                            )
                            output = list(
                                set(output).symmetric_difference(
                                    {f'--requires-dist="{del_requirement}"'},
                                ),
                            )
                            for req in del_requirement:
                                prefix.pop(f'Requires-Dist: {req}')
                    else:
                        message_dialog(
                            title='ozi-new interactive prompt',
                            text='No requirements to remove.',
                            style=_style,
                        ).run()
                case x if x and x == 'ok':
                    break
                case None:
                    result, output, prefix = menu_loop(output, prefix)
                    if result is not None:
                        return result, output, prefix
        return None, output, prefix

    @staticmethod
    def readme_type(
        project_name: str,
        output: list[str],
        prefix: dict[str, str],
    ) -> tuple[str, list[str], dict[str, str]]:
        readme_type = radiolist_dialog(
            values=(
                ('rst', 'ReStructuredText'),
                ('md', 'Markdown'),
                ('txt', 'Plaintext'),
            ),
            title='ozi-new interactive prompt',
            text=f'Please select README type for {project_name}:',
            style=_style,
            ok_text='✔ Ok',
            cancel_text='← Back',
        ).run()
        output += [f'--readme-type="{readme_type}"'] if readme_type else []
        prefix.update(
            (
                {
                    'Description-Content-Type:': f'Description-Content-Type: {readme_type}',  # noqa: B950, RUF100, E501
                }
                if readme_type
                else {}
            ),
        )
        return readme_type, output, prefix


_P = Project()


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

    def __init__(  # noqa: C901
        self,  # noqa: ANN101
        values: Sequence[tuple[_T, Any]],
        default: _T | None = None,
    ) -> None:  # pragma: no cover
        super().__init__(values, default)
        # Key bindings.
        kb = KeyBindings()

        @kb.add('pageup')
        def _pageup(event: KeyPressEvent) -> None:
            w = event.app.layout.current_window
            if w.render_info:
                self._selected_index = max(
                    0,
                    self._selected_index - len(w.render_info.displayed_lines),
                )

        @kb.add('pagedown')
        def _pagedown(event: KeyPressEvent) -> None:
            w = event.app.layout.current_window
            if w.render_info:
                self._selected_index = min(
                    len(self.values) - 1,
                    self._selected_index + len(w.render_info.displayed_lines),
                )

        @kb.add('up')
        def _up(event: KeyPressEvent) -> None:
            _pageup(event)

        @kb.add('down')
        def _down(event: KeyPressEvent) -> None:
            _pagedown(event)

        @kb.add('enter')
        @kb.add(' ')
        def _click(event: KeyPressEvent) -> None:
            self._handle_enter()

        self.control = FormattedTextControl(
            self._get_text_fragments,
            key_bindings=kb,
            focusable=True,
        )

        self.window = Window(
            content=self.control,
            style=self.container_style,
            right_margins=[
                ConditionalMargin(
                    margin=ScrollbarMargin(display_arrows=True),
                    filter=Condition(lambda: self.show_scrollbar),
                ),
            ],
            dont_extend_height=True,
        )

    def _handle_enter(self) -> None:  # noqa: ANN101
        pass  # pragma: no cover


def admonition_dialog(
    title: str = '',
    text: str = '',
    heading_label: str = '',
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
    longest_line = len(max(lines, key=len))
    dialog = Dialog(
        title=title,
        body=HSplit(
            [Label(text=heading_label, dont_extend_height=True), cb_list],
            padding=1,
        ),
        buttons=[
            Button(text=ok_text, handler=ok_handler),
            Button(text=cancel_text, handler=_return_none),
        ],
        with_background=True,
        width=longest_line + 8 if longest_line > 40 else 80,
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
        text='\n'.join(args),
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
                    output += [f'--{label.lower()}="{i}"' for i in header]
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
) -> tuple[None | list[str] | bool, list[str], dict[str, str]]:  # pragma: no cover
    while True:
        match button_dialog(
            title='ozi-new interactive prompt',
            text='Main menu, select an action:',
            buttons=[
                ('∋ Metadata', 1),
                ('⚙ Options', 0),
                ('↺ Reset', False),
                ('✘ Exit', None),
                ('✎ Edit', -1),
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
            case -1:
                while True:
                    match radiolist_dialog(
                        title='ozi-new interactive prompt',
                        text='Edit menu, select content to edit:',
                        values=[
                            ('name', 'Name'),
                            ('summary', 'Summary'),
                            ('keywords', 'Keywords'),
                            ('home_page', 'Home-page'),
                            ('author', 'Author'),
                            ('author_email', 'Email'),
                            ('license_', 'License'),
                            ('license_expression', 'Extra: License-Expression'),
                            ('maintainer', 'Maintainer'),
                            ('maintainer_email', 'Maintainer-email'),
                            ('requires_dist', 'Requires-Dist (requirements)'),
                            ('audience', 'Intended Audience'),
                            ('environment', 'Environment'),
                            ('framework', 'Framework'),
                            ('language', 'Natural Language'),
                            ('status', 'Status'),
                            ('topic', 'Topic'),
                            ('readme_type', 'Description-Content-Type'),
                        ],
                        cancel_text='← Back',
                        ok_text='✔ Ok',
                        style=_style,
                    ).run():
                        case None:
                            break
                        case x if x and isinstance(x, str):
                            project_name = (
                                prefix.get('Name', '').replace('Name', '').strip(': ')
                            )
                            match x:
                                case x if x == 'name':
                                    result, output, prefix = _P.name(output, prefix)
                                    if isinstance(result, list):
                                        return result, output, prefix
                                case x if x == 'license_expression':
                                    result, output, prefix = _P.license_expression(
                                        project_name,
                                        prefix.get(
                                            'License',
                                            '',
                                        )
                                        .replace(
                                            'License',
                                            '',
                                        )
                                        .strip(': '),
                                        output,
                                        prefix,
                                    )
                                    if isinstance(result, list):
                                        return result, output, prefix
                                case x if x == 'license_':
                                    _license, output, prefix = _P.license_(
                                        project_name,
                                        output,
                                        prefix,
                                    )
                                    if isinstance(_license, str):
                                        result, output, prefix = _P.license_expression(
                                            project_name,
                                            _license,
                                            output,
                                            prefix,
                                        )
                                    if isinstance(result, list):  # pyright: ignore
                                        return result, output, prefix
                                case x if x and x in (
                                    'audience',
                                    'environment',
                                    'framework',
                                    'language',
                                    'status',
                                    'topic',
                                ):
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
                                case x:
                                    result, output, prefix = getattr(_P, x)(
                                        project_name,
                                        output,
                                        prefix,
                                    )
                                    if isinstance(result, list):
                                        return result, output, prefix
            case 0:
                while True:
                    match button_dialog(
                        title='ozi-new interactive prompt',
                        text='Options menu, select an option:',
                        buttons=[
                            ('← Back', True),
                        ],
                        style=_style,
                    ).run():
                        case True:
                            break
            case 1:
                if admonition_dialog(
                    title='ozi-new interactive prompt',
                    heading_label='PKG-INFO Metadata:',
                    text='\n'.join(
                        prefix.values() if len(prefix) > 0 else {'Name:': 'Name:'},
                    ),
                    ok_text='⌂ Prompt',
                    cancel_text='← Back',
                ).run():
                    break
    return None, output, prefix


def interactive_prompt(project: Namespace) -> list[str]:  # noqa: C901  # pragma: no cover
    curses.setupterm()
    e3 = curses.tigetstr('E3') or b''
    clear_screen_seq = curses.tigetstr('clear') or b''
    os.write(sys.stdout.fileno(), e3 + clear_screen_seq)

    if (
        admonition_dialog(
            title='ozi-new interactive prompt',
            heading_label='Disclaimer',
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
    project_name = '""'

    result, output, prefix = _P.name(output, prefix, project.check_package_exists)
    if isinstance(result, list):
        return result
    if isinstance(result, str):
        project_name = result

    result, output, prefix = _P.summary(project_name, output, prefix)
    if isinstance(result, list):
        return result

    result, output, prefix = _P.keywords(project_name, output, prefix)
    if isinstance(result, list):
        return result

    result, output, prefix = _P.home_page(project_name, output, prefix)
    if isinstance(result, list):
        return result

    result, output, prefix = _P.author(project_name, output, prefix)
    if isinstance(result, list):
        return result

    result, output, prefix = _P.author_email(project_name, output, prefix)
    if isinstance(result, list):
        return result

    result, output, prefix = _P.license_(project_name, output, prefix)
    if isinstance(result, list):
        return result
    _license = result if result else ''

    result, output, prefix = _P.license_expression(project_name, _license, output, prefix)
    if isinstance(result, list):
        return result

    if yes_no_dialog(
        title='ozi-new interactive prompt',
        text=f'Are there any maintainers of {project_name}?\n(other than the author or authors)',
        style=_style,
    ).run():
        result, output, prefix = _P.maintainer(project_name, output, prefix)
        if isinstance(result, list):
            return result

        result, output, prefix = _P.maintainer_email(project_name, output, prefix)
        if isinstance(result, list):
            return result

    result, output, prefix = _P.requires_dist(project_name, output, prefix)
    if isinstance(result, list):
        return result

    while not admonition_dialog(
        title='ozi-new interactive prompt',
        heading_label='Confirm project creation?\nPKG-INFO Metadata:',
        text='\n'.join(prefix.values()),
        ok_text='✔ Ok',
        cancel_text='☰  Menu',
    ).run():
        result, output, prefix = menu_loop(output, prefix)
        if isinstance(result, list):
            return result

    return output
