from __future__ import annotations

from typing import final

from yatbaf.typing import NoneInt

from ..types import message
from .abc import TelegramType


@final
class GiveawayCompleted(TelegramType):
    """This object represents a service message about the completion of a
    giveaway without public winners.

    See: https://core.telegram.org/bots/api#giveawaycompleted
    """

    winner_count: int
    """Number of winners in the giveaway."""

    unclaimed_prize_count: NoneInt = None
    """*Optional.* Number of undistributed prizes."""

    giveaway_message: message.Message | None = None
    """*Optional.* Message with the giveaway that was completed, if it wasn't
    deleted.
    """
