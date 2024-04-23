from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import MessageId

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.typing import NoneBool
    from yatbaf.typing import NoneInt


@final
class ForwardMessages(TelegramMethod[list[MessageId]]):
    """See :meth:`~yatbaf.bot.Bot.forward_messages`"""

    chat_id: int | str
    from_chat_id: int | str
    message_ids: list[int]
    message_thread_id: NoneInt = None
    disable_notification: NoneBool = None
    protect_content: NoneBool = None
