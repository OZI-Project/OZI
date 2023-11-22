# ozi/templates/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
root_templates = [
    '.gitignore.j2',
    'LICENSE.txt.j2',
    'PKG-INFO.j2',
    'README.rst.j2',
    'bandit.meson.options',
    'bandit.pyproject.toml',
    'black.meson.options',
    'black.pyproject.toml',
    'CHANGELOG.md.j2',
    'coverage.pyproject.toml',
    'doc8.meson.options',
    'doc8.pyproject.toml',
    'flake8.meson.options',
    'flake8.pyproject.toml',
    'isort.meson.options',
    'isort.pyproject.toml',
    'meson.build.j2',
    'meson.options.j2',
    'mypy.meson.options',
    'mypy.pyproject.toml',
    'new_child.j2',
    'ozi.wrap.j2',
    'project.ozi.wrap.j2',
    'project.PKG-INFO',
    'project.array.meson.options',
    'project.feature.meson.options',
    'project.integer.meson.options',
    'project.meson.build',
    'pydocstyle.meson.options',
    'pylint.pyproject.toml',
    'pyproject.toml.j2',
    'pyright.meson.options',
    'pyright.pyproject.toml',
    'pytest.pyproject.toml',
    'requirements.in.j2',
    'root.pyproject.toml',
    'ruff.pyproject.toml',
    'semantic_release.pyproject.toml',
    'setuptools_scm.pyproject.toml',
    'tox.pyproject.toml',
]
foreach file: root_templates
    fs.copyfile(file)
    python.install_sources(file, subdir: 'ozi'/'templates')
endforeach
if false
    executable('source_child_templates', root_templates)
endif
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
    executable('source_child_templates_children', children)
endif
