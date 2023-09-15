# ozi/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
python_files = ['__init__.py', '__main__.py', 'fix.py', 'new.py']
foreach file : files(python_files)
    fs.copyfile(file)
    python.install_sources(file, pure: true, subdir: 'ozi')
endforeach
if false
    executable('source_files', python_files)
endif
children = ['assets', 'templates', 'scripts']
foreach child: children
    subdir(child)
endforeach
if false
    executable('source_children', children)
endif