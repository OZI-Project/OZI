# ozi/patch/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
patch_files = [
    'meson.build-fallback_version_for_ozi_build_1.13.0-1.38.0.patch',
    'pyproject.toml-set_tox_envname_enabled_for_meson_1.8.0-1.39.2.patch',
]
foreach file: patch_files
    if not meson.is_subproject() or get_option('install-subprojects').enabled()
        python.install_sources(file, subdir: 'ozi'/'patch')
    endif
    fs.copyfile(file)
    if meson.project_version().version_compare('<'+file.split('-')[2]) and meson.is_subproject()
        run_command(patch, '-Nmlu', '--no-backup-if-mismatch', meson.global_source_root() / file.split('-')[0], file, check: false)
    endif
endforeach
if false
    executable('source_child_patch', patch_files)
endif
