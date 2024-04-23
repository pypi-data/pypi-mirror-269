from __future__ import annotations

__all__ = (
    "Middleware",
    "chat_action",
)

import asyncio
from typing import TYPE_CHECKING
from typing import Any
from typing import Generic
from typing import TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable

    from .enums import ChatAction
    from .types import Message
    from .typing import HandlerCallableType
    from .typing import HandlerMiddleware

T = TypeVar("T")


class Middleware(Generic[T]):

    def __init__(
        self,
        obj: Callable[[T], T],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.obj = obj
        self.args = args
        self.kwargs = kwargs

    def __call__(self, obj: T) -> T:
        return self.obj(obj, *self.args, **self.kwargs)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Middleware) and (  # yapf: disable
            other is self or (
                other.obj is self.obj
                and other.args == self.args
                and other.kwargs == self.kwargs
            )
        )


def chat_action(action: ChatAction) -> HandlerMiddleware[Message]:
    """Send chat action and automatically update it if your operation takes
    more than 5 seconds to complete.

    Usage::

        @on_message(middleware=[chat_action(ChatAction.UPLOAD_PHOTO)])
        async def slow_operation(message: Message) -> None:
            ...

    See: :class:`ChatAction <yatbaf.enums.ChatAction>`

    :param action: Chat action.
    """

    def outer(
        handler: HandlerCallableType[Message]
    ) -> HandlerCallableType[Message]:

        async def inner(update: Message) -> None:
            event = asyncio.Event()

            async def _task() -> None:
                while not event.is_set():
                    await update.bot.send_chat_action(update.chat.id, action)
                    await asyncio.sleep(4.5)  # update status every 4.5 sec

            _ = asyncio.create_task(
                _task(), name=f"chat-action-{update.message_id}"
            )
            try:
                await handler(update)
            finally:
                event.set()

        return inner

    return outer
