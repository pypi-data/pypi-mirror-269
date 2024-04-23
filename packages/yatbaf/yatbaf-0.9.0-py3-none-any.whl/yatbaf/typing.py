from __future__ import annotations

__all__ = (
    "HandlerGuard",
    "HandlerCallable",
    "HandlerMiddleware",
    "RouterGurad",
    "RouterCallable",
    "RouterMiddleware",
    "Handlers",
    "MiddlewareCallable",
    "UpdateT",
    "UpdateModel",
    "ReplyMarkup",
    "NoneStr",
    "NoneInt",
    "NoneBool",
)

from typing import TYPE_CHECKING
from typing import Any
from typing import Concatenate
from typing import Literal
from typing import ParamSpec
from typing import Protocol
from typing import TypeAlias
from typing import TypedDict
from typing import TypeVar
from typing import runtime_checkable

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator
    from collections.abc import Awaitable
    from collections.abc import Callable

    from .abc import AbstractHandler
    from .bot import Bot
    from .middleware import Middleware
    from .types import BusinessConnection
    from .types import BusinessMessagesDeleted
    from .types import CallbackQuery
    from .types import ChatBoostRemoved
    from .types import ChatBoostUpdated
    from .types import ChatJoinRequest
    from .types import ChatMemberUpdated
    from .types import ChosenInlineResult
    from .types import ForceReply
    from .types import InlineKeyboardMarkup
    from .types import InlineQuery
    from .types import Message
    from .types import MessageReactionCountUpdated
    from .types import MessageReactionUpdated
    from .types import Poll
    from .types import PollAnswer
    from .types import PreCheckoutQuery
    from .types import ReplyKeyboardMarkup
    from .types import ReplyKeyboardRemove
    from .types import ShippingQuery
    from .types import Update
    from .types.abc import TelegramType

    UpdateT = TypeVar(
        "UpdateT",
        bound=(
            CallbackQuery
            | ChatJoinRequest
            | ChatMemberUpdated
            | InlineQuery
            | ChosenInlineResult
            | Message
            | MessageReactionCountUpdated
            | MessageReactionUpdated
            | Poll
            | PollAnswer
            | PreCheckoutQuery
            | ShippingQuery
            | ChatBoostRemoved
            | ChatBoostUpdated
            | BusinessConnection
            | BusinessMessagesDeleted
        )
    )

    ResultModelT = TypeVar(
        "ResultModelT", bound=TelegramType | list | int | str | bool
    )

else:
    UpdateT = TypeVar("UpdateT")
    ResultModelT = TypeVar("ResultModelT")

T = TypeVar("T")
P = ParamSpec("P")
T_contra = TypeVar("T_contra", contravariant=True)

UpdateModel: TypeAlias = (
    "CallbackQuery "
    "| ChatJoinRequest "
    "| ChatMemberUpdated "
    "| InlineQuery "
    "| ChosenInlineResult "
    "| Message "
    "| MessageReactionCountUpdated "
    "| MessageReactionUpdated "
    "| Poll "
    "| PollAnswer "
    "| PreCheckoutQuery "
    "| ShippingQuery"
    "| ChatBoostRemoved"
    "| ChatBoostUpdated"
    "| BusinessConnection"
    "| BusinessMessagesDeleted"
)

ReplyMarkup: TypeAlias = (
    "ForceReply "
    "| InlineKeyboardMarkup "
    "| ReplyKeyboardMarkup "
    "| ReplyKeyboardRemove"
)

NoneStr: TypeAlias = "str | None"
NoneInt: TypeAlias = "int | None"
NoneBool: TypeAlias = "bool | None"

MiddlewareCallable: TypeAlias = "Callable[[T], T]"

RouterCallable: TypeAlias = "Callable[[Update], Awaitable[None]]"
RouterGurad: TypeAlias = "Callable[[Update], Awaitable[None]]"
RouterMiddleware: TypeAlias = "Middleware[RouterCallable] | MiddlewareCallable[RouterCallable]"  # noqa: E501

_HandlerCallable: TypeAlias = "Callable[Concatenate[UpdateT, P], Awaitable[None]]"  # noqa: E501
HandlerCallable: TypeAlias = "_HandlerCallable[UpdateT, Any]"
HandlerCallableType: TypeAlias = "Callable[[UpdateT], Awaitable[None]]"
HandlerGuard: TypeAlias = "Callable[[UpdateT], Awaitable[None]]"
HandlerMiddleware: TypeAlias = (
    "Middleware[HandlerCallableType[UpdateT]] "
    "| MiddlewareCallable[HandlerCallableType[UpdateT]]"
)
HandlerDependency: TypeAlias = (
    "Callable[..., Awaitable[Any]] "
    "| Callable[..., AsyncGenerator[Any, None]] "
    "| type[Any]"
)

Scope: TypeAlias = "Literal['router', 'handler', 'local']"

PollingHook: TypeAlias = "Callable[[Bot], Awaitable[None]]"

FilterGroup: TypeAlias = "Literal['content', 'sender', 'chat']"
FilterPriority: TypeAlias = "dict[FilterGroup, tuple[int, int | tuple[int, int]]]"  # noqa: E501


class Handlers(TypedDict):
    message: AbstractHandler[Message] | None
    edited_message: AbstractHandler[Message] | None
    channel_post: AbstractHandler[Message] | None
    edited_channel_post: AbstractHandler[Message] | None
    message_reaction: AbstractHandler[MessageReactionUpdated] | None
    message_reaction_count: AbstractHandler[MessageReactionCountUpdated] | None
    inline_query: AbstractHandler[InlineQuery] | None
    chosen_inline_result: AbstractHandler[ChosenInlineResult] | None
    callback_query: AbstractHandler[CallbackQuery] | None
    shipping_query: AbstractHandler[ShippingQuery] | None
    pre_checkout_query: AbstractHandler[PreCheckoutQuery] | None
    poll: AbstractHandler[Poll] | None
    poll_answer: AbstractHandler[PollAnswer] | None
    my_chat_member: AbstractHandler[ChatMemberUpdated] | None
    chat_member: AbstractHandler[ChatMemberUpdated] | None
    chat_join_request: AbstractHandler[ChatJoinRequest] | None
    chat_boost: AbstractHandler[ChatBoostUpdated] | None
    removed_chat_boost: AbstractHandler[ChatBoostRemoved] | None


@runtime_checkable
class InputFile(Protocol):
    """File protocol"""

    @property
    def file_name(self) -> str:
        """Name of file."""
        pass

    async def read(self) -> bytes:
        """Returns the file content."""
        pass
