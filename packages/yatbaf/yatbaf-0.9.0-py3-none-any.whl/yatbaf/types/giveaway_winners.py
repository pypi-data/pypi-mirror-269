from __future__ import annotations

from typing import final

from yatbaf.typing import NoneBool
from yatbaf.typing import NoneInt
from yatbaf.typing import NoneStr

from ..types import chat  # noqa: F401
from .abc import TelegramType
from .user import User


@final
class GiveawayWinners(TelegramType):
    """This object represents a message about the completion of a giveaway with
    public winners.

    See: https://core.telegram.org/bots/api#giveawaywinners
    """

    chat: chat.Chat
    """The chat that created the giveaway."""

    giveaway_message_id: int
    """Identifier of the messsage with the giveaway in the chat."""

    winners_selection_date: int
    """Point in time (Unix timestamp) when winners of the giveaway were selected."""  # noqa: E501

    winner_count: int
    """Total number of winners in the giveaway."""

    winners: list[User]
    """List of up to 100 winners of the giveaway."""

    additional_chat_count: NoneInt = None
    """*Optional.* The number of other chats the user had to join in order to be
    eligible for the giveaway.
    """

    premium_subscription_month_count: NoneInt = None
    """*Optional.* The number of months the Telegram Premium subscription won
    from the giveaway will be active for.
    """

    unclaimed_prize_count: NoneInt = None
    """*Optional.* Number of undistributed prizes."""

    only_new_members: NoneBool = None
    """*Optional.* ``True``, if only users who had joined the chats after the
    giveaway started were eligible to win.
    """

    was_refunded: NoneBool = None
    """*Optional.* ``True``, if the giveaway was canceled because the payment
    for it was refunded.
    """

    prize_description: NoneStr = None
    """*Optional.* Description of additional giveaway prize."""
