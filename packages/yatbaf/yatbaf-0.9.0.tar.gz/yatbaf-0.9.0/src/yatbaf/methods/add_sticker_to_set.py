from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import final

from .abc import TelegramMethodWithMedia

if TYPE_CHECKING:
    from yatbaf.types import InputSticker


@final
class AddStickerToSet(TelegramMethodWithMedia[bool]):
    """See :meth:`yatbaf.bot.Bot.add_sticker_to_set`"""

    user_id: int
    name: str
    sticker: InputSticker

    __meth_media_fields__: ClassVar[tuple[str, ...]] = ("sticker",)
