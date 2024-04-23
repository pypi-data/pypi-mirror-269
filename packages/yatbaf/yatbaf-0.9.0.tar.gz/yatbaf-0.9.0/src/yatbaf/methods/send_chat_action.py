from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.enums import ChatAction
    from yatbaf.typing import NoneInt
    from yatbaf.typing import NoneStr


@final
class SendChatAction(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.send_chat_action`"""

    chat_id: str | int
    action: ChatAction
    business_connection_id: NoneStr = None
    message_thread_id: NoneInt = None
