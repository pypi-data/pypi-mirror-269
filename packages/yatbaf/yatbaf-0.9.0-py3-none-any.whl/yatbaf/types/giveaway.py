from __future__ import annotations

from typing import final

from yatbaf.typing import NoneBool
from yatbaf.typing import NoneInt
from yatbaf.typing import NoneStr

from ..types import chat
from .abc import TelegramType


@final
class Giveaway(TelegramType):
    """This object represents a message about a scheduled giveaway.

    See: https://core.telegram.org/bots/api#giveaway
    """

    chats: list[chat.Chat]
    """The list of chats which the user must join to participate in the
    giveaway.
    """

    winners_selection_date: int
    """Point in time (Unix timestamp) when winners of the giveaway will be
    selected.
    """

    winner_count: int
    """The number of users which are supposed to be selected as winners of the
    giveaway.
    """

    only_new_members: NoneBool = None
    """*Optional.* ``True``, if only users who join the chats after the giveaway
    started should be eligible to win.
    """

    has_public_winners: NoneBool = None
    """*Optional.* ``True``, if the list of giveaway winners will be visible to
    everyone.
    """

    prize_description: NoneStr = None
    """*Optional.* Description of additional giveaway prize."""

    country_codes: list[str] | None = None
    """*Optional.* A list of two-letter ISO 3166-1 alpha-2 country codes
    indicating the countries from which eligible users for the giveaway must
    come. If empty, then all users can participate in the giveaway. Users with
    a phone number that was bought on Fragment can always participate in
    giveaways.
    """

    premium_subscription_month_count: NoneInt = None
    """*Optional.* The number of months the Telegram Premium subscription won
    from the giveaway will be active for.
    """
