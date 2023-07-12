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

========
OZI lint
========

Codebase linting and formatting.

Default Toolchain
-----------------

* Bandit_:
  A tool designed to find common security issues in Python code.
* Black_:
  The uncompromising code formatter.
* Flake8_:
  A wrapper around PyFlakes_, pycodestyle_ and Ned Batchelder's McCabe_ script.
* Flake8-pyproject_:
  A wrapper around Flake8 to use pyproject.toml
* flake8-quotes_
* flake8-docstring-checker_
* flake8-pytest-style_
* flake8-type-checking_
* flake8-annotations_
* flake8-broken-line_
* flake8-eradicate_
* flake8-fixme_
* flake8-bugbear_
* flake8-datetimez_
* flake8-no-pep420_
* flake8-comprehensions_
* flake8-leading-blank-lines_
* flake8-tidy-imports_
* flake8-pyi_
* isort_:
  Sort imports alphabetically, and automatically separated into sections and by type. 
* Pylint_:
  A static code analyser for Python
* Pyright_:
  A full-featured, standards-based static type checker for Python.
* restructuredtext-lint_:
  Python Packaging Authority flavoured reST linting.

Standards
---------

* Universal
   * Maximum line width 93
   * ``pyproject.toml`` provides configuration
   * Exit successfully
* Excluding restructuredtext-lint
   * Target all sources and tests
* Bandit
   * Ignore nosec comments
* Black
   * skip string normalization (``-S``)
* Flake8
   * Maximum complexity of 5 (``--max-complexity=5``)
   * Respect noqa comments
      * C901: complexity <= 8
      * INP001: tests and scripts
   * Check PEP 8 - Style Guide for Python Code
   * Check PEP 287 - reStructuredText Docstring Format
   * Check PEP 484 - Type Hints
   * Check PEP 3107 - Function Annotations
   * Check annotations ANN001-ANN003, ANN101-ANN102, ANN201-ANN206
   * Check broken-line N400
   * Check bugbear B001-B033
   * Check comprehensions C400-C419
   * Check datetimez DTZ001-DTZ012
   * Check docstring-checker DC100-DC104
   * Check eradicate E800
   * Check fixme T100-T102
   * Check leading-blank-lines LBL001
   * Check no-pep420 INP001
   * Check pyi Y001-Y057
   * Check pytest-style PT001-PT027
   * Check quotes Q000-Q003
   * Check tidy-imports I250, I252
   * Check type-checking TC001-TC006

.. _Bandit: https://pypi.org/project/bandit/
.. _Black: https://pypi.org/project/black/
.. _Flake8: https://pypi.org/project/flake8
.. _Flake8-pyproject: https://pypi.org/project/Flake8-pyproject
.. _flake8-quotes: https://pypi.org/project/flake8-quotes/
.. _flake8-docstring-checker: https://pypi.org/project/flake8-docstring-checker/
.. _flake8-pytest-style: https://pypi.org/project/flake8-pytest-style/
.. _flake8-type-checking: https://pypi.org/project/flake8-type-checking/
.. _flake8-annotations: https://pypi.org/project/flake8-annotations/
.. _flake8-broken-line: https://pypi.org/project/flake8-broken-line/
.. _flake8-eradicate: https://pypi.org/project/flake8-eradicate/
.. _flake8-fixme: https://pypi.org/project/flake8-fixme/
.. _flake8-bugbear: https://pypi.org/project/flake8-bugbear/
.. _flake8-datetimez: https://pypi.org/project/flake8-datetimez/
.. _flake8-no-pep420: https://pypi.org/project/flake8-no-pep420/
.. _flake8-comprehensions: https://pypi.org/project/flake8-comprehensions/
.. _flake8-leading-blank-lines: https://pypi.org/project/flake8-leading-blank-lines/
.. _flake8-tidy-imports: https://pypi.org/project/flake8-tidy-imports/
.. _flake8-pyi: https://pypi.org/project/flake8-pyi/
.. _Pyflakes: https://pypi.org/project/pyflakes/
.. _pycodestyle: https://pypi.org/project/pycodestyle/
.. _McCabe: https://pypi.org/project/mccabe/
.. _isort: https://pypi.org/project/isort/
.. _Pylint: https://pypi.org/project/pylint/
.. _Pyright: https://pypi.org/project/pyright/
.. _restructuredtext-lint: https://pypi.org/project/restructuredtext-lint/