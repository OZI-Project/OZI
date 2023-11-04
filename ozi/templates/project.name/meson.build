# ozi/templates/project.name/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
source_templates = [
    '__init__.pyi.j2',
    '__init__.py.j2',
    'meson.build.j2',
    'py.typed.j2',
    'new_module.py.j2',
]
foreach file: source_templates
    fs.copyfile(file)
    python.install_sources(file, subdir: 'ozi'/'templates'/'project.name')
endforeach
