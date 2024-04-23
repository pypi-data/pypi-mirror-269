from __future__ import annotations

from typing import final

from .abc import TelegramType
from .chat_boost_source import ChatBoostSource


@final
class ChatBoost(TelegramType):
    """This object contains information about a chat boost.

    See: https://core.telegram.org/bots/api#chatboost
    """

    boost_id: str
    """Unique identifier of the boost."""

    add_date: int
    """Point in time (Unix timestamp) when the chat was boosted."""

    expiration_date: int
    """Point in time (Unix timestamp) when the boost will automatically expire,
    unless the booster's Telegram Premium subscription is prolonged.
    """

    source: ChatBoostSource
    """Source of the added boost."""
