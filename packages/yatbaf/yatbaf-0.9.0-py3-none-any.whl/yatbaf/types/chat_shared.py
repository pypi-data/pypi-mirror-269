from __future__ import annotations

from typing import final

from yatbaf.typing import NoneStr

from .abc import TelegramType
from .photo_size import PhotoSize


@final
class ChatShared(TelegramType):
    """This object contains information about the chat whose identifier was
    shared with the bot using a
    :class:`yatbaf.types.KeyboardButtonRequestChat` button.

    See: https://core.telegram.org/bots/api#chatshared
    """

    request_id: int
    """Identifier of the request."""

    chat_id: int
    """Identifier of the shared chat.

    .. note::

        The bot may not have access to the chat and could be unable to use
        this identifier, unless the chat is already known to the bot by some
        other means.
    """

    title: NoneStr = None
    """*Optional.* Title of the chat, if the title was requested by the bot."""

    username: NoneStr = None
    """*Optional.* Username of the chat, if the username was requested by the
    bot and available.
    """

    photo: list[PhotoSize] | None = None
    """*Optional.* Available sizes of the chat photo, if the photo was requested
    by the bot.
    """
