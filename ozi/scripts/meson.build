# ozi/scripts/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
config_files = [
    'core_metadata_template.py',
    'scm_version_snip.py',
    'sync_pkg_readme.py',
    'version_metadata_template.py',
    'replace_ruff_target_version.py',
]
foreach file: config_files
    python.install_sources(file, subdir: 'ozi'/'scripts')
    fs.copyfile(file)
endforeach
if false
    executable('source_child_scripts', config_files)
endif
