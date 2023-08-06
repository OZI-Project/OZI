"""API intended to be used to fulfill the OZI Standard Requirements."""
# Copyright 2023 Ross J. Duff MSc
# The copyright holder licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
# pylint: disable=unused-import
from datetime import date, timezone, datetime
import platform
from typing import Any, Final
from warnings import warn

try:
    import toml  # noqa: F401
except ImportError:
    import tomli as toml  # noqa: F401

from bandit.blacklists import utils
from bandit.core import issue


__pymajor, __pyminor, __pypatch = map(int, platform.python_version_tuple())

PYMAJOR: Final[int] = __pymajor
PYMINOR: Final[int] = __pyminor
PYPATCH: Final[int] = __pypatch

minor_deprecation = {
    9: date(2025, 10, 1),
    10: date(2026, 10, 1),
    11: date(2027, 10, 1),
    12: date(2028, 10, 1),
}
python3_eol = minor_deprecation.get(PYMINOR, date(2008, 12, 3))

if datetime.now(tz=timezone.utc).date() > python3_eol:  # pragma: no cover
    warn(
        f'Python {PYMAJOR}.{PYMINOR}.{PYPATCH} is not supported as of {python3_eol}.',
        RuntimeWarning,
    )

def gen_blacklist():
    """Generate a list of items to blacklist.

    Methods of this type, "bandit.blacklist" plugins, are used to build a list
    of items that bandit's built in blacklisting tests will use to trigger
    issues. They replace the older blacklist* test plugins and allow
    blacklisted items to have a unique bandit ID for filtering and profile
    usage.

    :return: a dictionary mapping node types to a list of blacklist data
    """
    sets = []
    sets.append(
        utils.build_conf_dict(
            "import_telnetlib",
            "B401",
            issue.Cwe.CLEARTEXT_TRANSMISSION,
            ["telnetlib"],
            "A telnet-related module is being imported.  Telnet is "
            "considered insecure. Use SSH or some other encrypted protocol.",
            "HIGH",
        )
    )


if __name__ == '__main__':
    project = Project()
    print(project.readme_rst())
    print(project.pkg_info_payload_readme())
    print(project.scm_payload_readme())
