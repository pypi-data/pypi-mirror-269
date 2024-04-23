from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Literal
from typing import final

from .abc import TelegramType

if TYPE_CHECKING:
    from .chat import Chat


@final
class InaccessibleMessage(TelegramType):
    """This object describes a message that was deleted or is otherwise
    inaccessible to the bot.

    See: https://core.telegram.org/bots/api#inaccessiblemessage
    """

    chat: Chat
    """Chat the message belonged to."""

    message_id: int
    """Unique message identifier inside the chat."""

    date: Literal[0] = 0
    """Always 0. The field can be used to differentiate regular and inaccessible
    messages.
    """
