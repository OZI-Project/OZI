# ozi/fix/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
config_files = [
    '__init__.py',
    '__main__.py',
    'parser.py',
]
foreach file: config_files
    python.install_sources(file, subdir: 'ozi'/'fix')
    fs.copyfile(file)
endforeach
if false
    executable('source_child_fix', config_files)
endif
