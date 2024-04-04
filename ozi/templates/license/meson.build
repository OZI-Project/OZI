# ozi/templates/license/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
files = [
    'agpl-3.0.txt',
    'apache-2.0.txt',
    'artistic-2.0.txt',
    'bsd-3-clause.txt',
    'cc0-1.0.txt',
    'epl-1.0.txt',
    'gfdl-1.3.txt',
    'gpl-2.0.txt',
    'gpl-3.0.txt',
    'isc.txt',
    'lgpl-2.0.txt',
    'lgpl-2.1.txt',
    'lgpl-3.0.txt',
    'mit.txt',
    'ofl-1.1.txt',
    'zlib.txt',
]
foreach file : files
    fs.copyfile(file)
    if not meson.is_subproject() or get_option('install-subprojects').enabled()
        python.install_sources(
            file,
            subdir: 'ozi' / 'templates' / 'license',
        )
    endif
endforeach
children = [
    'CC0_1_0_Universal__CC0_1_0__Public_Domain_Dedication',
    'DFSG_approved',
    'Free_To_Use_But_Restricted',
    'OSI_Approved',
    'Public_Domain',
]
foreach child : children
    subdir(child.underscorify())
endforeach
if false
    executable('templates_license_children', children)
endif
