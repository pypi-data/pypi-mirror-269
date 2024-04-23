from __future__ import annotations

from typing import final

from yatbaf.typing import NoneStr

from .abc import TelegramType
from .photo_size import PhotoSize


@final
class SharedUser(TelegramType):
    """This object contains information about a user that was shared with the
    bot using a :class:`~.keyboard_button.KeyboardButtonRequestUser` button.

    See: https://core.telegram.org/bots/api#shareduser
    """

    user_id: int
    """Identifier of the shared user.

    .. note::

        The bot may not have access to the user and could be unable to use this
        identifier, unless the user is already known to the bot by some other
        means.
    """

    first_name: NoneStr = None
    """*Optional.* First name of the user, if the name was requested by the bot."""  # noqa: E501

    last_name: NoneStr = None
    """*Optional.* Last name of the user, if the name was requested by the bot."""  # noqa: E501

    username: NoneStr = None
    """*Optional.* Username of the user, if the username was requested by the
    bot.
    """

    photo: list[PhotoSize] | None = None
    """*Optional.* Available sizes of the chat photo, if the photo was requested
    by the bot.
    """
