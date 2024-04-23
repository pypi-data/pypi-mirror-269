from __future__ import annotations

__all__ = (
    "ChatBoostSource",
    "ChatBoostSourcePremium",
    "ChatBoostSourceGiftCode",
    "ChatBoostSourceGiveaway",
)

from typing import ClassVar
from typing import Literal
from typing import TypeAlias
from typing import final

from yatbaf.typing import NoneBool

from .abc import TelegramType
from .user import User


@final
class ChatBoostSourcePremium(TelegramType, tag="premium"):
    """The boost was obtained by subscribing to Telegram Premium or by gifting
    a Telegram Premium subscription to another user.

    See: https://core.telegram.org/bots/api#chatboostsourcepremium
    """

    user: User
    """User that boosted the chat."""

    source: ClassVar[Literal["premium"]] = "premium"
    """Source of the boost, always *premium*."""


@final
class ChatBoostSourceGiftCode(TelegramType, tag="gift_code"):
    """The boost was obtained by the creation of Telegram Premium gift codes to
    boost a chat. Each such code boosts the chat 4 times for the duration of the
    corresponding Telegram Premium subscription.

    See: https://core.telegram.org/bots/api#chatboostsourcegiftcode
    """

    user: User
    """User for which the gift code was created."""

    source: ClassVar[Literal["gift_code"]] = "gift_code"
    """Source of the boost, always *gift_code*."""


@final
class ChatBoostSourceGiveaway(TelegramType, tag="giveaway"):
    """The boost was obtained by the creation of a Telegram Premium giveaway.
    This boosts the chat 4 times for the duration of the corresponding Telegram
    Premium subscription.

    See: https://core.telegram.org/bots/api#chatboostsourcegiveaway
    """

    giveaway_message_id: int
    """Identifier of a message in the chat with the giveaway.

    .. note::

        The message could have been deleted already. May be 0 if the message
        isn't sent yet.
    """

    user: User | None = None
    """*Optional.* User that won the prize in the giveaway if any."""

    is_unclaimed: NoneBool = None
    """*Optional.* ``True``, if the giveaway was completed, but there was no
    user to win the prize.
    """

    source: ClassVar[Literal["giveaway"]] = "giveaway"
    """Source of the boost, always *giveaway*."""


ChatBoostSource: TypeAlias = (
    ChatBoostSourcePremium
    | ChatBoostSourceGiftCode
    | ChatBoostSourceGiveaway
)
"""This object describes the source of a chat boost.

See: https://core.telegram.org/bots/api#chatboostsource
"""
