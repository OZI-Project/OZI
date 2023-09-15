# ozi/templates/github_workflows/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
workflows = [
    'ozi.yml',
    'sigstore.yml',
    'semantic_release.yml',
    'release.yml.j2',
    'publish.yml.j2',
    'ozi.yml.j2',
    'checkpoint.yml.j2',
]
foreach file: workflows
    fs.copyfile(file)
    python.install_sources(file, subdir: 'ozi'/'templates'/'github_workflows')
endforeach