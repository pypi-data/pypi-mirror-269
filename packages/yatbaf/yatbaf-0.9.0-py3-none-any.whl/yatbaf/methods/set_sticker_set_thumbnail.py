from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import final

from .abc import TelegramMethodWithFile

if TYPE_CHECKING:
    from yatbaf.enums import StickerFormat
    from yatbaf.typing import InputFile


@final
class SetStickerSetThumbnail(TelegramMethodWithFile[bool]):
    """See :meth:`yatbaf.bot.Bot.set_sticker_set_thumbnail`"""

    name: str
    user_id: int
    format: StickerFormat
    thumbnail: InputFile | str | None = None

    __meth_file_fields__: ClassVar[tuple[str, ...]] = ("thumbnail",)
