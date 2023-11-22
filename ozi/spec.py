"""Specification API for OZI Metadata."""
from __future__ import annotations

import platform
import sys
from datetime import date
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from functools import cached_property
from importlib.metadata import PackageNotFoundError
from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Protocol

if sys.version_info >= (3, 11):  # pragma: no cover
    from typing import Self
else:  # pragma: no cover
    from typing_extensions import Self

from typing import Sequence
from typing import TypeAlias
from warnings import warn

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Callable
    from collections.abc import Mapping

    _VT: TypeAlias = list['_KT'] | Mapping[str, '_KT']
    _KT: TypeAlias = str | int | float | None | _VT
    _Lambda: TypeAlias = Callable[[], '_FactoryMethod']
    _FactoryMethod: TypeAlias = Callable[[], _Lambda]

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from dataclasses import fields
from importlib.metadata import version

__all__ = (
    'Build',
    'CI',
    'Checkpoint',
    'CheckpointSuite',
    'ClassicDist',
    'ClassicLint',
    'ClassicProject',
    'ClassicTest',
    'Default',
    'License',
    'Metadata',
    'OZI',
    'Pkg',
    'PkgInfo',
    'PkgPattern',
    'PkgRequired',
    'Publish',
    'PythonProject',
    'PythonSupport',
    'RuffLint',
    'RuffProject',
    'Spec',
    'SrcFormat',
    'SrcRequired',
    'SrcTemplate',
    'Support',
)

pymajor, pyminor, pypatch = map(int, platform.python_version_tuple())
DATE_FORMAT = '%Y-%m-%d'
DEPRECATION_DELTA_WEEKS = 104


def current_version() -> str:
    """Returns the currently installed version of OZI."""
    try:
        return version('OZI')
    except PackageNotFoundError:  # pragma: no cover
        from setuptools_scm import get_version  # type: ignore

        return str(get_version(root='..', relative_to=__file__))


class _FactoryDataclass(Protocol):
    """A dataclass that, when called, returns a factory method."""

    __dataclass_fields__: ClassVar[dict[str, _VT]]

    def asdict(self: Self) -> dict[str, _VT]:
        ...

    def __call__(self: Self) -> _FactoryMethod:
        ...


@dataclass(frozen=True)
class Default(_FactoryDataclass):
    """A dataclass that, when called, returns it's own default factory method."""

    def __call__(self: Self) -> _FactoryMethod:  # pragma: defer to python
        return field(default_factory=lambda: self())

    def asdict(self: Self) -> dict[str, _VT]:
        """Return a dictionary of all fields where repr=True.
        Hide a variable from the dict by setting repr to False and using
        a Default subclass as the default_factory.
        Typing is compatible with Jinja2 Environment and JSON.
        """
        all_fields = (
            (
                f.name,
                getattr(self, f.name)
                if not isinstance(getattr(self, f.name), Default)
                else getattr(self, f.name).asdict(),
            )
            for f in fields(self)
            if f.repr
        )

        return dict(all_fields) | {
            'help': str(self.__class__.__doc__).replace('\n   ', ''),
        }

    def __len__(self: Self) -> int:  # pragma: defer to python
        return len(list(iter(asdict(self))))


@dataclass(frozen=True, slots=True, eq=True)
class PythonSupport(Default):
    """Datatype for OZI Python version support."""

    deprecation_schedule: dict[int, str] = field(
        default_factory=lambda: {
            8: date(2024, 10, 1).strftime(DATE_FORMAT),
            9: date(2025, 10, 1).strftime(DATE_FORMAT),
            10: date(2026, 10, 1).strftime(DATE_FORMAT),
            11: date(2027, 10, 1).strftime(DATE_FORMAT),
            12: date(2028, 10, 1).strftime(DATE_FORMAT),
            13: date(2029, 10, 1).strftime(DATE_FORMAT),
        },
    )
    major: str = field(init=False, default='3')
    current_date: str = field(
        init=False,
        compare=False,
        default_factory=lambda: datetime.now(tz=timezone.utc).date().strftime(DATE_FORMAT),
    )

    def __post_init__(self: Self) -> None:
        python3_eol = (
            datetime.strptime(
                self.deprecation_schedule.get(
                    pyminor,
                    date(2008, 12, 3).strftime(DATE_FORMAT),
                ),
                DATE_FORMAT,
            )
            .replace(tzinfo=timezone.utc)
            .date()
        )
        ozi_support_eol = python3_eol - timedelta(weeks=DEPRECATION_DELTA_WEEKS)
        if datetime.now(tz=timezone.utc).date() > python3_eol:  # pragma: no cover
            text = (
                f'Python {pymajor}.{pyminor}.{pypatch} is not supported as of {python3_eol}.'
            )
            raise RuntimeError(text)
        elif datetime.now(tz=timezone.utc).date() > ozi_support_eol:  # pragma: no cover
            warn(
                f'Python {pymajor}.{pyminor}.{pypatch} support is deprecated '
                f'as of {ozi_support_eol}.',
                DeprecationWarning,
            )

    @cached_property
    def _minor_versions(self: Self) -> list[int]:
        return sorted(
            [
                k
                for k, v in self.deprecation_schedule.items()
                if datetime.strptime(v, DATE_FORMAT).replace(tzinfo=timezone.utc)
                - timedelta(weeks=DEPRECATION_DELTA_WEEKS)
                > datetime.strptime(self.current_date, DATE_FORMAT).replace(
                    tzinfo=timezone.utc,
                )
            ],
        )[:4]

    @cached_property
    def bugfix1_minor(self: Self) -> int:
        _, _, bugfix1, *_ = self._minor_versions
        return bugfix1

    @cached_property
    def bugfix1(self: Self) -> str:
        return '.'.join(map(str, (self.major, self.bugfix1_minor)))

    @cached_property
    def bugfix2_minor(self: Self) -> int:
        _, bugfix2, *_ = self._minor_versions
        return bugfix2

    @cached_property
    def bugfix2(self: Self) -> str:
        return '.'.join(map(str, (self.major, self.bugfix2_minor)))

    @cached_property
    def security_minor(self: Self) -> int:
        security, *_ = self._minor_versions
        return security

    @cached_property
    def security(self: Self) -> str:
        return '.'.join(map(str, (self.major, self.security_minor)))

    @cached_property
    def prerelease_minor(self: Self) -> int | None:
        _, _, _, *prerelease = self._minor_versions
        return prerelease[0] if prerelease else None

    @cached_property
    def prerelease(self: Self) -> str:
        if self.prerelease_minor:
            return '.'.join(map(str, (self.major, self.prerelease_minor)))
        return ''  # pragma: defer to good-first-issue

    @cached_property
    def classifiers(self: Self) -> Sequence[tuple[str, str]]:
        classifiers = [
            ('Classifier', f'Programming Language :: Python :: {self.major} :: Only'),
            (
                'Classifier',
                f'Programming Language :: Python :: {self.security}',
            ),
            (
                'Classifier',
                f'Programming Language :: Python :: {self.bugfix2}',
            ),
            (
                'Classifier',
                f'Programming Language :: Python :: {self.bugfix1}',
            ),
        ]
        if self.prerelease_minor:  # pragma: no cover
            classifiers += [
                ('Classifier', f'Programming Language :: Python :: {self.prerelease}'),
            ]
        return classifiers


@dataclass(kw_only=True, frozen=True, eq=True)
class CheckpointSuite(Default):
    """OZI checkpoint base class."""

    exclude: tuple[str, ...] = field(default_factory=tuple)
    module: tuple[str, ...] = field(default_factory=tuple)
    plugin: Mapping[str, str] = field(default_factory=dict)
    utility: Mapping[str, str] = field(default_factory=dict)


@dataclass(slots=True, frozen=True, eq=True)
class RuffLint(CheckpointSuite):
    """OZI experimental linting and formatting with ruff."""

    module: tuple[str, ...] = ('ruff', 'mypy', 'pyright')
    exclude: tuple[str, ...] = ('meson-private',)
    utility: Mapping[str, str] = field(
        default_factory=lambda: {
            'ruff': 'ruff>=0.1.6',
            'mypy': 'mypy',
            'pyright': 'pyright',
        },
    )


@dataclass(slots=True, frozen=True, eq=True)
class ClassicLint(CheckpointSuite):
    """OZI standard linting and formatting suite."""

    module: tuple[str, ...] = ('bandit', 'black', 'flake8', 'isort', 'mypy', 'pyright')
    exclude: tuple[str, ...] = ('venv', 'meson-private')
    utility: Mapping[str, str] = field(
        default_factory=lambda: {
            'bandit': 'bandit[toml]',
            'black': 'black',
            'flake8': 'flake8',
            'isort': 'isort',
            'mypy': 'mypy',
            'pyright': 'pyright',
        },
    )
    plugin: Mapping[str, str] = field(
        default_factory=lambda: {
            'Flake8-pyproject': 'Flake8-pyproject',
            'flake8-annotations': 'flake8-annotations',
            'flake8-broken-line': 'flake8-broken-line',
            'flake8-bugbear': 'flake8-bugbear',
            'flake8-comprehensions': 'flake8-comprehensions',
            'flake8-datetimez': 'flake8-datetimez',
            'flake8-docstring-checker': 'flake8-docstring-checker',
            'flake8-eradicate': 'flake8-eradicate',
            'flake8-fixme': 'flake8-fixme',
            'flake8-leading-blank-lines': 'flake8-leading-blank-lines',
            'flake8-no-pep420': 'flake8-no-pep420',
            'flake8-pyi': 'flake8-pyi',
            'flake8-pytest-style': 'flake8-pytest-style',
            'flake8-quotes': 'flake8-quotes',
            'flake8-tidy-imports': 'flake8-tidy-imports',
            'flake8-type-checking': 'flake8-type-checking',
        },
    )


@dataclass(slots=True, frozen=True, eq=True)
class ClassicTest(CheckpointSuite):
    """OZI standard testing and coverage."""

    module: tuple[str, ...] = ('coverage', 'pytest')
    plugin: Mapping[str, str] = field(
        default_factory=lambda: {
            'hypothesis': 'hypothesis[all]',
            'pytest-asyncio': 'pytest-asyncio',
            'pytest-cov': 'pytest-cov',
            'pytest-randomly': 'pytest-randomly',
            'pytest-tcpclient': 'pytest-tcpclient',
            'pytest-xdist': 'pytest-xdist',
        },
    )
    utility: Mapping[str, str] = field(
        default_factory=lambda: {
            'coverage': 'coverage[toml]',
            'pytest': 'pytest',
        },
    )


@dataclass(slots=True, frozen=True, eq=True)
class ClassicDist(CheckpointSuite):
    """OZI standard publishing and distribution."""

    module: tuple[str, ...] = ('pyc_wheel', 'python-semantic-release', 'sigstore')
    utility: Mapping[str, str] = field(
        default_factory=lambda: {
            'pyc_wheel': 'pyc_wheel',
            'python-semantic-release': 'python-semantic-release',
            'sigstore': 'sigstore',
        },
    )


@dataclass(slots=True, frozen=True, eq=True)
class Publish(Default):
    """Publishing patterns for packaged project."""

    include: tuple[str, ...] = ('*.tar.gz', '*.whl', 'sig/*')


@dataclass(slots=True, frozen=True, eq=True)
class Checkpoint(Default):
    """Checkpoint suites to run."""

    suites: tuple[str, ...] = ('dist', 'lint', 'test')


@dataclass(slots=True, frozen=True, eq=True)
class CI(Default):
    """Provider-agnostic CI information."""

    backend: str = 'tox'
    checkpoint: Checkpoint = Checkpoint()
    publish: Publish = Publish()
    providers: tuple[str, ...] = ('github',)


@dataclass(slots=True, frozen=True, eq=True)
class SrcFormat(Default):
    """Python source code formatting specification."""

    date: str = '%Y-%m-%d %H:%M:%S'
    line_end: str = 'LF'
    quotes: str = 'single'
    log: str = '%(asctime)s [%(levelname)8s] %(name)s: %(message)s (%(filename)s:%(lineno)s)'
    max_line_length: str = '93'
    version_placeholder: str = '{version}'


@dataclass(slots=True, frozen=True, eq=True)
class SrcRequired(Default):
    """Required files for OZI to output with ``ozi-new``."""

    root: tuple[str, ...] = (
        'README.rst',
        '.gitignore',
        'pyproject.toml',
        'meson.build',
        'meson.options',
        'LICENSE.txt',
        'PKG-INFO',
        'requirements.in',
        'CHANGELOG.md',
    )
    source: tuple[str, ...] = (
        'meson.build',
        '__init__.py',
        'py.typed',
    )
    test: tuple[str, ...] = ('meson.build',)


@dataclass(slots=True, frozen=True, eq=True)
class SrcTemplate(Default):
    """OZI templates folder layout.
    This is also the relative search directory used when searching
    for ``ozi-new`` user-provided templates in the ``templates/``
    root directory.
    """

    root: tuple[str, ...] = (
        '.gitignore',
        'meson.build',
        'meson.options',
        'PKG-INFO',
        'pyproject.toml',
        'README.rst',
        'LICENSE.txt',
        'requirements.in',
        'CHANGELOG.md',
    )
    source: tuple[str, ...] = (
        'project.name/__init__.py',
        'project.name/meson.build',
        'project.name/py.typed',
    )
    test: tuple[str, ...] = ('tests/meson.build',)
    ci_provider: Mapping[str, str] = field(
        default_factory=lambda: {'github': 'github_workflows/ozi.yml'},
    )
    add_root: str = field(default='project.name/new_test.py')
    add_source: str = field(default='project.name/new_module.py')
    add_test: str = field(default='tests/new_test.py')


@dataclass(slots=True, frozen=True, eq=True)
class PkgRequired(Default):
    """Required files for OZI project publishing."""

    root: tuple[str, ...] = (
        'README.rst',
        'CHANGELOG.md',
        'pyproject.toml',
        'PKG-INFO',
        'LICENSE.txt',
        'requirements.in',
    )

    source: tuple[str, ...] = ('__init__.py',)

    test: tuple[str, ...] = ()


@dataclass(slots=True, frozen=True, eq=True)
class PkgPattern(Default):
    """Regex patterns (or deferrals) for PKG-INFO headers."""

    name: str = r'^([A-Za-z]|[A-Za-z][A-Za-z0-9._-]*[A-Za-z0-9]){1,80}$'
    keywords: str = r'^(([a-z_]*[a-z0-9],)*{2, 650})$'
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
class PkgInfo(Default):
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


@dataclass(slots=True, frozen=True, eq=True)
class Build(Default):
    """Build backend and required packages for OZI."""

    backend: str = 'mesonpep517.buildapi'
    requires: Mapping[str, str] = field(
        default_factory=lambda: {
            'mesonpep517': 'mesonpep517',
            'meson': 'meson>=1.1.0',
            'ninja': 'ninja',
            'pip-tools': 'pip-tools',
            'setuptools': 'setuptools>=64',
            'setuptools_scm': 'setuptools_scm[toml]>=6.2',
            'tomli': 'tomli>=2.0.0',
        },
    )


@dataclass(slots=True, frozen=True, eq=True)
class Support(Default):
    """Python implementation and version support info for OZI."""

    implementations: tuple[str, ...] = ('CPython',)
    metadata_version: str = '2.1'
    major: str = '3'
    prerelease: str = PythonSupport().prerelease
    bugfix1: str = PythonSupport().bugfix1
    bugfix2: str = PythonSupport().bugfix2
    security: str = PythonSupport().security
    deprecation_schedule: Mapping[int, str] = field(
        default_factory=lambda: PythonSupport().deprecation_schedule,
    )
    deprecation_delta_weeks: int = DEPRECATION_DELTA_WEEKS


@dataclass(slots=True, frozen=True, eq=True)
class License(Default):
    """Licensing specification metadata."""

    ambiguous: Mapping[str, tuple[str, ...]] = field(
        default_factory=lambda: {
            'Private': ('LicenseRef-Proprietary',),
            'DFSG approved': (
                'AGPL-3.0-only',
                'AGPL-3.0-or-later',
                'Apache-2.0',
                'Artistic-2.0',
                'BSD-3-Clause',
                'CC-BY-4.0',
                'CC-BY-SA-4.0',
                'EPL-1.0',
                'GPL-2.0-only',
                'GPL-2.0-or-later',
                'GPL-3.0-only',
                'GPL-3.0-or-later',
                'ISC',
                'LGPL-2.1-or-later',
                'LGPL-3.0-only',
                'LGPL-3.0-or-later',
                'MIT',
                'OFL-1.1',
                'WTFPL',
                'Zlib',
            ),
            'OSI Approved :: Academic Free License (AFL)': ('AFL-3.0',),
            'OSI Approved :: Apache Software License': ('Apache-2.0',),
            'OSI Approved :: Apple Public Source License': (
                'APSL-1.0',
                'APSL-1.1',
                'APSL-1.2',
                'APSL-2.0',
            ),
            'OSI Approved :: Artistic License': ('Artistic-2.0',),
            'OSI Approved :: BSD License': (
                '0BSD',
                'BSD-2-Clause',
                'BSD-3-Clause',
                'BSD-3-Clause-Clear',
                'BSD-4-Clause',
            ),
            'OSI Approved :: GNU Affero General Public License v3': (
                'AGPL-3.0-only',
                'AGPL-3.0-or-later',
            ),
            'OSI Approved :: GNU Free Documentation License (FDL)': (
                'GFDL-1.3-only',
                'GFDL-1.3-or-later',
            ),
            'OSI Approved :: GNU General Public License (GPL)': (
                'GPL-2.0-only',
                'GPL-2.0-or-later',
                'GPL-3.0-only',
                'GPL-3.0-or-later',
            ),
            'OSI Approved :: GNU General Public License v2 (GPLv2)': (
                'GPL-2.0-only',
                'GPL-2.0-or-later',
            ),
            'OSI Approved :: GNU General Public License v3 (GPLv3)': (
                'GPL-3.0-only',
                'GPL-3.0-or-later',
            ),
            'OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)': (
                'LGPL-2.0-only',
            ),
            'OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)': (
                'LGPL-2.1-or-later',
            ),
            'OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)': (
                'LGPL-3.0-only',
                'LGPL-3.0-or-later',
            ),
            'OSI Approved :: GNU Library or Lesser General Public License (LGPL)': (
                'LGPL-2.1-or-later',
                'LGPL-3.0-only',
                'LGPL-3.0-or-later',
            ),
            'Public Domain': ('LicenseRef-Public-Domain', 'CC0-1.0', 'Unlicense'),
        },
    )
    exceptions: tuple[str, ...] = (
        '389-exception',
        'Asterisk-exception',
        'Autoconf-exception-2.0',
        'Autoconf-exception-3.0',
        'Autoconf-exception-generic',
        'Autoconf-exception-macro',
        'Bison-exception-2.2',
        'Bootloader-exception',
        'Classpath-exception-2.0',
        'CLISP-exception-2.0',
        'cryptsetup-OpenSSL-exception',
        'DigiRule-FOSS-exception',
        'eCos-exception-2.0',
        'Fawkes-Runtime-exception',
        'FLTK-exception',
        'Font-exception-2.0',
        'freertos-exception-2.0',
        'GCC-exception-2.0',
        'GCC-exception-3.1',
        'GNAT-exception',
        'gnu-javamail-exception',
        'GPL-3.0-interface-exception',
        'GPL-3.0-linking-exception',
        'GPL-3.0-linking-source-exception',
        'GPL-CC-1.0',
        'GStreamer-exception-2005',
        'GStreamer-exception-2008',
        'i2p-gpl-java-exception',
        'KiCad-libraries-exception',
        'LGPL-3.0-linking-exception',
        'libpri-OpenH323-exception',
        'Libtool-exception',
        'Linux-syscall-note',
        'LLGPL',
        'LLVM-exception',
        'LZMA-exception',
        'mif-exception',
        'OCaml-LGPL-linking-exception',
        'OCCT-exception-1.0',
        'OpenJDK-assembly-exception-1.0',
        'openvpn-openssl-exception',
        'PS-or-PDF-font-exception-20170817',
        'QPL-1.0-INRIA-2004-exception',
        'Qt-GPL-exception-1.0',
        'Qt-LGPL-exception-1.1',
        'Qwt-exception-1.0',
        'SHL-2.0',
        'SHL-2.1',
        'SWI-exception',
        'Swift-exception',
        'u-boot-exception-2.0',
        'Universal-FOSS-exception-1.0',
        'vsftpd-openssl-exception',
        'WxWindows-exception-3.1',
        'x11vnc-openssl-exception',
    )


@dataclass(slots=True, frozen=True, eq=True)
class Src(Default):
    """Python source code metadata."""

    format: SrcFormat = SrcFormat()
    required: SrcRequired = SrcRequired()
    template: SrcTemplate = field(default_factory=SrcTemplate)


@dataclass(slots=True, frozen=True, eq=True)
class Pkg(Default):
    """Packaging specification metadata."""

    wheel: bool = True
    sdist: bool = True
    required: PkgRequired = PkgRequired()
    license: License = License()
    pattern: PkgPattern = PkgPattern()
    info: PkgInfo = PkgInfo()


@dataclass(slots=True, frozen=True, eq=True)
class PythonProject(Default):
    """Base class for Python Project specification metadata."""

    ci: CI = CI()
    support: Support = Support()
    dist: CheckpointSuite = ClassicDist()
    lint: CheckpointSuite = ClassicLint()
    test: CheckpointSuite = ClassicTest()
    build: Build = Build()
    pkg: Pkg = Pkg()
    src: Src = Src()


@dataclass(slots=True, frozen=True, eq=True)
class ClassicProject(PythonProject):
    """OZI project using classic Python checkpoint toolchains."""


@dataclass(slots=True, frozen=True, eq=True)
class RuffProject(PythonProject):
    """Alternative to classic project using ruff for linting and formatting."""

    lint: RuffLint = RuffLint()


@dataclass(slots=True, frozen=True, eq=True)
class Spec(Default):
    """OZI Specification metadata."""

    version: str = field(default='0.1', init=False)
    python: PythonProject = ClassicProject()


@dataclass(slots=True, frozen=True, eq=True)
class OZI(Default):
    """OZI distribution metadata."""

    version: str = field(default_factory=current_version)
    python_support: PythonSupport = PythonSupport()


@dataclass(slots=True, frozen=True, eq=True)
class Metadata(Default):
    """OZI metadata."""

    ozi: OZI = OZI()
    spec: Spec = field(default_factory=Spec)
