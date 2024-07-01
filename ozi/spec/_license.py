# ozi/spec/_license.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""License specification constants."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

NOT_SUPPORTED = {
    'Aladdin Free Public License (AFPL)',  # nonreusable
    'Free For Educational Use',  # too broad
    'Free For Home Use',  # too broad
    'Free for non-commercial use',  # too broad
    'Freely Distributable',  # too broad
    'Freeware',  # too broad
    'GUST Font License 1.0',  # no licenseref
    'GUST Font License 2006-09-30',  # no licenseref
    'Netscape Public License (NPL)',  # nonreusable
    'Nokia Open Source License (NOKOS)',  # nonreusable
    'OSI Approved :: Attribution Assurance License',  # boilerplate
    'OSI Approved :: Common Development and Distribution License 1.0 (CDDL-1.0)',  # legacy
    'OSI Approved :: Common Public License',  # superseded
    'OSI Approved :: Historical Permission Notice and Disclaimer (HPND)',  # legacy
    'OSI Approved :: IBM Public License',  # superseded
    'OSI Approved :: Intel Open Source License',  # legacy
    'OSI Approved :: Jabber Open Source License',  # legacy
    'OSI Approved :: MITRE Collaborative Virtual Workspace License (CVW)',  # legacy
    'OSI Approved :: Motosoto License',  # nonreusable
    'OSI Approved :: European Union Public Licence 1.0 (EUPL 1.0)',  # superseded
    'OSI Approved :: Mozilla Public License 1.0 (MPL)',  # superseded
    'OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)',  # superseded
    'OSI Approved :: NASA Open Source Agreement v1.3 (NASA-1.3)',  # other
    'OSI Approved :: Nethack General Public License',  # nonreusable
    'OSI Approved :: Nokia Open Source License',  # nonreusable
    'OSI Approved :: Python License (CNRI Python License)',  # legacy
    'OSI Approved :: Python Software Foundation License',
    'OSI Approved :: Qt Public License (QPL)',  # nonreusable
    'OSI Approved :: Ricoh Source Code Public License',  # nonreusable
    'OSI Approved :: Sleepycat License',  # nonreusable
    'OSI Approved :: Sun Industry Standards Source License (SISSL)',  # legacy
    'OSI Approved :: Sun Public License',  # nonreusable
    'OSI Approved :: Vovida Software License 1.0',  # nonreusable
    'OSI Approved :: W3C License',  # nonreusable
    'OSI Approved :: X.Net License',  # legacy
    'OSI Approved :: Zope Public License',  # nonreusable
    'Repoze Public License',  # no licenseref
}

SPDX_LICENSE_MAP: dict[str, Sequence[str]] = {
    'Private': ('LicenseRef-Proprietary',),
    'CeCILL-B Free Software License Agreement (CECILL-B)': ('CECILL-B',),
    'CeCILL-C Free Software License Agreement (CECILL-C)': ('CECILL-C',),
    'OSI Approved :: MirOS License (MirOS)': ('MirOS',),
    'OSI Approved :: Open Group Test Suite License': ('OGTSL',),
    'OSI Approved :: Universal Permissive License': ('UPL-1.0',),
    'Eiffel Forum License (EFL)': ('EFL-2.0',),
    'DFSG approved': (
        'AGPL-3.0-only',
        'AGPL-3.0-or-later',
        'Apache-2.0',
        'Artistic-2.0',
        'BSD-3-Clause',
        'CC-BY-4.0',
        'CC-BY-SA-4.0',
        'EPL-1.0',
        'EFL-2.0',
        'GPL-2.0-only',
        'GPL-2.0-or-later',
        'GPL-3.0-only',
        'GPL-3.0-or-later',
        'ISC',
        'LGPL-2.1-or-later',
        'LGPL-3.0-only',
        'LGPL-3.0-or-later',
        'MIT',
        'OFL-1.1',
        'WTFPL',
        'Zlib',
    ),
    'OSI Approved': (
        '0BSD',
        'AFL-3.0',
        'AGPL-3.0-only',
        'AGPL-3.0-or-later',
        'APSL-1.0',
        'APSL-1.1',
        'APSL-1.2',
        'APSL-2.0',
        'Apache-2.0',
        'Artistic-2.0',
        'BSD-2-Clause',
        'BSD-3-Clause',
        'BSD-3-Clause-Clear',
        'BSD-4-Clause',
        'BSL-1.0',
        'CECILL-2.1',
        'EFL-2.0',
        'EPL-1.0',
        'EPL-2.0',
        'EUPL-1.1',
        'EUPL-1.2',
        'GFDL-1.3-only',
        'GFDL-1.3-or-later',
        'GPL-2.0-only',
        'GPL-2.0-or-later',
        'GPL-3.0-only',
        'GPL-3.0-or-later',
        'ISC',
        'LGPL-2.0-only',
        'LGPL-2.1-or-later',
        'LGPL-3.0-only',
        'LGPL-3.0-or-later',
        'MIT',
        'MIT-0',
        'MPL-2.0',
        'MirOS',
        'MulanPSL-2.0',
        'NCSA',
        'OFL-1.1',
        'OGTSL',
        'OSL-3.0',
        'PostgreSQL',
        'UPL-1.0',
        'Unlicense',
        'Zlib',
    ),
    'OSI Approved :: Academic Free License (AFL)': ('AFL-3.0',),
    'OSI Approved :: Apache Software License': ('Apache-2.0',),
    'OSI Approved :: Apple Public Source License': (
        'APSL-1.0',
        'APSL-1.1',
        'APSL-1.2',
        'APSL-2.0',
    ),
    'OSI Approved :: Artistic License': ('Artistic-2.0',),
    'OSI Approved :: BSD License': (
        '0BSD',
        'BSD-2-Clause',
        'BSD-3-Clause',
        'BSD-3-Clause-Clear',
        'BSD-4-Clause',
    ),
    'OSI Approved :: Boost Software License 1.0 (BSL-1.0)': ('BSL-1.0',),
    'OSI Approved :: CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)': (
        'CECILL-2.1',
    ),
    'OSI Approved :: Eclipse Public License 1.0 (EPL-1.0)': ('EPL-1.0',),
    'OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)': ('EPL-2.0',),
    'OSI Approved :: Eiffel Forum License': ('EFL-2.0',),
    'OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)': ('EUPL-1.1',),
    'OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)': ('EUPL-1.2',),
    'OSI Approved :: GNU Affero General Public License v3': (
        'AGPL-3.0-only',
        'AGPL-3.0-or-later',
    ),
    'OSI Approved :: GNU Free Documentation License (FDL)': (
        'GFDL-1.3-only',
        'GFDL-1.3-or-later',
    ),
    'OSI Approved :: GNU General Public License (GPL)': (
        'GPL-2.0-only',
        'GPL-2.0-or-later',
        'GPL-3.0-only',
        'GPL-3.0-or-later',
    ),
    'OSI Approved :: GNU General Public License v2 (GPLv2)': (
        'GPL-2.0-only',
        'GPL-2.0-or-later',
    ),
    'OSI Approved :: GNU General Public License v3 (GPLv3)': (
        'GPL-3.0-only',
        'GPL-3.0-or-later',
    ),
    'OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)': ('LGPL-2.0-only',),
    'OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)': (
        'LGPL-2.1-or-later',
    ),
    'OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)': (
        'LGPL-3.0-only',
        'LGPL-3.0-or-later',
    ),
    'OSI Approved :: GNU Library or Lesser General Public License (LGPL)': (
        'LGPL-2.1-or-later',
        'LGPL-3.0-only',
        'LGPL-3.0-or-later',
    ),
    'OSI Approved :: ISC License (ISCL)': ('ISC',),
    'OSI Approved :: MIT License': ('MIT', 'MIT-0'),
    'OSI Approved :: MIT No Attribution License (MIT-0)': ('MIT-0',),
    'OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)': ('MPL-2.0',),
    'OSI Approved :: Mulan Permissive Software License v2 (MulanPSL-2.0)': ('MulanPSL-2.0',),
    'OSI Approved :: Open Software License 3.0 (OSL-3.0)': ('OSL-3.0',),
    'OSI Approved :: PostgreSQL License': ('PostgreSQL',),
    'OSI Approved :: SIL Open Font License 1.1 (OFL-1.1)': ('OFL-1.1',),
    'OSI Approved :: University of Illinois/NCSA Open Source License': ('NCSA',),
    'OSI Approved :: Zero-Clause BSD (0BSD)': ('0BSD',),
    'OSI Approved :: The Unlicense (Unlicense)': ('Unlicense',),
    'OSI Approved :: zlib/libpng License': ('Zlib',),
    'Other/Proprietary License': ('LicenseRef-Proprietary',),
    'Public Domain': ('LicenseRef-Public-Domain', 'Unlicense', 'CC0-1.0'),
}
SPDX_LICENSE_EXCEPTIONS = (
    '389-exception',
    'Asterisk-exception',
    'Autoconf-exception-2.0',
    'Autoconf-exception-3.0',
    'Autoconf-exception-generic',
    'Autoconf-exception-macro',
    'Bison-exception-2.2',
    'Bootloader-exception',
    'Classpath-exception-2.0',
    'CLISP-exception-2.0',
    'cryptsetup-OpenSSL-exception',
    'DigiRule-FOSS-exception',
    'eCos-exception-2.0',
    'Fawkes-Runtime-exception',
    'FLTK-exception',
    'Font-exception-2.0',
    'freertos-exception-2.0',
    'GCC-exception-2.0',
    'GCC-exception-3.1',
    'GNAT-exception',
    'gnu-javamail-exception',
    'GPL-3.0-interface-exception',
    'GPL-3.0-linking-exception',
    'GPL-3.0-linking-source-exception',
    'GPL-CC-1.0',
    'GStreamer-exception-2005',
    'GStreamer-exception-2008',
    'i2p-gpl-java-exception',
    'KiCad-libraries-exception',
    'LGPL-3.0-linking-exception',
    'libpri-OpenH323-exception',
    'Libtool-exception',
    'Linux-syscall-note',
    'LLGPL',
    'LLVM-exception',
    'LZMA-exception',
    'mif-exception',
    'OCaml-LGPL-linking-exception',
    'OCCT-exception-1.0',
    'OpenJDK-assembly-exception-1.0',
    'openvpn-openssl-exception',
    'PS-or-PDF-font-exception-20170817',
    'QPL-1.0-INRIA-2004-exception',
    'Qt-GPL-exception-1.0',
    'Qt-LGPL-exception-1.1',
    'Qwt-exception-1.0',
    'SHL-2.0',
    'SHL-2.1',
    'SWI-exception',
    'Swift-exception',
    'u-boot-exception-2.0',
    'Universal-FOSS-exception-1.0',
    'vsftpd-openssl-exception',
    'WxWindows-exception-3.1',
    'x11vnc-openssl-exception',
)
