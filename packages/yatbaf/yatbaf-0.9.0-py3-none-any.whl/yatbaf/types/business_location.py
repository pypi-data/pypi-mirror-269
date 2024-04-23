from __future__ import annotations

from typing import final

from .abc import TelegramType
from .location import Location


@final
class BusinessLocation(TelegramType):
    """See: https://core.telegram.org/bots/api#businesslocation"""

    address: str
    """Address of the business."""

    location: Location | None = None
    """*Optional.* Location of the business."""
