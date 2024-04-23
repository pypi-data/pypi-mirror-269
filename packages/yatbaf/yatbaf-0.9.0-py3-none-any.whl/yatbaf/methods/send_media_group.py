from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import final

from yatbaf.types import Message

from .abc import TelegramMethodWithMedia

if TYPE_CHECKING:
    from yatbaf.types import InputMediaAudio
    from yatbaf.types import InputMediaDocument
    from yatbaf.types import InputMediaPhoto
    from yatbaf.types import InputMediaVideo
    from yatbaf.types import ReplyParameters
    from yatbaf.typing import NoneBool
    from yatbaf.typing import NoneInt
    from yatbaf.typing import NoneStr


@final
class SendMediaGroup(TelegramMethodWithMedia[list[Message]]):
    """See :meth:`yatbaf.bot.Bot.send_media_group`"""

    chat_id: str | int
    # yapf: disable
    media: list[InputMediaAudio | InputMediaDocument | InputMediaPhoto | InputMediaVideo]  # noqa: E501
    # yapf: enable
    business_connection_id: NoneStr = None
    message_thread_id: NoneInt = None
    disable_notification: NoneBool = None
    protect_content: NoneBool = None
    reply_parameters: ReplyParameters | None = None

    __meth_media_fields__: ClassVar[tuple[str, ...]] = ("media",)
