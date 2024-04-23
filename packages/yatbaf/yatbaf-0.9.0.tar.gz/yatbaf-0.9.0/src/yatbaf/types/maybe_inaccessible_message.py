from __future__ import annotations

from typing import TYPE_CHECKING
from typing import TypeAlias

if TYPE_CHECKING:
    from .inaccessible_message import InaccessibleMessage
    from .message import Message

MaybeInaccessibleMessage: TypeAlias = "Message | InaccessibleMessage"
"""This object describes a message that can be inaccessible to the bot.

See: https://core.telegram.org/bots/api#maybeinaccessiblemessage
"""
