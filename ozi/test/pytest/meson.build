# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
configure_file(
    input: ['requirements.txt', 'extra/backports/requirements.txt'],
    output: 'requirements.txt',
    command: [find_program('cat'), '@INPUT@'],
    capture: true,
)
