# ozi/scripts/lint/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
source_child_lint_children = [
    'bandit',
    'black',
    'flake8',
    'isort',
    'mypy',
    'pyright',
    'readme-renderer',
]
if (get_option('dev').enabled() or get_option('lint').enabled())
    foreach package : source_child_lint_children
        message('configure', package, 'with', ' '.join(pip_compile))
        subdir(package)
    endforeach
endif
