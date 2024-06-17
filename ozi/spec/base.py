# ozi/spec/base.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Base dataclasses for OZI Metadata."""
from __future__ import annotations

import reprlib
from dataclasses import MISSING
from dataclasses import Field
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import fields
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar
from typing import Iterator
from typing import Protocol
from typing import TypeAlias
from typing import TypeVar

if TYPE_CHECKING:
    import sys
    from collections.abc import Callable
    from collections.abc import Mapping

    VT = TypeVar('VT', str, int, float, None)
    _Val: TypeAlias = list['_Key[VT]'] | Mapping['_Key[VT]', VT] | VT
    _Key: TypeAlias = VT | _Val[VT]
    _Lambda: TypeAlias = Callable[[], '_FactoryMethod']
    _FactoryMethod: TypeAlias = Callable[[], _Lambda]

    if sys.version_info >= (3, 11):
        from typing import Self
    elif sys.version_info < (3, 11):
        from typing_extensions import Self


class _FactoryDataclass(Protocol):
    """A dataclass that, when called, returns a factory method."""

    __dataclass_fields__: ClassVar[dict[str, _Val[Any]]]

    def asdict(self: Self) -> dict[str, _Val[str]]: ...

    def __call__(self: Self) -> _FactoryMethod: ...


@dataclass(frozen=True, repr=False)
class Default(_FactoryDataclass):
    """A dataclass that, when called, returns it's own default factory field."""

    def __call__(self: Self) -> _FactoryMethod:  # pragma: defer to python
        return Field(
            default=MISSING,
            default_factory=self,  # type: ignore
            init=True,
            repr=True,
            hash=None,
            compare=True,
            metadata={'help': str(self.__class__.__doc__).replace('\n   ', '')},
            kw_only=MISSING,  # type: ignore
        )

    def __iter__(self: Self) -> Iterator[tuple[str, _Val[Any]]]:
        for f in fields(self):
            if f.repr:  # pragma: no cover
                yield (
                    f.name,
                    (
                        getattr(self, f.name)
                        if not isinstance(getattr(self, f.name), Default)
                        else getattr(self, f.name).asdict()
                    ),
                )

    def asdict(self: Self) -> dict[str, _Val[str]]:
        """Return a dictionary of all fields where repr=True.
        Hide a variable from the dict by setting repr to False and using
        a Default subclass as the default_factory.
        Typing is compatible with JSON and Jinja2 global namespace.

        .. seealso::

           :std:ref:`jinja2:global-namespace`
        """
        return dict(iter(self)) | {
            'help': str(self.__class__.__doc__).replace('\n   ', ''),
        }

    def __repr__(self: Self) -> str:
        return reprlib.repr(self)

    def __len__(self: Self) -> int:  # pragma: defer to python
        return len(list(iter(asdict(self))))
