from __future__ import annotations

from typing import final

from .abc import TelegramType
from .chat import Chat
from .reaction_count import ReactionCount


@final
class MessageReactionCountUpdated(TelegramType):
    """This object represents reaction changes on a message with anonymous
    reactions.

    See: https://core.telegram.org/bots/api#messagereactioncountupdated
    """

    chat: Chat
    """The chat containing the message."""

    message_id: int
    """Unique message identifier inside the chat."""

    date: int
    """Date of the change in Unix time."""

    reactions: list[ReactionCount]
    """List of reactions that are present on the message."""
