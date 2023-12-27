# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
requirements = ['requirements.in']
configure_file(
    input: requirements,
    output: 'requirements.txt',
    command: ['pip-compile', '-q', '--strip-extras', '--allow-unsafe',  '--generate-hashes', '-o', '@OUTPUT@', '@INPUT@']
)
