# ozi/new/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
config_files = [
    '__init__.py',
    '__main__.py',
    'interactive.py',
    'parser.py',
    'validate.py',
]
foreach file: config_files
    if not meson.is_subproject() or get_option('install-subprojects').enabled()
        python.install_sources(file, subdir: 'ozi'/'new')
    endif
    fs.copyfile(file)
endforeach
if false
    executable('source_child_new', config_files)
endif
