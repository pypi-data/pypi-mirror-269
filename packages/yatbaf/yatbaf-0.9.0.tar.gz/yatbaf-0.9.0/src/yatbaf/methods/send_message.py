from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import Message

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.enums import ParseMode
    from yatbaf.types import LinkPreviewOptions
    from yatbaf.types import MessageEntity
    from yatbaf.types import ReplyParameters
    from yatbaf.typing import NoneBool
    from yatbaf.typing import NoneInt
    from yatbaf.typing import NoneStr
    from yatbaf.typing import ReplyMarkup


@final
class SendMessage(TelegramMethod[Message]):
    """See :meth:`yatbaf.bot.Bot.send_message`"""

    chat_id: str | int
    text: str
    business_connection_id: NoneStr = None
    message_thread_id: NoneInt = None
    parse_mode: ParseMode | None = None
    entities: list[MessageEntity] | None = None
    link_preview_options: LinkPreviewOptions | None = None
    disable_notification: NoneBool = None
    protect_content: NoneBool = None
    reply_parameters: ReplyParameters | None = None
    reply_markup: ReplyMarkup | None = None
