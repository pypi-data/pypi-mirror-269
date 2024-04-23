from __future__ import annotations

from typing import final

from .abc import TelegramType
from .business_opening_hours_interval import BusinessOpeningHoursInterval


@final
class BusinessOpeningHours(TelegramType):
    """See: https://core.telegram.org/bots/api#businessopeninghours"""

    time_zone_name: str
    """Unique name of the time zone for which the opening hours are defined."""

    opening_hours: list[BusinessOpeningHoursInterval]
    """List of time intervals describing business opening hours."""
