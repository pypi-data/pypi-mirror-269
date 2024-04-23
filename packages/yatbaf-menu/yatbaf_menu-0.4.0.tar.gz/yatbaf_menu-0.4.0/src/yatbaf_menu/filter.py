from __future__ import annotations

__all__ = ("CallbackPayload",)

from typing import TYPE_CHECKING
from typing import final

from yatbaf.filters import BaseFilter

if TYPE_CHECKING:
    from yatbaf.types import CallbackQuery
    from yatbaf.typing import FilterPriority


@final
class CallbackPayload(BaseFilter):
    __slots__ = ("payload",)

    def __init__(self, payload: str) -> None:
        self.payload = payload

    @property
    def priority(self) -> FilterPriority:
        return {"content": (1, 100)}

    async def check(self, q: CallbackQuery) -> bool:
        return q.data[:8] == self.payload  # type: ignore[index]


@final
class MenuVersion(BaseFilter):
    __slots__ = ("version",)

    def __init__(self, version: str) -> None:
        self.version = version

    @property
    def priority(self) -> FilterPriority:
        return {"content": (1, 100)}

    async def check(self, q: CallbackQuery) -> bool:
        # aa[00]bbcc
        return q.data[2:4] == self.version  # type: ignore[index]


@final
class MenuPrefix(BaseFilter):
    __slots__ = ("prefix",)

    def __init__(self, prefix: str) -> None:
        self.prefix = prefix

    @property
    def priority(self) -> FilterPriority:
        return {"content": (1, 100)}

    async def check(self, q: CallbackQuery) -> bool:
        # aa00[bb]cc
        return q.data[4:6] == self.prefix  # type: ignore[index]


@final
class RootMenuPrefix(BaseFilter):
    __slots__ = ("prefix",)

    def __init__(self, prefix: str) -> None:
        self.prefix = prefix

    @property
    def priority(self) -> FilterPriority:
        return {"content": (1, 100)}

    async def check(self, q: CallbackQuery) -> bool:
        # [aa]00bbcc
        return (d := q.data) is not None and d[:2] == self.prefix


RootMenuPrefix.incompat(MenuPrefix)


@final
class HasMessage(BaseFilter):
    __slots__ = ()

    @property
    def priority(self) -> FilterPriority:
        return {"content": (1, 100)}

    async def check(self, q: CallbackQuery) -> bool:
        return q.message is not None and q.message.date != 0
