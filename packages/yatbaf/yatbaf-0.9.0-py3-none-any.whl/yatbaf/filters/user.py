from __future__ import annotations

__all__ = ("User",)

from typing import TYPE_CHECKING
from typing import final

from .base import BaseFilter

if TYPE_CHECKING:
    from yatbaf.types import Message
    from yatbaf.typing import FilterPriority


@final
class User(BaseFilter):
    """User filter.

    Use it to filter message coming from a specific user::

        @on_message(filters=[User("user")])
        async def handler(message: Message) -> None:
            ...
    """

    __slots__ = (
        "users",
        "_priority",
    )

    def __init__(self, *users: str | int, priority: int = 100) -> None:
        """
        :param users: Public username (with or without `@`) or user id.
        :param priority: *Optional.* Filter priority.
        """
        self.users = frozenset([
            u.lower().removeprefix("@") if isinstance(u, str) else u
            for u in users
        ])
        self._priority = priority

    @property
    def priority(self) -> FilterPriority:
        return {"sender": (len(self.users), self._priority)}

    async def check(self, update: Message) -> bool:
        return (u := update.from_) is not None and (
            u.id in self.users or
            (u.username is not None and u.username.lower() in self.users)
        )
