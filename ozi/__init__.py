"""Core OZI packaging management plane module."""
# ozi/__init__.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
from importlib.metadata import version
from typing import List
from warnings import warn

from packaging.version import Version, parse

from .assets import (
    implementation_support,
    meson_min_version,
    metadata_version,
    python_support,
    specification_version,
)

metadata = {
    'ozi': {
        'version': version('OZI'),
        'metadata_version': metadata_version,
        'spec': specification_version,
        'meson_min_version': meson_min_version,
        'py_major': python_support.major,
        'py_security': '.'.join(map(str, (python_support.major, python_support.security))),
        'py_bugfix2': '.'.join(map(str, (python_support.major, python_support.bugfix2))),
        'py_bugfix1': '.'.join(map(str, (python_support.major, python_support.bugfix1))),
        'py_implementations': implementation_support,
    }
}


def check_for_update(
    current_version: Version, releases: List[str]
) -> None:  # pragma: no cover
    """Issue a warning if installed version of OZI is not up to date."""
    match max(map(parse, releases)):
        case latest if latest > current_version:
            warn(
                'Newer version of OZI available to download on PyPI: '
                'https://pypi.org/project/OZI/',
                RuntimeWarning,
            )
        case latest if latest < current_version:
            print('ok - OZI package is development version.')
        case latest if latest == current_version:
            print('ok - OZI package is up to date.')
