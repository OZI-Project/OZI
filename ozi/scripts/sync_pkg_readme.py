# noqa: INP001
# Copyright 2023 Ross J. Duff MSc
# The copyright holder licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""Check if the README.rst file is synchronized with PKG-INFO."""
import difflib
import email
import os
import pathlib
import sys
#
try:
    import toml  # noqa: F401
except ImportError:
    import tomli as toml  # noqa: F401
# pylint: disable=consider-using-with
source = pathlib.Path(
    os.path.relpath(
        os.path.join('/', os.environ.get('MESON_SOURCE_ROOT', os.path.relpath('..'))),
        '/'
    )
)
pkg_info_file = open('PKG-INFO', 'r', encoding='utf-8')
pkg_info = email.message_from_file(pkg_info_file).get_payload()
pkg_info_file.close()
readme_file = open('README.rst', 'r', encoding='utf-8')
readme = readme_file.read()
readme_file.close()
project_file = open('/'/source/'pyproject.toml', 'r', encoding='utf-8')
pyproject_toml = toml.loads(project_file.read())
project_file.close()
setuptools_scm = pyproject_toml.get('tool', {}).get('setuptools_scm', {})
write_to_template = email.message_from_string(
    setuptools_scm.get('write_to_template', '')).get_payload()
DIFF1 = str().join(
    difflib.context_diff(
        pkg_info,
        readme,
        tofile='PKG-INFO',
        fromfile='README.rst'
        )
    )
DIFF2 = str().join(
    difflib.context_diff(
        readme,
        write_to_template,
        tofile='pyproject.toml',
        fromfile='README.rst'
        )
    )
DIFF3 = str().join(
    difflib.context_diff(
        write_to_template,
        pkg_info,
        tofile='pyproject.toml',
        fromfile='PKG-INFO'
        )
    )
if DIFF1 != '':
    print(DIFF1)
    sys.exit(len(DIFF1))
elif DIFF2 != '':
    print(DIFF2)
    sys.exit(len(DIFF2))
elif DIFF3 != '':
    print(DIFF3)
    sys.exit(len(DIFF3))
