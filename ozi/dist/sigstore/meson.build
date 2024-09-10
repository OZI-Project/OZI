# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
requirements = ['requirements.in']
extra_args = []
if pip_compile[0].endswith('uv')
    extra_args = ['--prerelease=allow']
endif
configure_file(
    input: requirements,
    output: 'requirements.txt',
    command: [pip_compile, get_option('config-args-sigstore'), extra_args, '-o', '@OUTPUT@', '@INPUT@']
)
