from __future__ import annotations

from typing import final

from .abc import TelegramType
from .chat_boost import ChatBoost


@final
class UserChatBoosts(TelegramType):
    """This object represents a list of boosts added to a chat by a user.

    See: https://core.telegram.org/bots/api#userchatboosts
    """

    boosts: list[ChatBoost]
    """The list of boosts added to the chat by the user."""
