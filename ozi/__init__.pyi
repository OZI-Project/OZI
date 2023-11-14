"""
Core OZI packaging management plane module.
"""

from importlib.metadata import version
from typing import Annotated, Dict, List, Tuple
from warnings import warn

from packaging.version import Version, parse

from .assets import (
    implementation_support,
    meson_min_version,
    metadata_version,
    python_support,
    specification_version,
)

metadata: Dict[Annotated[str, 'ozi'], Dict[str, str | List[str]]] = ...
def check_for_update(current_version: Version, releases: List[str]) -> None:
    """Issue a warning if installed version of OZI is not up to date."""
    ...

