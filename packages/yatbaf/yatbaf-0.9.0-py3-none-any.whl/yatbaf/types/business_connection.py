from __future__ import annotations

from typing import final

from .abc import TelegramType
from .user import User


@final
class BusinessConnection(TelegramType):
    """Describes the connection of the bot with a business account.

    See: https://core.telegram.org/bots/api#businessconnection
    """

    id: str
    """Unique identifier of the business connection."""

    user: User
    """Business account user that created the business connection."""

    user_chat_id: int
    """Identifier of a private chat with the user who created the business
    connection.
    """

    date: int
    """Date the connection was established in Unix time."""

    can_reply: bool
    """``True``, if the bot can act on behalf of the business account in chats
    that were active in the last 24 hours.
    """

    is_enabled: bool
    """``True``, if the connection is active."""
