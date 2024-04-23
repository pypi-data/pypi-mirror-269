from __future__ import annotations

__all__ = (
    "ReactionType",
    "ReactionTypeEmoji",
    "ReactionTypeCustomEmoji",
)

from typing import ClassVar
from typing import Literal
from typing import TypeAlias
from typing import final

from .abc import TelegramType


@final
class ReactionTypeEmoji(TelegramType, tag="emoji"):
    """The reaction is based on an emoji.

    See: https://core.telegram.org/bots/api#reactiontypeemoji
    """

    emoji: str
    """Reaction emoji."""

    type: ClassVar[Literal["emoji"]] = "emoji"
    """Type of the reaction, always *emoji*"""


@final
class ReactionTypeCustomEmoji(TelegramType, tag="custom_emoji"):
    """The reaction is based on a custom emoji.

    See: https://core.telegram.org/bots/api#reactiontypecustomemoji
    """

    custom_emoji_id: str
    """Custom emoji identifier."""

    type: ClassVar[Literal["custom_emoji"]] = "custom_emoji"
    """Type of the reaction, always *custom_emoji*."""


ReactionType: TypeAlias = ReactionTypeEmoji | ReactionTypeCustomEmoji
"""This object describes the type of a reaction.

See: https://core.telegram.org/bots/api#reactiontype
"""
