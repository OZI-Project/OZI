# ozi/spec/project.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Project specification metadata."""
from dataclasses import dataclass

from ozi.spec.base import Default
from ozi.spec.ci import CI
from ozi.spec.ci import Build
from ozi.spec.ci import CheckpointSuite
from ozi.spec.ci import ClassicDist
from ozi.spec.ci import ClassicLint
from ozi.spec.ci import ClassicTest
from ozi.spec.ci import RuffLint
from ozi.spec.pkg import Pkg
from ozi.spec.python import Support
from ozi.spec.src import Src


@dataclass(slots=True, frozen=True, eq=True, repr=False)
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


@dataclass(slots=True, frozen=True, eq=True, repr=False)
class ClassicProject(PythonProject):
    """OZI project using classic Python checkpoint toolchains."""


@dataclass(slots=True, frozen=True, eq=True, repr=False)
class RuffProject(PythonProject):
    """Alternative to classic project using ruff for linting and formatting."""

    lint: RuffLint = RuffLint()
