from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import final

from .abc import TelegramMethodWithMedia

if TYPE_CHECKING:
    from yatbaf.enums import StickerType
    from yatbaf.types import InputSticker
    from yatbaf.typing import NoneBool


@final
class CreateNewStickerSet(TelegramMethodWithMedia[bool]):
    """See :meth:`yatbaf.bot.Bot.create_new_sticker_set`"""

    user_id: int
    name: str
    title: str
    stickers: list[InputSticker]
    sticker_type: StickerType | None = None
    needs_repainting: NoneBool = None

    __meth_media_fields__: ClassVar[tuple[str, ...]] = ("stickers",)
