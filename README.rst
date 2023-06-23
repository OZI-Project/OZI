.. Copyright 2023 Ross J. Duff MSc 
   The copyright holder licenses this file
   to you under the Apache License, Version 2.0 (the
   "License"); you may not use this file except in compliance
   with the License.  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing,
   software distributed under the License is distributed on an
   "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
   KIND, either express or implied.  See the License for the
   specific language governing permissions and limitations
   under the License.
===
OZI
===

|py-version-badge| |slsa-level3-badge| |semantic-release-badge|
|coverage-badge| |pytest-plugins-badge| 
|bandit-badge| |black-badge| |isort-badge| |flake8-badge| |pyright-badge| |pylint-ckpt-badge| |rst-lint-badge|

OZI, an end-to-end Python packager for the Meson build system.

.. image:: https://raw.githubusercontent.com/sigstore/community/main/artwork/badge/sigstore_codesigned_purple.png
 :align: right
 :height: 140
 :target: https://www.sigstore.dev/

Project Information
-------------------

OZI,
`IPA pronunciation <http://ipa-reader.xyz/?text=o%CA%8Az%C9%9Bd%CB%88a%C9%AA&voice=Salli>`_ /oʊzɛdˈaɪ/,
is a packaging management plane for Python packages
built with Meson_. This allows you to create a versioned and traceable
system of development practices.

Purpose
^^^^^^^

Originally, OZI was created to fullfill the maintainers desire to put all packaging configuration
into a single ``pyproject.toml`` file. This is still the case but the focus of OZI is now to be a
Python packaging management plane tool. 

* What OZI is **not**:

  * A replacement for test environment managers like tox_, as a matter of fact OZI uses ``tox``.
  * A replacement for git hook package management tools like pre-commit_

* What OZI is: A Python packaging management plane tool for...

  * code testing and coverage
  * distributing Python packages with Meson_
  * documentation linting, build, and doctests
  * code linting and formatting

Limitations
^^^^^^^^^^^

Due to reliance on features introduced in
`Meson version 1.1.0 <https://mesonbuild.com/Release-notes-for-1-1-0.html>`_
that is our minimum supported version, we do not currently plan support for prior releases. 
However, we are open to contributions or comments in this regard. 

As a convention, we will only support 
the 3 most recent `Python versions <https://devguide.python.org/versions/#versions>`_
that are not ``end-of-life``, ``prerelease``, or ``feature`` status.

Backend Toolchain
^^^^^^^^^^^^^^^^^

These are the build-system packages and their dependencies

* build_:
  A simple, correct Python build frontend.
* Meson_ (only Meson versions > 1.1.0):
  Next-generation build system that organizes the toolchain described here.
* mesonpep517_:
  Implements PEP517_ for the meson build system.
* Ninja_:
  A small build system with a focus on speed.
* setuptools_:
  Python's packaging standard reference implementation.
* setuptools_scm_:
  Extracts Python package versions from git or hg metadata.
* Tomli_:
  Library for parsing TOML_ (pre-Python 3.11).  
* wheel_:
  Python's binary packaging standard reference implementation.

License
^^^^^^^

OZI is released under the terms of the 2.0 version of the Apache License,
approved by the Apache Software Foundation. OZI meets the Open Source Initiative's definition of
open source software, and the Free Software Foundation's definition of GPLv3-compatible open 
source software.

|osi-logo| |asf-logo| |fsf-logo|

.. note::
   The OSI logo trademark is the trademark of Open Source Initiative.
   The OZI project is not affiliated with or endorsed by the Open Source Initiative.

.. note::
   The Apache logo trademark is the trademark of the Apache Software Foundation.
   The OZI project is not affiliated with or endorsed by the Apache Software Foundation.

.. note::
   The FSF logo trademark is the trademark of the Free Software Foundation.
   The OZI project is not affiliated with or endorsed by the Free Software Foundation.



.. |py-version-badge| image:: https://img.shields.io/badge/Python%20Version-3.9%20%7C%203.10%20%7C%203.11-blue

.. |pylint-ckpt-badge| image:: https://img.shields.io/badge/linting-%E2%9C%94%20Pylint%3A%2010.00%2F10-informational

.. |slsa-level3-badge| image:: https://slsa.dev/images/gh-badge-level3.svg

.. |semantic-release-badge| image:: https://img.shields.io/badge/semantic--release-gitmoji-e10079?logo=semantic-release
    :target: https://github.com/python-semantic-release/python-semantic-release
    :alt: Automatic Semantic Versioning for Python projects
.. |bandit-badge| image:: https://img.shields.io/badge/security-%E2%9C%94%20bandit-yellow.svg
    :target: https://github.com/PyCQA/bandit
    :alt: Security Status

.. |pytest-plugins-badge| image:: https://img.shields.io/badge/Pytest-asyncio%20cov%20%20hypothesis%20mock%20randomly%20tcpclient-informational

.. |black-badge| image:: https://img.shields.io/badge/code%20style-%E2%9C%94%20black-000000.svg
    :target: https://github.com/psf/black

.. |flake8-badge| image:: https://img.shields.io/badge/code%20quality-%E2%9C%94%20Flake8-informational
.. |isort-badge| image:: https://img.shields.io/badge/%20imports-%E2%9C%94%20isort-%231674b1?style=flat&labelColor=ef8336
    :target: https://pycqa.github.io/isort/
.. |pyright-badge| image:: https://img.shields.io/badge/typing-%E2%9C%94%20Pyright%3A%200%20e%2C%200%20w%2C%200%20i-informational
.. |rst-lint-badge| image:: https://img.shields.io/badge/rst--lint-%E2%9C%94%20README.rst-informational

.. |coverage-badge| image:: https://img.shields.io/badge/Coverage.py-%E2%9C%94%20100%25-success

.. |osi-logo| image:: https://149753425.v2.pressablecdn.com/wp-content/uploads/2009/06/OSIApproved_100X125.png
 :height: 100
 :alt: OSI Approved Open Source License under Keyhole Logo
 :target: https://opensource.org/

.. |asf-logo| image:: https://www.apache.org/foundation/press/kit/asf_logo_url.png
 :height: 100
 :alt: Apache-2.0 License
 :target: https://www.apache.org/

.. |fsf-logo| image:: https://www.gnu.org/graphics/logo-fsf.org.png
 :width: 330
 :alt: GPL-compatible Open Source License
 :target: https://www.gnu.org/


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
