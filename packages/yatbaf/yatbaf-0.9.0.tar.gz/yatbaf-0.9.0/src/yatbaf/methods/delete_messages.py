from __future__ import annotations

from typing import final

from .abc import TelegramMethod


@final
class DeleteMessages(TelegramMethod[bool]):
    """See :meth:`~yatbaf.bot.Bot.delete_messages`"""

    chat_id: int | str
    message_ids: list[int]
