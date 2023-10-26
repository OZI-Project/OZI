# ozi/assets/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
python_files = files('__init__.py', 'structure.py')
foreach file : python_files
    fs.copyfile(file)
    python.install_sources(file, subdir: 'ozi'/'assets')
endforeach
if false
    executable('source_child_assets', python_files)
endif