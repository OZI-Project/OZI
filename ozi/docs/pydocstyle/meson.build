# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
custom_target(
    'requirements-pydocstyle',
    input: 'requirements.in',
    output: 'requirements.txt',
    build_always_stale: true,
    build_by_default: true,
    command: ['pip-compile', '-q', '--strip-extras', '--allow-unsafe',  '--generate-hashes', '-o', '@OUTPUT@', '@INPUT@']
)