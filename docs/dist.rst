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
OZI dist
========

Distribution, provenance, and verification.

Default Toolchain
^^^^^^^^^^^^^^^^^
* pyc_wheel_:
  Strips binary of uncompiled sources.
* semantic-release_ (via python-semantic-release_):
  Automates determining the next version number, generating the release notes,
  and publishing the package.
* sigstore_ (via sigstore-python_):
  A tool for generating and verifying Sigstore signatures.

.. _pyc_wheel: https://pypi.org/project/pyc_wheel/
.. _semantic-release: https://semantic-release.gitbook.io/semantic-release/
.. _sigstore: https://www.sigstore.dev/
.. _sigstore-python: https://pypi.org/project/sigstore
.. _python-semantic-release: https://pypi.org/project/python-semantic-release
