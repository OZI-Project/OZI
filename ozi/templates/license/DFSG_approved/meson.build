# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
files = [
    'agpl-3.0-only.txt',
    'agpl-3.0-or-later.txt',
    'apache-2.0.txt',
    'artistic-2.0.txt',
    'cc-by-4.0.txt',
    'cc-by-sa-4.0.txt',
    'epl-1.0.txt',
    'gpl-2.0-only.txt',
    'gpl-2.0-or-later.txt',
    'gpl-3.0-only.txt',
    'gpl-3.0-or-later.txt',
    'isc.txt',
    'lgpl-2.0-only.txt',
    'lgpl-2.0-or-later.txt',
    'lgpl-2.1-or-later.txt',
    'lgpl-3.0-only.txt',
    'lgpl-3.0-or-later.txt',
    'mit.txt',
    'ofl-1.1.txt',
    'wtfpl.txt',
    'zlib.txt',
]
foreach file: files
    fs.copyfile(file)
    python.install_sources(
        file, 
        subdir: 'ozi'/'templates'/'license'/fs.name(meson.current_source_dir()))
endforeach
