from __future__ import annotations

__all__ = (
    "Chat",
    "ChatId",
    "private",
    "group",
    "channel",
)

from typing import TYPE_CHECKING
from typing import TypeAlias
from typing import final

from yatbaf.enums import ChatType

from .base import BaseFilter

if TYPE_CHECKING:
    from yatbaf.types import ChatBoostRemoved
    from yatbaf.types import ChatBoostUpdated
    from yatbaf.types import ChatJoinRequest
    from yatbaf.types import ChatMemberUpdated
    from yatbaf.types import Message
    from yatbaf.typing import FilterPriority

Update: TypeAlias = (
    "ChatBoostRemoved "
    "| ChatBoostUpdated"
    "| ChatJoinRequest"
    "| ChatMemberUpdated "
    "| Message "
)


@final
class Chat(BaseFilter):
    """Chat type filter."""

    __slots__ = (
        "types",
        "_priority",
    )

    def __init__(self, *types: ChatType | str, priority: int = 100) -> None:
        if not types:
            raise ValueError("You must pass at least one type.")
        self.types = frozenset([ChatType(t) for t in types])
        self._priority = priority

    @property
    def priority(self) -> FilterPriority:
        return {"chat": (len(self.types), self._priority)}

    async def check(self, update: Update) -> bool:
        return update.chat.type in self.types


private = Chat("private")
group = Chat("group")
channel = Chat("channel")


@final
class ChatId(BaseFilter):
    """Chat id filter."""

    __slots__ = (
        "ids",
        "_priority",
    )

    def __init__(self, *ids: int, priority: int = 150) -> None:
        if not ids:
            raise ValueError("You must pass at least one id.")
        self.ids = frozenset(ids)
        self._priority = priority

    @property
    def priority(self) -> FilterPriority:
        return {"chat": (len(self.ids), self._priority)}

    async def check(self, update: Update) -> bool:
        return update.chat.id in self.ids
