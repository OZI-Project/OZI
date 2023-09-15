# ozi/templates/license/OSI_Approved/SIL_Open_Font_License_1_1__OFL_1_1_/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
files = [
    'ofl-1.1.txt'
]
foreach file: files
    fs.copyfile(file)
    python.install_sources(
        file, 
        subdir: 'ozi'/'templates'/'license'/'OSI_Approved'/fs.name(meson.current_source_dir()))
endforeach
