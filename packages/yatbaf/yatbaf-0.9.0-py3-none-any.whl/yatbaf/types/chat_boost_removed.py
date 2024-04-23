from __future__ import annotations

from typing import final

from .abc import TelegramType
from .chat import Chat
from .chat_boost_source import ChatBoostSource


@final
class ChatBoostRemoved(TelegramType):
    """This object represents a boost removed from a chat.

    See: https://core.telegram.org/bots/api#chatboostremoved
    """

    chat: Chat
    """Chat which was boosted."""

    boost_id: str
    """Unique identifier of the boost."""

    remove_date: int
    """Point in time (Unix timestamp) when the boost was removed."""

    source: ChatBoostSource
    """Source of the removed boost."""
