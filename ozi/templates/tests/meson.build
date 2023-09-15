# ozi/templates/tests/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
tests_templates = [
    'meson.build.j2',
    'new_test.py.j2',
]
foreach file: tests_templates
    fs.copyfile(file)
    python.install_sources(file, subdir: 'ozi'/'templates'/'tests')
endforeach