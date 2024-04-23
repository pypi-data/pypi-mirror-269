from __future__ import annotations

from typing import final

from .abc import TelegramType


@final
class BusinessOpeningHoursInterval(TelegramType):
    """See: https://core.telegram.org/bots/api#businessopeninghoursinterval"""

    opening_minute: int
    """The minute's sequence number in a week, starting on Monday, marking the
    start of the time interval during which the business is open; 0 - 7 * 24 * 60
    """  # noqa: E501

    closing_minute: int
    """The minute's sequence number in a week, starting on Monday, marking the
    end of the time interval during which the business is open; 0 - 8 * 24 * 60
    """
