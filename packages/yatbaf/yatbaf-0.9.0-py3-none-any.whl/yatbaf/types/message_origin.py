from __future__ import annotations

from typing import ClassVar
from typing import Literal
from typing import TypeAlias
from typing import final

from yatbaf.typing import NoneStr

from ..types import chat
from .abc import TelegramType
from .user import User


@final
class MessageOriginUser(TelegramType, tag="user"):
    """The message was originally sent by a known user.

    See: https://core.telegram.org/bots/api#messageoriginuser
    """

    date: int
    """Date the message was sent originally in Unix time."""

    sender_user: User
    """User that sent the message originally."""

    type: ClassVar[Literal["user"]] = "user"
    """Type of the message origin, always `user`"""


@final
class MessageOriginHiddenUser(TelegramType, tag="hidden_user"):
    """The message was originally sent by an unknown user.

    See: https://core.telegram.org/bots/api#messageoriginhiddenuser
    """

    date: int
    """Date the message was sent originally in Unix time."""

    sender_user_name: str
    """Name of the user that sent the message originally."""

    type: ClassVar[Literal["hidden_user"]] = "hidden_user"
    """Type of the message origin, always `hidden_user`"""


@final
class MessageOriginChat(TelegramType, tag="chat"):
    """The message was originally sent on behalf of a chat to a group chat.

    See: https://core.telegram.org/bots/api#messageoriginchat
    """

    date: int
    """Date the message was sent originally in Unix time."""

    sender_chat: chat.Chat
    """Chat that sent the message originally."""

    author_signature: NoneStr = None
    """*Optional.* For messages originally sent by an anonymous chat
    administrator, original message author signature.
    """

    type: ClassVar[Literal["chat"]] = "chat"
    """Type of the message origin, always `chat`"""


@final
class MessageOriginChannel(TelegramType, tag="channel"):
    """The message was originally sent to a channel chat.

    See: https://core.telegram.org/bots/api#messageoriginchannel
    """

    date: int
    """Date the message was sent originally in Unix time."""

    chat: chat.Chat
    """Channel chat to which the message was originally sent."""

    message_id: int
    """Unique message identifier inside the chat."""

    author_signature: NoneStr = None
    """*Optional.* Signature of the original post author."""

    type: ClassVar[Literal["channel"]] = "channel"
    """Type of the message origin, always `channel`"""


MessageOrigin: TypeAlias = (
    MessageOriginUser
    | MessageOriginHiddenUser
    | MessageOriginChat
    | MessageOriginChannel
)
"""This object describes the origin of a message.

See: https://core.telegram.org/bots/api#messageorigin
"""
