from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import Message

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.types import InlineKeyboardMarkup
    from yatbaf.types import ReplyParameters
    from yatbaf.typing import NoneBool
    from yatbaf.typing import NoneInt
    from yatbaf.typing import NoneStr


@final
class SendGame(TelegramMethod[Message]):
    """See :meth:`yatbaf.bot.Bot.send_game`"""

    chat_id: str | int
    game_short_name: str
    business_connection_id: NoneStr = None
    message_thread_id: NoneInt = None
    disable_notification: NoneBool = None
    protect_content: NoneBool = None
    reply_parameters: ReplyParameters | None = None
    reply_markup: InlineKeyboardMarkup | None = None
