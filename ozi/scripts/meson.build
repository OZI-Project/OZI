# ozi/scripts/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
config_files = [
    'get_optional_dependencies.py',
    'create_subproject_symlink.py',
    'scm_version_snip.py',
    'meson_setuptools_scm.py',
    'meson_dist_setuptools_scm.py',
    'meson_postconf_install_dependencies.py',
    'meson_postconf_install_depends_external.py',
    'version_metadata_template.py',
    'to_distribution_template.py',
]
foreach file: config_files
    if not meson.is_subproject() or get_option('install-subprojects').enabled()
        python.install_sources(file, subdir: 'ozi'/'scripts')
    endif
    fs.copyfile(file)
endforeach
if false
    executable('source_child_scripts', config_files)
endif
