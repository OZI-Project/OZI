# ozi/templates/license/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
children = [
    'CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
    'DFSG approved',
    'Free To Use But Restricted',
    'OSI Approved',
    'Public Domain',
]
foreach child: children
    subdir(child.underscorify())
endforeach
if false
    executable('templates_license_children', children)
endif
