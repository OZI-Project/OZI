# ozi/scripts/lint/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
foreach package : lint_suite
    if package not in plugin_only
        subdir(package)
    endif
endforeach
