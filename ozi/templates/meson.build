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
    'meson.build.j2',
    'meson.options.j2',
    'PKG-INFO.j2',
    'pyproject.toml.j2',
    'README.rst.j2',
]
foreach file: root_templates
    fs.copyfile(file)
    python.install_sources(file)
endforeach
subdir('project.name')
subdir('api/required')
subdir('api/optional')
subdir('github_workflows')