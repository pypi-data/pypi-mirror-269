from __future__ import annotations

from typing import final

from yatbaf.enums import ParseMode
from yatbaf.typing import NoneBool
from yatbaf.typing import NoneInt
from yatbaf.typing import NoneStr

from .abc import TelegramType
from .message_entity import MessageEntity


@final
class ReplyParameters(TelegramType):
    """Describes reply parameters for the message that is being sent.

    See: https://core.telegram.org/bots/api#replyparameters
    """

    message_id: int
    """Identifier of the message that will be replied to in the current chat,
    or in the chat ``chat_id`` if it is specified.
    """

    chat_id: str | int | None = None
    """*Optional.* If the message to be replied to is from a different chat,
    unique identifier for the chat or username of the channel (in the format
    @channelusername).
    """

    allow_sending_without_reply: NoneBool = None
    """*Optional.* Pass ``True`` if the message should be sent even if the
    specified message to be replied to is not found; can be used only for
    replies in the same chat and forum topic.
    """

    quote: NoneStr = None
    """*Optional.* Quoted part of the message to be replied to; 0-1024
    characters after entities parsing. The quote must be an exact substring of
    the message to be replied to, including *bold*, *italic*, *underline*,
    *strikethrough*, *spoiler*, and *custom_emoji* entities. The message will
    fail to send if the quote isn't found in the original message.
    """

    quote_parse_mode: ParseMode | None = None
    """*Optional.* Mode for parsing entities in the quote."""

    quote_entities: list[MessageEntity] | None = None
    """*Optional.* A list of special entities that appear in the quote. It can
    be specified instead of ``quote_parse_mode``.
    """

    quote_position: NoneInt = None
    """*Optional.* Position of the quote in the original message in UTF-16 code
    units.
    """
