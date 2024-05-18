# ozi/spec/_spec.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Specification API for OZI Metadata."""
from dataclasses import dataclass
from dataclasses import field
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version

from ozi.spec.base import Default
from ozi.spec.ci import RuffLint
from ozi.spec.project import ClassicProject
from ozi.spec.project import PythonProject
from ozi.spec.python import PythonSupport


def current_version() -> str:
    """Returns the currently installed version of OZI."""
    try:
        return version('OZI')
    except PackageNotFoundError:  # pragma: no cover
        from setuptools_scm import get_version  # type: ignore

        return str(get_version(root='..', relative_to=__file__))


@dataclass(slots=True, frozen=True, eq=True)
class Spec(Default):
    """OZI Specification metadata."""

    version: str = '0.4'
    python: PythonProject = ClassicProject()


@dataclass(slots=True, frozen=True, eq=True)
class Experimental(Default):
    """Experimental OZI specifications."""

    ruff: RuffLint = RuffLint()


@dataclass(slots=True, frozen=True, eq=True)
class OZI(Default):
    """OZI distribution metadata."""

    version: str = field(default_factory=current_version)
    python_support: PythonSupport = PythonSupport()
    experimental: Experimental = Experimental()


@dataclass(slots=True, frozen=True, eq=True)
class Metadata(Default):
    """OZI metadata."""

    ozi: OZI = OZI()
    spec: Spec = field(default_factory=Spec)
