from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramType

if TYPE_CHECKING:
    from yatbaf.enums import ParseMode

    from .link_preview_options import LinkPreviewOptions
    from .message_entity import MessageEntity


@final
class InputTextMessageContent(TelegramType):
    """Represents the content of a text message to be sent as the result of an
    inline query.

    See: https://core.telegram.org/bots/api#inputtextmessagecontent
    """

    message_text: str
    """Text of the message to be sent, 1-4096 characters."""

    parse_mode: ParseMode | None = None
    """*Optional.* Mode for parsing entities in the message text."""

    entities: list[MessageEntity] | None = None
    """*Optional.* List of special entities that appear in message text, which
    can be specified instead of ``parse_mode``.
    """

    link_preview_options: LinkPreviewOptions | None = None
    """*Optional.* Link preview generation options for the message."""
