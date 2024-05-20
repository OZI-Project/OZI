# ozi/spec/pkg.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Package specification metadata."""
from __future__ import annotations

from collections.abc import Mapping  # noqa: TCH003,TC003,RUF100
from dataclasses import dataclass
from dataclasses import field

from ozi.spec._license import SPDX_LICENSE_EXCEPTIONS
from ozi.spec._license import SPDX_LICENSE_MAP
from ozi.spec.base import Default


@dataclass(slots=True, frozen=True, eq=True, repr=False)
class PkgVersion(Default):
    """Versioning metadata.

    .. versionchanged:: 1.5
       default to `angular` semantic instead of `emoji`
    """

    semantic: str = 'angular'
    major_tags: tuple[str] = (':boom:',)
    minor_tags: tuple[str] = (':sparkles:',)
    patch_tags: tuple[str, ...] = (
        ':adhesive_bandage:',
        ':alembic:',
        ':alien:',
        ':ambulance:',
        ':apple:',
        ':arrow_down:',
        ':arrow_up:',
        ':bento:',
        ':bug:',
        ':bulb:',
        ':card_file_box:',
        ':chart_with_upwards_trend:',
        ':checkered_flag:',
        ':children_crossing:',
        ':dizzy:',
        ':egg:',
        ':fire:',
        ':globe_with_meridians:',
        ':goal_net:',
        ':green_apple:',
        ':green_heart:',
        ':hammer:',
        ':heavy_minus_sign:',
        ':heavy_plus_sign:',
        ':iphone:',
        ':label:',
        ':lipstick:',
        ':lock:',
        ':mag:',
        ':necktie:',
        ':package:',
        ':passport_control:',
        ':pencil2:',
        ':penguin:',
        ':pushpin:',
        ':recycle:',
        ':rewind:',
        ':robot:',
        ':speech_balloon:',
        ':triangular_flag_on_post:',
        ':wastebasket:',
        ':wheelchair:',
        ':wrench:',
        ':zap:',
    )


@dataclass(slots=True, frozen=True, eq=True)
class PkgRequired(Default):
    """Required files for OZI project publishing."""

    root: tuple[str, ...] = (
        'README',
        'CHANGELOG.md',
        'pyproject.toml',
        'LICENSE.txt',
        'requirements.in',
    )

    source: tuple[str, ...] = ('__init__.py',)

    test: tuple[str, ...] = ()


@dataclass(slots=True, frozen=True, eq=True)
class PkgPattern(Default):
    """Regex patterns (or deferrals) for PKG-INFO headers."""

    name: str = r'^([A-Za-z]|[A-Za-z][A-Za-z0-9._-]*[A-Za-z0-9]){1,80}$'
    version: str = r'^(?P<prefix>v)?(?P<version>[^\\+]+)(?P<suffix>.*)?$'
    keywords: str = r'^(([a-z_]*[a-z0-9],)*{2,650})$'
    email: str = 'defer to RFC'
    license: str = 'defer to SPDX'
    license_id: str = 'defer to SPDX'
    license_exception_id = 'defer to SPDX'
    url: str = 'defer to IDNA'
    author: str = r'^((.+?)(?:,\s*|$)){1,128}$'
    summary: str = r'^((?\s).*){1,255}$'
    copyright_head: str = r'^((?\s).*){1,255}$'
    classifiers: str = r'^([\w\s]*\s\:\:\s)?'


@dataclass(slots=True, frozen=True, eq=True)
class PkgClassifiers(Default):
    """PKG-INFO default classifier metadata."""

    intended_audience: list[str] = field(default_factory=lambda: ['Other Audience'])
    typing: list[str] = field(default_factory=lambda: ['Typed'])
    environment: list[str] = field(default_factory=lambda: ['Other Environment'])
    language: list[str] = field(default_factory=lambda: ['English'])
    development_status: tuple[str] = ('1 - Planning',)


@dataclass(slots=True, frozen=True, eq=True)
class PkgInfo(Default):
    """PKG-INFO defaults metadata."""

    required: tuple[str, ...] = (
        'Author',
        'Author-email',
        'Description-Content-Type',
        'Home-page',
        'License',
        'Metadata-Version',
        'Name',
        'Summary',
        'Version',
    )
    classifiers: PkgClassifiers = PkgClassifiers()


@dataclass(slots=True, frozen=True, eq=True)
class License(Default):
    """Licensing specification metadata."""

    ambiguous: Mapping[str, tuple[str, ...]] = field(
        default_factory=lambda: SPDX_LICENSE_MAP,
    )
    exceptions: tuple[str, ...] = SPDX_LICENSE_EXCEPTIONS


@dataclass(slots=True, frozen=True, eq=True, repr=False)
class Pkg(Default):
    """Packaging specification metadata."""

    wheel: bool = True
    sdist: bool = True
    required: PkgRequired = PkgRequired()
    license: License = License()
    pattern: PkgPattern = PkgPattern()
    version: PkgVersion = PkgVersion()
    info: PkgInfo = PkgInfo()
