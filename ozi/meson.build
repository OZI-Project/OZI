# ozi/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
source_files = [
    '__init__.py',
    '__main__.py',
    'tasks.py',
]
foreach file : files(source_files)
    fs.copyfile(file)
    if not meson.is_subproject() or get_option('install-subprojects').enabled()
        python.install_sources(file, pure: true, subdir: 'ozi')
    endif
endforeach
source_children = [
    'dist',
    'fix',
    'lint',
    'new',
    'scripts',
    'test',
    'patch'
]
foreach child: source_children
    subdir(child)
endforeach
