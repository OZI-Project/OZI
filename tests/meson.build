# tests/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
test_files = ['ozi_fix.py', 'ozi_new.py']
foreach file: test_files
  fs.copyfile(file)
  python.install_sources(file, subdir: 'ozi'/'tests')
endforeach
if false
  executable('test_files', test_files)
endif
children = []
foreach child: children
    subdir(child)
endforeach
if false
    executable('test_children', children)
endif