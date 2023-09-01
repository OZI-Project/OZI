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
required_forms = [
    'bandit.meson.options',
    'bandit.pyproject.toml',
    'black.meson.options',
    'black.pyproject.toml',
    'flake8.meson.options',
    'flake8.pyproject.toml',
    'isort.meson.options',
    'isort.pyproject.toml',
    'mypy.meson.options',
    'mypy.pyproject.toml',
    'project.array.meson.options',
    'project.feature.meson.options',
    'project.integer.meson.options',
    'project.meson.build',
    'project.PKG-INFO',
    'pyright.meson.options',
    'pytest.pyproject.toml',
    'semantic_release.pyproject.toml',
    'setuptools_scm.pyproject.toml',
    'tox.pyproject.toml',
]
foreach form: required_forms
    python.install_sources(form, subdir: 'ozi'/'templates'/'api'/'optional')
    fs.copyfile(form)
endforeach
