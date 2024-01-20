.. OZI
  Classifier: License-Expression :: Apache-2.0 WITH LLVM-exception
  Classifier: License-File :: LICENSE.txt

.. README.rst
   Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
   See LICENSE.txt for license information.


===
OZI
===

|py-version-badge| |openssf-badge| |slsa-level3-badge| |fossa-badge| |semantic-release-badge|
|bandit-badge| |black-badge| |isort-badge| |flake8-badge| |pyright-badge|

.. image:: https://raw.githubusercontent.com/sigstore/community/main/artwork/badge/sigstore_codesigned_purple.png
 :align: right
 :height: 140
 :target: https://www.sigstore.dev/

Project Information
-------------------

OZI is a set of publishing tools for creating and maintaining pure Python packages.
See the `documentation <https://docs.oziproject.dev/>`_ for the project roadmap,
API specification, Meson version support, and other project information.

Purpose
^^^^^^^

What OZI is
###########

* Checkpointed Python packaging for Meson projects focused on pure Python sources.

OZI is meant for Python developers as a standardized and opinionated
Python packaging style guide and checkpointing API using the Meson build system.

The OZI continuous integration strategy consists of:

1. The following checkpointed environments:

* code testing and coverage
* distributing Python packages with Meson_
* code linting and formatting

2. Release drafting
3. Publishing

What OZI is **not**
###################

* A replacement for test environment managers like tox_, as a matter of fact OZI uses ``tox``.
* A replacement for git hook package management tools like pre-commit_

Message from the Maintainer
###########################

I just wanted packaging to work without having to reorient myself to best practices every time. 
This is a solution to help me package Python modules with Meson.
OZI can also help to synchronize packaging practices across packages using it, helping to reduce maintenance time.

Contributing
############

See the project `CONTRIBUTING.md <https://github.com/rjdbcm/OZI/blob/main/.github/CONTRIBUTING.md>`_

License
^^^^^^^

OZI is released under the terms of the 2.0 version of the Apache License,
approved by the Apache Software Foundation.
As of 13-Sept-2023 the OZI project has adopted the language of the LLVM-exception
to mitigate GPLv2 compatibility issues and reduce publishing clutter.
OZI meets the Open Source Initiative's definition of
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

.. note::
   The "LLVM" software name is the registered trademark of the LLVM Foundation.
   The OZI project is not affiliated with or endorsed by the LLVM Foundation.

Contact
-------

Ross J. Duff MSc - help@oziproject.dev

.. |py-version-badge| image:: https://img.shields.io/pypi/pyversions/ozi
    :alt: PyPI - Python Version
.. |pylint-ckpt-badge| image:: https://img.shields.io/badge/linting-%E2%9C%94%20Pylint%3A%2010.00%2F10-informational
.. |fossa-badge| image:: https://app.fossa.com/api/projects/git%2Bgithub.com%2Frjdbcm%2Fozi.svg?type=shield
    :target: https://app.fossa.com/projects/git%2Bgithub.com%2Frjdbcm%2Fozi?ref=badge_large
    :alt: License Compliance

.. |slsa-level3-badge| image:: https://slsa.dev/images/gh-badge-level3.svg
.. |openssf-badge| image:: https://bestpractices.coreinfrastructure.org/projects/7515/badge
    :target: https://bestpractices.coreinfrastructure.org/projects/7515
    :alt: Open Source Security Foundation self-certification status
.. |semantic-release-badge| image:: https://img.shields.io/badge/semantic--release-gitmoji-e10079?logo=semantic-release
    :target: https://github.com/python-semantic-release/python-semantic-release
    :alt: Automatic Semantic Versioning for Python projects
.. |bandit-badge| image:: https://img.shields.io/badge/security-%E2%9C%94%20bandit-yellow.svg
    :target: https://github.com/PyCQA/bandit
    :alt: Security Status
.. |black-badge| image:: https://img.shields.io/badge/code%20style-%E2%9C%94%20black-000000.svg
    :target: https://github.com/psf/black
    :alt: The Uncompromising Code Formatter
.. |flake8-badge| image:: https://img.shields.io/badge/code%20quality-%E2%9C%94%20Flake8-informational
.. |isort-badge| image:: https://img.shields.io/badge/%20imports-%E2%9C%94%20isort-%231674b1?style=flat&labelColor=ef8336
    :target: https://pycqa.github.io/isort/
    :alt: isort your imports, so you don't have to.
.. |pyright-badge| image:: https://img.shields.io/badge/typing-%E2%9C%94%20Pyright%3A%200%20e%2C%200%20w%2C%200%20i-informational

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
