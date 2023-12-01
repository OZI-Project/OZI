# ozi/templates/license/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
children = [
    'CC0_1_0_Universal__CC0_1_0__Public_Domain_Dedication',
    'DFSG_approved',
    'Free_To_Use_But_Restricted',
    'OSI_Approved',
    'Public_Domain',
]
foreach child: children
    subdir(child.underscorify())
endforeach
if false
    executable('templates_license_children', children)
endif
