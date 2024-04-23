from typing import final

from .abc import TelegramType


@final
class GiveawayCreated(TelegramType):
    """This object represents a service message about the creation of a
    scheduled giveaway. Currently holds no information.

    See: https://core.telegram.org/bots/api#giveawaycreated
    """
