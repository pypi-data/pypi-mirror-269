from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import final

from .abc import TelegramMethodWithMedia

if TYPE_CHECKING:
    from yatbaf.types import InputSticker


@final
class ReplaceStickerInSet(TelegramMethodWithMedia[bool]):
    """See :meth:`~yatbaf.bot.Bot.replace_sticker_in_set`"""

    user_id: int
    name: str
    old_sticker: str
    sticker: InputSticker

    __meth_media_fields__: ClassVar[tuple[str, ...]] = ("sticker",)
