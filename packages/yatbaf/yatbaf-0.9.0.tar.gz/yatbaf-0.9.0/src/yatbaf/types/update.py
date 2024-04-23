from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramType
from .business_connection import BusinessConnection
from .business_messages_deleted import BusinessMessagesDeleted
from .callback_query import CallbackQuery
from .chat_boost_removed import ChatBoostRemoved
from .chat_boost_updated import ChatBoostUpdated
from .chat_join_request import ChatJoinRequest
from .chat_member import ChatMemberUpdated
from .chosen_inline_result import ChosenInlineResult
from .inline_query import InlineQuery
from .message import Message
from .message_reaction_count_updated import MessageReactionCountUpdated
from .message_reaction_updated import MessageReactionUpdated
from .poll import Poll
from .poll_answer import PollAnswer
from .pre_checkout_query import PreCheckoutQuery
from .shipping_query import ShippingQuery

if TYPE_CHECKING:
    from yatbaf.typing import UpdateModel


@final
class Update(TelegramType):
    """This object represents an incoming update.

    .. note::

        At most **one** of the optional parameters can be present in any given
        update.

    See: https://core.telegram.org/bots/api#update
    """

    update_id: int
    """The update's unique identifier. Update identifiers start from a certain
    positive number and increase sequentially. This ID becomes especially handy
    if you're using webhooks, since it allows you to ignore repeated updates or
    to restore the correct update sequence, should they get out of order. If
    there are no new updates for at least a week, then identifier of the next
    update will be chosen randomly instead of sequentially.
    """

    message: Message | None = None
    """*Optional.* New incoming message of any kind - text, photo, sticker, etc."""  # noqa: E501

    edited_message: Message | None = None
    """*Optional.* New version of a message that is known to the bot and was edited."""  # noqa: E501

    channel_post: Message | None = None
    """*Optional.* New incoming channel post of any kind - text, photo, sticker, etc."""  # noqa: E501

    edited_channel_post: Message | None = None
    """*Optional.* New version of a channel post that is known to the bot and
    was edited.
    """

    business_connection: BusinessConnection | None = None
    """*Optional.* The bot was connected to or disconnected from a business
    account, or a user edited an existing connection with the bot.
    """

    business_message: Message | None = None
    """*Optional.* New non-service message from a connected business account."""

    edited_business_message: Message | None = None
    """*Optional.* New version of a message from a connected business account."""  # noqa: E501

    deleted_business_messages: BusinessMessagesDeleted | None = None
    """*Optional.* Messages were deleted from a connected business account."""

    message_reaction: MessageReactionUpdated | None = None
    """*Optional.* A reaction to a message was changed by a user.

    .. important::

        The bot must be an administrator in the chat and must explicitly specify
        ``message_reaction`` in the list of ``allowed_updates`` to receive these
        updates. The update isn't received for reactions set by bots.
    """

    message_reaction_count: MessageReactionCountUpdated | None = None
    """*Optional.* Reactions to a message with anonymous reactions were changed.

    .. important::

        The bot must be an administrator in the chat and must explicitly specify
        ``message_reaction_count`` in the list of ``allowed_updates`` to receive
        these updates.
    """

    inline_query: InlineQuery | None = None
    """*Optional.* New incoming inline query"""

    chosen_inline_result: ChosenInlineResult | None = None
    """*Optional.* The result of an inline query that was chosen by a user and
    sent to their chat partner. Please see documentation on the
    `feedback collecting`_ for details on how to enable these updates for your
    bot.

    .. _feedback collecting: https://core.telegram.org/bots/inline#collecting-feedback
    """  # noqa: E501

    callback_query: CallbackQuery | None = None
    """*Optional.* New incoming callback query."""

    shipping_query: ShippingQuery | None = None
    """*Optional.* New incoming shipping query.

    .. note::

        Only for invoices with flexible price.
    """

    pre_checkout_query: PreCheckoutQuery | None = None
    """*Optional.* New incoming pre-checkout query. Contains full information
    about checkout.
    """

    poll: Poll | None = None
    """*Optional.* New poll state. Bots receive only updates about stopped polls
    and polls, which are sent by the bot.
    """

    poll_answer: PollAnswer | None = None
    """*Optional.* A user changed their answer in a non-anonymous poll. Bots
    receive new votes only in polls that were sent by the bot itself.
    """

    my_chat_member: ChatMemberUpdated | None = None
    """*Optional.* The bot's chat member status was updated in a chat. For
    private chats, this update is received only when the bot is blocked or
    unblocked by the user.
    """

    chat_member: ChatMemberUpdated | None = None
    """*Optional.* A chat member's status was updated in a chat.

    .. important::

        The bot must be an administrator in the chat and must explicitly specify
        ``chat_member`` in the list of ``allowed_updates`` to receive these
        updates.
    """

    chat_join_request: ChatJoinRequest | None = None
    """*Optional.* A request to join the chat has been sent.

    .. important::

        The bot must have the ``can_invite_users`` administrator right in the
        chat to receive these updates.
    """

    chat_boost: ChatBoostUpdated | None = None
    """*Optional.* A chat boost was added or changed.

    .. important::

        The bot must be an administrator in the chat to receive these updates.
    """

    removed_chat_boost: ChatBoostRemoved | None = None
    """*Optional.* A boost was removed from a chat.

    .. important::

        The bot must be an administrator in the chat to receive these updates.
    """

    @property
    def event(self) -> UpdateModel:
        """:meta private:"""
        return self.__usrctx__["_event"]  # type: ignore[no-any-return]

    @property
    def event_type(self) -> str:
        """:meta private:"""
        return self.__usrctx__["_event_type"]  # type: ignore[no-any-return]

    def __post_init__(self) -> None:
        """:meta private:"""
        super().__post_init__()
        update_id = self.update_id
        self.update_id = None  # type: ignore[assignment]
        for field in self.__struct_fields__:
            # one filed is always not None
            if (v := getattr(self, field)) is not None:
                self.update_id = update_id
                self.__usrctx__["_event"] = v
                self.__usrctx__["_event_type"] = field
                break
