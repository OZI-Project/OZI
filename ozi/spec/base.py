# ozi/spec/base.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Base dataclasses for OZI Metadata."""
from __future__ import annotations

import reprlib
from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Protocol
from typing import TypeAlias

if TYPE_CHECKING:
    import sys
    from collections.abc import Callable
    from collections.abc import Mapping

    _VT: TypeAlias = list['_KT'] | Mapping[str, '_KT']
    _KT: TypeAlias = str | int | float | None | _VT
    _Lambda: TypeAlias = Callable[[], '_FactoryMethod']
    _FactoryMethod: TypeAlias = Callable[[], _Lambda]

    if sys.version_info >= (3, 11):
        from typing import Self
    elif sys.version_info < (3, 11):
        from typing_extensions import Self

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from dataclasses import fields


class _FactoryDataclass(Protocol):
    """A dataclass that, when called, returns a factory method."""

    __dataclass_fields__: ClassVar[dict[str, _VT]]

    def asdict(self: Self) -> dict[str, _VT]: ...

    def __call__(self: Self) -> _FactoryMethod: ...


@dataclass(frozen=True, repr=False)
class Default(_FactoryDataclass):
    """A dataclass that, when called, returns it's own default factory method."""

    def __call__(self: Self) -> _FactoryMethod:  # pragma: defer to python
        return field(default_factory=lambda: self())

    def asdict(self: Self) -> dict[str, _VT]:
        """Return a dictionary of all fields where repr=True.
        Hide a variable from the dict by setting repr to False and using
        a Default subclass as the default_factory.
        Typing is compatible with Jinja2 Environment and JSON.
        """
        all_fields = (
            (
                f.name,
                (
                    getattr(self, f.name)
                    if not isinstance(getattr(self, f.name), Default)
                    else getattr(self, f.name).asdict()
                ),
            )
            for f in fields(self)
            if f.repr
        )

        return dict(all_fields) | {
            'help': str(self.__class__.__doc__).replace('\n   ', ''),
        }

    def __repr__(self: Self) -> str:
        return reprlib.repr(self)

    def __len__(self: Self) -> int:  # pragma: defer to python
        return len(list(iter(asdict(self))))
