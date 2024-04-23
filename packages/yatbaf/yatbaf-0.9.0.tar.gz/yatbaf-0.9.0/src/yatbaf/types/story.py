from __future__ import annotations

from typing import final

from ..types import chat  # noqa: F401
from .abc import TelegramType


@final
class Story(TelegramType):
    """This object represents a story.

    See: https://core.telegram.org/bots/api#story
    """

    chat: chat.Chat
    """Chat that posted the story."""

    id: int
    """Unique identifier for the story in the chat."""
