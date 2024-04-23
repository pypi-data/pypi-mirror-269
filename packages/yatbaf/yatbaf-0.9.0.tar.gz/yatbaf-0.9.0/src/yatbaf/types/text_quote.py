from __future__ import annotations

from typing import final

from yatbaf.typing import NoneBool

from .abc import TelegramType
from .message_entity import MessageEntity


@final
class TextQuote(TelegramType):
    """This object contains information about the quoted part of a message that
    is replied to by the given message.

    See: https://core.telegram.org/bots/api#textquote
    """

    text: str
    """Text of the quoted part of a message that is replied to by the given
    message.
    """

    position: int
    """Approximate quote position in the original message in UTF-16 code units
    as specified by the sender.
    """

    entities: list[MessageEntity] | None = None
    """*Optional.* Special entities that appear in the quote. Currently, only
    *bold*, *italic*, *underline*, *strikethrough*, *spoiler*, and
    *custom_emoji* entities are kept in quotes.
    """

    is_manual: NoneBool = None
    """Optional. ``True``, if the quote was chosen manually by the message
    sender. Otherwise, the quote was added automatically by the server.
    """
