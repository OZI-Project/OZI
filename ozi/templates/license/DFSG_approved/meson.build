# Copyright 2023 Ross J. Duff MSc
# The copyright holder licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
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
