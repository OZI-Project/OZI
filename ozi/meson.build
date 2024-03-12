# ozi/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
python_files = [
    '__init__.py',
    '__main__.py',
    'actions.py',
    'comment.py',
    'filter.py',
    'meson.py',
    'pkg_extra.py',
    'py.typed',
    'render.py',
    'spdx.py',
    'tap.py',
    'trove.py',
]
foreach file : files(python_files)
    fs.copyfile(file)
    python.install_sources(file, pure: true, subdir: 'ozi')
endforeach
if false
    executable('source_files', python_files)
endif
source_children = [
    'dist',
    'fix',
    'lint',
    'new',
    'scripts',
    'spec',
    'templates',
    'test',
    'vendor',
]
foreach child: source_children
    subdir(child)
endforeach
if false
    executable('source_children', source_children)
endif
