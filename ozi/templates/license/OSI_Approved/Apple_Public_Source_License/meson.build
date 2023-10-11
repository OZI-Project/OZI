# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
files = [
    'apsl-1.0.txt',
    'apsl-1.1.txt',
    'apsl-1.2.txt',
    'apsl-2.0.txt',
]
foreach file: files
    fs.copyfile(file)
    python.install_sources(
        file, 
        subdir: 'ozi'/'templates'/'license'/'OSI_Approved'/fs.name(meson.current_source_dir()))
endforeach
