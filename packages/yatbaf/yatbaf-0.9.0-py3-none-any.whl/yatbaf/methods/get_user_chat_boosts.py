from __future__ import annotations

from typing import final

from yatbaf.types import UserChatBoosts

from .abc import TelegramMethod


@final
class GetUserChatBoosts(TelegramMethod[UserChatBoosts]):
    """See :meth:`~yatbaf.bot.Bot.get_user_chat_boosts`."""

    chat_id: int | str
    user_id: int
