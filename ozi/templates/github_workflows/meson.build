# ozi/templates/github_workflows/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
workflows = [
    'checkpoint.yml.j2',
    'ozi.yml.j2',
    'publish.yml.j2',
    'pyc_wheel.yml.j2',
    'release.yml.j2',
    'semantic_release.yml.j2',
    'sigstore.yml.j2',
]
foreach file: workflows
    fs.copyfile(file)
    python.install_sources(file, subdir: 'ozi'/'templates'/'github_workflows')
endforeach
if false
    executable('source_files_child_templates_child_github_workflows', workflows)
endif