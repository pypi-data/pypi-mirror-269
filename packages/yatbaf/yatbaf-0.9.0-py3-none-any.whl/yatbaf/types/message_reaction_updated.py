from __future__ import annotations

from typing import final

from .abc import TelegramType
from .chat import Chat
from .reaction_type import ReactionType
from .user import User


@final
class MessageReactionUpdated(TelegramType, kw_only=True):
    """This object represents a change of a reaction on a message performed by
    a user.

    See: https://core.telegram.org/bots/api#messagereactionupdated
    """

    chat: Chat
    """The chat containing the message the user reacted to."""

    message_id: int
    """Unique identifier of the message inside the chat."""

    user: User | None = None
    """*Optional.* The user that changed the reaction, if the user isn't
    anonymous.
    """

    actor_chat: Chat | None = None
    """*Optional.* The chat on behalf of which the reaction was changed, if the
    user is anonymous.
    """

    date: int
    """Date of the change in Unix time."""

    old_reaction: list[ReactionType]
    """Previous list of reaction types that were set by the user."""

    new_reaction: list[ReactionType]
    """New list of reaction types that have been set by the user."""
