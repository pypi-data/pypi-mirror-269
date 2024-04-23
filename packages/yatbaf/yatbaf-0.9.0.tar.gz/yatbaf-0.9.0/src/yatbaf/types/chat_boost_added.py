from __future__ import annotations

from typing import final

from .abc import TelegramType


@final
class ChatBoostAdded(TelegramType):
    """This object represents a service message about a user boosting a chat.

    See: https://core.telegram.org/bots/api#chatboostadded
    """

    boost_count: int
    """Number of boosts added by the user."""
