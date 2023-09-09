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
root_templates = [
    '.gitignore.j2',
    'LICENSE.txt.j2',
    'NOTICE.j2',
    'PKG-INFO.j2',
    'README.rst.j2',
    'meson.build.j2',
    'meson.options.j2',
    'pyproject.toml.j2',
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
    'pyright.pyproject.toml',
    'pytest.pyproject.toml',
    'semantic_release.pyproject.toml',
    'setuptools_scm.pyproject.toml',
    'tox.pyproject.toml',
    'doc8.meson.options',
    'doc8.pyproject.toml',
    'pydocstyle.meson.options',
    'pylint.pyproject.toml',
]
foreach file: root_templates
    fs.copyfile(file)
    python.install_sources(file, subdir: 'ozi'/'templates')
endforeach
children = [
    'project.name',
    'github_workflows',
    'license',
    'tests',
]
foreach child: children
    subdir(child)
endforeach
if false
    executable('templates_children', children)
endif
