from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.types import ReactionType
    from yatbaf.typing import NoneBool


@final
class SetMessageReaction(TelegramMethod[bool]):
    """See: :meth:`~yatbaf.bot.Bot.set_message_reaction`."""

    chat_id: int | str
    message_id: int
    reaction: list[ReactionType] | None = None
    is_big: NoneBool = None
