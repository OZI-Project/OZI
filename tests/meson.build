# tests/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
config_files = []
foreach file: config_files
  fs.copyfile(file)
  python.install_sources(file, subdir: 'ozi'/'tests')
endforeach
if false
  executable('test_files', config_files)
endif
children = []
foreach child: children
    subdir(child)
endforeach
if false
    executable('test_children', children)
endif