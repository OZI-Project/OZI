# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
requirements = ['requirements.in']
nodejs = find_program('node', version: '>12', required: false)
if not nodejs.found()
    warning(
        'node version',
        '>12',
        'required by pyright version',
        '>=1.1.352',
        'not found'
    )
endif
if nodejs.version().version_compare('<=20') and nodejs.version().version_compare('!=18')
    warning('node version', nodejs.version(), 'is deprecated')
endif
configure_file(
    input: requirements,
    output: 'requirements.txt',
    command: ['pip-compile', '-q', '--strip-extras', '--allow-unsafe',  '--generate-hashes', '-o', '@OUTPUT@', '@INPUT@']
)
