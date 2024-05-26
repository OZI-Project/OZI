# ozi/scripts/test/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
source_child_test_children = ['coverage', 'pytest']
if (get_option('dev').enabled() or get_option('test').enabled())
  foreach package : source_child_test_children
      message('configure', package, 'with pip-compile')
      subdir(package)
  endforeach
endif
