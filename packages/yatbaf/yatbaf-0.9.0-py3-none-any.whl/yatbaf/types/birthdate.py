from __future__ import annotations

from typing import final

from yatbaf.typing import NoneInt

from .abc import TelegramType


@final
class Birthdate(TelegramType):
    """See: https://core.telegram.org/bots/api#birthdate"""

    day: int
    """Day of the user's birth; 1-31"""

    month: int
    """Month of the user's birth; 1-12"""

    year: NoneInt = None
    """Optional. Year of the user's birth."""
