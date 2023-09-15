# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
files = [
    'gpl-2.0-only.txt',
    'gpl-2.0-or-later.txt',
    'gpl-3.0-only.txt',
    'gpl-3.0-or-later.txt',
]
foreach file: files
    fs.copyfile(file)
    python.install_sources(
        file, 
        subdir: 'ozi'/'templates'/'license'/'OSI_Approved'/fs.name(meson.current_source_dir()))
endforeach
