# ozi/vendor/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
python_files = [
    '__init__.py',
    '__main__.py',
    'deliverability.py',
    'exceptions_types.py',
    'py.typed',
    'rfc_constants.py',
    'syntax.py',
    'validate_email.py',
    'version.py',
]
foreach file : files(python_files)
    fs.copyfile(file)
    python.install_sources(file, pure: true, subdir: 'ozi' / 'vendor' / 'email_validator')
endforeach
if false
    executable('email_validator_files', python_files)
endif
