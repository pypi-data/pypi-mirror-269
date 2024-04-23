from __future__ import annotations

__all__ = (
    "Content",
    "text",
    "video",
    "document",
    "audio",
    "photo",
    "sticker",
    "media",
)

from typing import TYPE_CHECKING
from typing import Final
from typing import final

from yatbaf.enums import ContentType

from .base import BaseFilter

if TYPE_CHECKING:
    from yatbaf.types import Message
    from yatbaf.typing import FilterPriority


@final
class Content(BaseFilter):
    """Content filter.

    Use it to filter message by content::

        @on_message(filters=[Content("photo")])
        async def process_photo(message: Message) -> None:
            ...

        @on_message(filters=[Content(ContentType.DOCUMENT)])
        async def process_document(message: Message) -> None:
            ...

    See :class:`~yatbaf.enums.ContentType`.
    """

    __slots__ = (
        "content",
        "_priority",
    )

    def __init__(
        self,
        *content: ContentType | str,
        priority: int = 100,
    ) -> None:
        """
        :param content: Content type.
        :param priority: *Optional.* Filter priority.
        :raise ValueError: If ``content`` is empty or wrong type was passed.
        """
        if not content:
            raise ValueError("You must pass at least one type.")
        self.content = frozenset([ContentType(c) for c in content])
        self._priority = priority

    @property
    def priority(self) -> FilterPriority:
        return {"content": (len(self.content), self._priority)}

    async def check(self, update: Message) -> bool:
        for c in self.content:
            if getattr(update, c) is not None:
                return True
        return False


text = Content("text")
video = Content("video")
document = Content("document")
audio = Content("audio")
photo = Content("photo")
sticker = Content("sticker")

media: Final[Content] = Content(
    ContentType.AUDIO,
    ContentType.VIDEO,
    ContentType.VIDEO_NOTE,
    ContentType.VOICE,
    ContentType.PHOTO,
    ContentType.ANIMATION,
    ContentType.STICKER,
    ContentType.DOCUMENT,
)
"""Media content filter.

Use it to filter message with media content (``animation``, ``audio``,
``document``, ``photo``, ``sticker``, ``video``, ``video note`` or ``voice``).

Usage::

    @on_message(filters=[media])
    async def callback(message: Message) -> None:
        ...
"""
