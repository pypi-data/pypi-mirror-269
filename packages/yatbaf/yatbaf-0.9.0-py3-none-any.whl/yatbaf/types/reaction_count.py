from __future__ import annotations

from typing import final

from .abc import TelegramType
from .reaction_type import ReactionType


@final
class ReactionCount(TelegramType):
    """Represents a reaction added to a message along with the number of times
    it was added.

    See: https://core.telegram.org/bots/api#reactioncount
    """

    type: ReactionType
    """Type of the reaction."""

    total_count: int
    """Number of times the reaction was added."""
