from __future__ import annotations

from typing import final

from yatbaf.typing import NoneStr

from .abc import TelegramType
from .sticker import Sticker


@final
class BusinessIntro(TelegramType):
    """See: https://core.telegram.org/bots/api#businessintro"""

    title: NoneStr = None
    """*Optional.* Title text of the business intro."""

    message: NoneStr = None
    """*Optional.* Message text of the business intro."""

    sticker: Sticker | None = None
    """*Optional.* Sticker of the business intro."""
