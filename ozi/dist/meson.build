# ozi/scripts/dist/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
source_child_dist_children = [
    'cibuildwheel',
    'semantic_release',
    'sigstore',
    'twine',
]
if (get_option('dev').enabled() or get_option('dist').enabled())
    foreach package : source_child_dist_children
        message('configure', package, 'with', ' '.join(pip_compile))
        subdir(package)
    endforeach
endif
