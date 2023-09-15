# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
files = [
    'cc0-1.0.txt',
    'unlicense.txt',
]
foreach file: files
    fs.copyfile(file)
    python.install_sources(
        file, 
        subdir: 'ozi'/'templates'/'license'/fs.name(meson.current_source_dir()))
endforeach
