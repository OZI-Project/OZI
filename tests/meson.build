# tests/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
test_files = [
    'test_ozi_fix.py',
    'test_ozi_new.py',
    'test_tap.py',
]
foreach file: test_files
  fs.copyfile(file)
  if not meson.is_subproject() or get_option('install-subprojects').enabled()
    python.install_sources(file, subdir: 'ozi'/'tests')
  endif
endforeach
test_children = []
foreach child: test_children
    subdir(child)
endforeach