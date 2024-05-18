.. OZI
  Classifier: License-Expression :: Apache-2.0 WITH LLVM-exception
  Classifier: License-File :: LICENSE.txt

.. README.rst
   Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
   See LICENSE.txt for license information.


===
OZI
===

.. image:: https://www.oziproject.dev/assets/brand/images/ozi_logo_v2.svg
  :align: left
  :height: 62
  :target: https://www.oziproject.dev/

OZI is a set of publishing tools for creating and maintaining pure Python packages.
See the `documentation <https://docs.oziproject.dev/>`_ for the project roadmap,
API specification, Meson version support, and other project information.

Project Information
-------------------

|py-version-badge| |License| |slsa-level3-badge|

|openssf-badge| |OSSF-Scorecard| |SourceRank|

Purpose
^^^^^^^

OZI is meant for Python developers as a standardized and opinionated
Python packaging style guide and continuous integration checkpointing API using the Meson build system.

The OZI continuous integration strategy consists of:

1. The following isolated checkpoint environments:

* code testing and coverage
* distributing Python packages with Meson_
* code linting and formatting

2. Release drafting
3. Building of releases
4. Provenance generation (`SLSA v1.0 - Level 3 <https://slsa.dev/spec/v1.0/levels#build-l3>`_)
5. Publishing

What OZI is **not**
###################

* A replacement for test environment managers like tox_, as a matter of fact OZI uses ``tox``.
* A replacement for git hook package management tools like pre-commit_

What OZI is
###########

* Checkpointed Python packaging for Meson projects focused on pure Python sources.

Contributing
------------

See the project `CONTRIBUTING.md <https://github.com/rjdbcm/OZI/blob/main/.github/CONTRIBUTING.md>`_

Contact
-------

Eden Ross Duff MSc - help@oziproject.dev

.. image:: https://raw.githubusercontent.com/sigstore/community/main/artwork/badge/sigstore_codesigned_purple.png
 :align: center
 :height: 140
 :target: https://www.sigstore.dev/

.. |py-version-badge| image:: https://img.shields.io/pypi/pyversions/ozi?logo=python&label=Python%20Version
    :target: https://pypi.org/search/?q=&o=-created&c=Programming+Language+%3A%3A+Python+%3A%3A+3&c=Programming+Language+%3A%3A+Python+%3A%3A+3+%3A%3A+Only&c=Programming+Language+%3A%3A+Python+%3A%3A+3.10&c=Programming+Language+%3A%3A+Python+%3A%3A+3.11&c=Programming+Language+%3A%3A+Python+%3A%3A+3.12&c=Programming+Language+%3A%3A+Python+%3A%3A+Implementation&c=Programming+Language+%3A%3A+Python+%3A%3A+Implementation+%3A%3A+CPython&c=Typing+%3A%3A+Typed
    :alt: PyPI - Python Version
.. |slsa-level3-badge| image:: https://slsa.dev/images/gh-badge-level3.svg
    :target: https://slsa.dev/spec/v1.0/levels#build-l3
    :alt: Supply-chain Levels for Software Artifacts v1.0 Build L3
.. |openssf-badge| image:: https://img.shields.io/cii/level/7515?label=OpenSSF%20Best%20Practices&labelColor=0c3455&link=https%3A%2F%2Fwww.bestpractices.dev%2Fen%2Fprojects%2F7515
    :target: https://bestpractices.coreinfrastructure.org/projects/7515
    :alt: Open Source Security Foundation self-certification status
.. |SourceRank| image:: https://img.shields.io/librariesio/sourcerank/pypi/ozi?logo=libraries.io&label=SourceRank&link=https%3A%2F%2Flibraries.io%2Fpypi%2FOZI%2Fsourcerank
   :target: https://libraries.io/pypi/OZI/sourcerank
   :alt: Libraries.io SourceRank
.. |OSSF-Scorecard| image:: https://img.shields.io/ossf-scorecard/github.com/OZI-Project/OZI?label=OpenSSF%20Scorecard&labelColor=0c3455
    :target: https://securityscorecards.dev/viewer/?uri=github.com/OZI-Project/OZI&sort_by=risk-level&sort_direction=desc
    :alt: Open Source Security Foundation Scorecard
.. |License| image:: https://img.shields.io/badge/License-Apache--2.0_with_LLVM_exceptions-282661?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz48c3ZnIHZlcnNpb249IjEuMSIgaWQ9IkxheWVyXzEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHg9IjBweCIgeT0iMHB4IiB2aWV3Qm94PSIwIDAgMTIyLjg4IDEwMi43MiIgc3R5bGU9ImVuYWJsZS1iYWNrZ3JvdW5kOm5ldyAwIDAgMTIyLjg4IDEwMi43MiIgeG1sOnNwYWNlPSJwcmVzZXJ2ZSI%2BPHN0eWxlIHR5cGU9InRleHQvY3NzIj4uc3Qwe2ZpbGwtcnVsZTpldmVub2RkO2NsaXAtcnVsZTpldmVub2RkO308L3N0eWxlPjxnPjxwYXRoIGNsYXNzPSJzdDAiIGQ9Ik02NS42MSwyMC45MXY3Mi43NGgzNS42M2MwLjM4LDAsMC42OCwwLjMxLDAuNjgsMC42OXY3LjdjMCwwLjM4LTAuMzEsMC42OS0wLjY4LDAuNjlIMjIuODQgYy0wLjM4LDAtMC42OS0wLjMxLTAuNjktMC42OXYtNy43YzAtMC4zOCwwLjMxLTAuNjksMC42OS0wLjY5aDM1LjYzbDAtNzIuNzFjLTMuMS0xLjA4LTUuNTYtMy41My02LjY0LTYuNjNIMjkuM3YzLjQzIGMwLDAuMzgtMC4zMSwwLjY4LTAuNjgsMC42OGgtNS43OGMtMC4zOCwwLTAuNjktMC4zMS0wLjY5LTAuNjh2LTMuNDNoLTUuNzNjLTAuNDQsMC0wLjgtMC4zMS0wLjgtMC42OFY3Ljg0IGMwLTAuMzgsMC4zNi0wLjY5LDAuOC0wLjY5aDM1LjQzQzUzLjMzLDIuOTksNTcuMzEsMCw2MS45OSwwYzQuNjgsMCw4LjY2LDIuOTksMTAuMTQsNy4xNmgzNS41M2MwLjQ0LDAsMC44LDAuMzEsMC44LDAuNjl2NS43OCBjMCwwLjM4LTAuMzYsMC42OC0wLjgsMC42OGgtNi40NnYzLjQzYzAsMC4zOC0wLjMxLDAuNjgtMC42OCwwLjY4aC01Ljc4Yy0wLjM4LDAtMC42OS0wLjMxLTAuNjktMC42OHYtMy40M0g3Mi4xNiBDNzEuMDksMTcuMzgsNjguNjcsMTkuODEsNjUuNjEsMjAuOTFMNjUuNjEsMjAuOTF6IE05OS42NiwyMi4zbDIyLjkxLDQwLjQ4YzAuMiwwLjM1LDAuMjksMC43MywwLjI4LDEuMWgwLjAyYzAsMC4wNSwwLDAuMSwwLDAuMTUgYzAsOS42NC0xMS4zNSwxNy40Ni0yNS4zNSwxNy40NmMtMTMuODUsMC0yNS4xLTcuNjUtMjUuMzQtMTcuMTVjLTAuMDQtMC4xNi0wLjA2LTAuMzQtMC4wNi0wLjUxYzAtMC40NCwwLjE0LTAuODYsMC4zNy0xLjIgbDIzLjQzLTQwLjQzYzAuNTktMS4wMiwxLjg5LTEuMzcsMi45MS0wLjc4Qzk5LjIsMjEuNjUsOTkuNDgsMjEuOTUsOTkuNjYsMjIuM0w5OS42NiwyMi4zeiBNOTkuNzUsMzEuMTF2MzAuNmgxNy4zMkw5OS43NSwzMS4xMSBMOTkuNzUsMzEuMTF6IE05NS42Nyw2MS43VjMxLjE2TDc3Ljk2LDYxLjdIOTUuNjdMOTUuNjcsNjEuN3ogTTI3LjU0LDIyLjNsMjIuOTEsNDAuNDhjMC4yLDAuMzUsMC4yOSwwLjczLDAuMjgsMS4xaDAuMDIgYzAsMC4wNSwwLDAuMSwwLDAuMTVjMCw5LjY0LTExLjM1LDE3LjQ2LTI1LjM1LDE3LjQ2Yy0xMy44NSwwLTI1LjEtNy42NS0yNS4zNC0xNy4xNUMwLjAyLDY0LjE5LDAsNjQuMDIsMCw2My44NCBjMC0wLjQ0LDAuMTQtMC44NiwwLjM3LTEuMkwyMy44LDIyLjIxYzAuNTktMS4wMiwxLjg5LTEuMzcsMi45MS0wLjc4QzI3LjA4LDIxLjY1LDI3LjM2LDIxLjk1LDI3LjU0LDIyLjNMMjcuNTQsMjIuM3ogTTI3LjYzLDMxLjExdjMwLjZoMTcuMzJMMjcuNjMsMzEuMTFMMjcuNjMsMzEuMTF6IE0yMy41NCw2MS43VjMxLjE2TDUuODQsNjEuN0gyMy41NEwyMy41NCw2MS43eiBNNjEuOTksNi4wNyBjMi41OSwwLDQuNjksMi4xLDQuNjksNC42OWMwLDIuNTktMi4xLDQuNjktNC42OSw0LjY5Yy0yLjU5LDAtNC42OS0yLjEtNC42OS00LjY5QzU3LjMsOC4xNyw1OS40LDYuMDcsNjEuOTksNi4wN0w2MS45OSw2LjA3eiIvPjwvZz48L3N2Zz4%3D
   :alt: Static Badge
   :target: https://github.com/OZI-Project/OZI/blob/main/LICENSE.txt

.. _TOML: https://toml.io/en/
.. _PEP517: https://peps.python.org/pep-0517/
.. _build: https://pypi.org/project/build/
.. _mesonpep517: https://pypi.org/project/mesonpep517
.. _Ninja: https://pypi.org/project/ninja/
.. _setuptools: https://pypi.org/project/setuptools/
.. _setuptools_scm: https://pypi.org/project/setuptools_scm/
.. _Tomli: https://pypi.org/project/tomli/
.. _wheel: https://pypi.org/project/wheel/
.. _pre-commit: https://pre-commit.com/
.. _tox: https://tox.wiki/en/latest/
.. _Meson: https://mesonbuild.com/
