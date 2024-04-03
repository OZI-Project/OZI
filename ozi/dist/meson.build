# ozi/scripts/dist/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
source_child_dist_children = [
    'semantic_release',
    'sigstore'
]
if (get_option('dev').enabled() or get_option('dist').enabled())
    foreach package : source_child_dist_children
        message('configuring', package)
        subdir(package)
    endforeach
endif