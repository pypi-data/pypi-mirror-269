from __future__ import annotations

from typing import final

from .abc import TelegramType
from .chat import Chat
from .chat_boost import ChatBoost


@final
class ChatBoostUpdated(TelegramType):
    """This object represents a boost added to a chat or changed.

    See: https://core.telegram.org/bots/api#chatboostupdated
    """

    chat: Chat
    """Chat which was boosted."""

    boost: ChatBoost
    """Infomation about the chat boost."""
