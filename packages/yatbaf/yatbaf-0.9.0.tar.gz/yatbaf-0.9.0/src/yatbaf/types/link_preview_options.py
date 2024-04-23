from __future__ import annotations

from typing import final

from yatbaf.typing import NoneBool
from yatbaf.typing import NoneStr

from .abc import TelegramType


@final
class LinkPreviewOptions(TelegramType):
    """Describes the options used for link preview generation.

    See: https://core.telegram.org/bots/api#linkpreviewoptions
    """

    is_disabled: NoneBool = None
    """*Optional.* ``True``, if the link preview is disabled."""

    url: NoneStr = None
    """*Optional.* URL to use for the link preview. If empty, then the first URL
    found in the message text will be used.
    """

    prefer_small_media: NoneBool = None
    """*Optional.* ``True``, if the media in the link preview is suppposed to be
    shrunk.

    .. note::

        Ignored if the URL isn't explicitly specified or media size change isn't
        supported for the preview.
    """

    prefer_large_media: NoneBool = None
    """*Optional.* ``True``, if the media in the link preview is suppposed to be
    enlarged.

    .. note::

        Ignored if the URL isn't explicitly specified or media size change isn't
        supported for the preview.
    """

    show_above_text: NoneBool = None
    """*Optional.* ``True``, if the link preview must be shown above the message
    text; otherwise, the link preview will be shown below the message text.
    """
