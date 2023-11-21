from __future__ import annotations

import hashlib
import re
from datetime import datetime
from datetime import timezone
from functools import lru_cache
from importlib.metadata import packages_distributions

import requests
from packaging.version import parse


def current_date(_format: str) -> str:
    """Filter to get the local date given format."""
    return datetime.now(tz=timezone.utc).date().strftime(_format)


@lru_cache
def underscorify(s: str) -> str:
    """Filter to replace non-alphanumerics with underscores."""
    return re.sub('[^0-9a-zA-Z]', '_', s)


@lru_cache
def wheel_repr(version: str) -> str:
    """Filter to transform versions of the form "X.Y" into "pyXY"."""
    major, minor = version.split('.')
    return f'py{major}{minor}'


@lru_cache
def sha256sum(version: str) -> str:  # pragma: no cover
    """Filter to transform OZI source version into a hash of the tarball.
    :param version: Version of OZI to get a hash for.
    :returns:
    """
    response = requests.get('https://pypi.org/pypi/OZI/json', timeout=30)
    match response.status_code:
        case 200:
            releases = response.json()['releases']
            latest_version = max(map(parse, releases.keys()))
            return str(
                [i for i in releases[latest_version] if i['filename'].endswith('.tar.gz')][
                    0
                ],
            )
        case _:
            checksum = hashlib.sha256()
            chunksize = 128 * 512
            response = requests.get(
                f'https://github.com/rjdbcm/OZI/archive/refs/tags/{version}.tar.gz',
                allow_redirects=True,
                stream=True,
                timeout=30,
            )
            for chunk in response.iter_content(chunksize):
                checksum.update(chunk)
            return checksum.hexdigest()


@lru_cache
def to_distribution(package: str) -> str | None:
    """Returns the first distributed module name for a package."""
    distributions = {v[0]: k for k, v in packages_distributions().items()}
    return distributions.get(package, None)
