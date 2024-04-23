from __future__ import annotations

from typing import TYPE_CHECKING

from .base import BaseFilter

if TYPE_CHECKING:
    from yatbaf.types import CallbackQuery
    from yatbaf.typing import FilterPriority


class Data(BaseFilter):
    """CallbackQuery data filter."""

    __slots__ = ("data",)

    def __init__(self, data: str) -> None:
        self.data = data

    @property
    def priority(self) -> FilterPriority:
        return {"content": (1, 100)}

    async def check(self, q: CallbackQuery) -> bool:
        return (d := q.data) is not None and d == self.data
