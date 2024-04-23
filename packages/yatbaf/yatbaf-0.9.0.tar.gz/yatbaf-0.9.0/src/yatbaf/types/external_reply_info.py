from __future__ import annotations

from typing import final

from yatbaf.typing import NoneBool

from ..types import chat  # noqa: F401
from .abc import TelegramType
from .animation import Animation
from .audio import Audio
from .contact import Contact
from .dice import Dice
from .document import Document
from .game import Game
from .giveaway import Giveaway
from .giveaway_winners import GiveawayWinners
from .invoice import Invoice
from .link_preview_options import LinkPreviewOptions
from .location import Location
from .message_origin import MessageOrigin
from .photo_size import PhotoSize
from .poll import Poll
from .sticker import Sticker
from .story import Story
from .venue import Venue
from .video import Video
from .video_note import VideoNote
from .voice import Voice


@final
class ExternalReplyInfo(TelegramType):
    """This object contains information about a message that is being replied
    to, which may come from another chat or forum topic.

    See: https://core.telegram.org/bots/api#externalreplyinfo
    """

    origin: MessageOrigin
    """Origin of the message replied to by the given message."""

    chat: chat.Chat | None = None  # noqa: F811
    """*Optional.* Chat the original message belongs to. Available only if the
    chat is a supergroup or a channel."""

    message_id: int | None = None
    """*Optional.* Unique message identifier inside the original chat. Available
    only if the original chat is a supergroup or a channel.
    """

    link_preview_options: LinkPreviewOptions | None = None
    """*Optional.* Options used for link preview generation for the original
    message, if it is a text message.
    """

    animation: Animation | None = None
    """*Optional.* Message is an animation, information about the animation."""

    audio: Audio | None = None
    """*Optional.* Message is an audio file, information about the file."""

    document: Document | None = None
    """*Optional.* Message is a general file, information about the file."""

    photo: list[PhotoSize] | None = None
    """*Optional.* Message is a photo, available sizes of the photo."""

    sticker: Sticker | None = None
    """*Optional.* Message is a sticker, information about the sticker."""

    story: Story | None = None
    """*Optional.* Message is a forwarded story."""

    video: Video | None = None
    """*Optional.* Message is a video, information about the video."""

    video_note: VideoNote | None = None
    """*Optional.* Message is a video note, information about the video message."""  # noqa: E501

    voice: Voice | None = None
    """*Optional.* Message is a voice message, information about the file."""

    has_media_spoiler: NoneBool = None
    """*Optional.* True, if the message media is covered by a spoiler animation."""  # noqa: E501

    contact: Contact | None = None
    """*Optional.* Message is a shared contact, information about the contact."""  # noqa: E501

    dice: Dice | None = None
    """*Optional.* Message is a dice with random value."""

    game: Game | None = None
    """*Optional.* Message is a game, information about the game."""

    giveaway: Giveaway | None = None
    """*Optional.* Message is a scheduled giveaway, information about the giveaway."""  # noqa: E501

    giveaway_winners: GiveawayWinners | None = None
    """*Optional.* A giveaway with public winners was completed."""

    invoice: Invoice | None = None
    """*Optional.* Message is an invoice for a payment, information about the invoice."""  # noqa: E501

    location: Location | None = None
    """*Optional.* Message is a shared location, information about the location."""  # noqa: E501

    poll: Poll | None = None
    """*Optional.* Message is a native poll, information about the poll."""

    venue: Venue | None = None
    """*Optional.* Message is a venue, information about the venue."""
