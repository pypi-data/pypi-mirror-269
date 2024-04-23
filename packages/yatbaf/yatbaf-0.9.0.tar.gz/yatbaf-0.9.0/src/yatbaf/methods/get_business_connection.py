from __future__ import annotations

from typing import final

from yatbaf.types import BusinessConnection

from .abc import TelegramMethod


@final
class GetBusinessConnection(TelegramMethod[BusinessConnection]):
    """See: :meth:`~yatbaf.bot.Bot.get_business_connection`."""

    business_connection_id: str
