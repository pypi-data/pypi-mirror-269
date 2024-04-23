from __future__ import annotations

__all__ = (
    "Handler",
    "on_message",
    "on_edited_message",
    "on_channel_post",
    "on_business_connection",
    "on_business_message",
    "on_edited_business_message",
    "on_deleted_business_messages",
    "on_edited_channel_post",
    "on_message_reaction",
    "on_message_reaction_count",
    "on_inline_query",
    "on_chosen_inline_result",
    "on_callback_query",
    "on_shipping_query",
    "on_pre_checkout_query",
    "on_poll",
    "on_poll_answer",
    "on_my_chat_member",
    "on_chat_member",
    "on_chat_join_request",
    "on_chat_boost",
    "on_removed_chat_boost",
)

from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import TypeAlias
from typing import final
from typing import overload

from .abc import AbstractHandler
from .di import Provide
from .di import create_dependency_batches
from .di import create_dependency_graph
from .di import get_parameters
from .di import is_reserved_key
from .di import resolve_dependencies
from .di import validate_provider
from .enums import UpdateType
from .exceptions import GuardException
from .filters.base import check_compatibility
from .filters.base import merge_priority
from .typing import UpdateT
from .utils import ensure_unique
from .utils import wrap_middleware

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Iterable
    from collections.abc import Sequence

    from .di import Dependency
    from .filters.base import BaseFilter
    from .types import BusinessConnection
    from .types import BusinessMessagesDeleted
    from .types import CallbackQuery
    from .types import ChatBoostRemoved
    from .types import ChatBoostUpdated
    from .types import ChatJoinRequest
    from .types import ChatMemberUpdated
    from .types import ChosenInlineResult
    from .types import InlineQuery
    from .types import Message
    from .types import MessageReactionCountUpdated
    from .types import MessageReactionUpdated
    from .types import Poll
    from .types import PollAnswer
    from .types import PreCheckoutQuery
    from .types import ShippingQuery
    from .typing import FilterPriority
    from .typing import HandlerCallable
    from .typing import HandlerGuard
    from .typing import HandlerMiddleware


class BaseHandler(AbstractHandler[UpdateT]):

    __slots__ = (
        "parent",
        "_guards",
        "_filters",
        "_middleware",
        "_filters",
        "_priority",
        "_dependencies",
    )

    parent: BaseHandler[UpdateT] | None

    def __init__(
        self,
        filters: Sequence[BaseFilter[UpdateT]] | None = None,
        guards: Sequence[HandlerGuard[UpdateT]] | None = None,
        middleware: Sequence[HandlerMiddleware[UpdateT]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> None:
        self.parent: BaseHandler[UpdateT] | None = None
        self._filters = tuple(filters or [])
        self._guards = list(guards or [])
        self._middleware = list(middleware or [])
        self._priority = ((0, (0, 0)), (0, (0, 0)), (0, (0, 0)))
        self._dependencies = dependencies or {}

    @final
    def __bool__(self) -> bool:
        return True

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, BaseHandler):
            return NotImplemented

        s_prior = self._priority
        o_prior = other._priority

        # priority (max, min) [content, sender, chat]
        sp = (s_prior[0][1], s_prior[1][1], s_prior[2][1])
        op = (o_prior[0][1], o_prior[1][1], o_prior[2][1])

        # priority max [content, sender, chat]
        sp_max = (sp[0][0], sp[1][0], sp[2][0])
        op_max = (op[0][0], op[1][0], op[2][0])

        # priority min [content, sender, chat]
        sp_min = (sp[0][1], sp[1][1], sp[2][1])
        op_min = (op[0][1], op[1][1], op[2][1])

        # number of filters [chat, sender, content]
        ss = (s_prior[2][0], s_prior[1][0], s_prior[0][0])
        os = (o_prior[2][0], o_prior[1][0], o_prior[0][0])

        if sp_max == op_max:
            if ss == os:
                return sp_min < op_min
            return ss < os
        return sp_max < op_max

    @final
    def __gt__(self, other: object) -> bool:  # noqa: U100
        return NotImplemented

    async def _check_guards(self, update: UpdateT) -> None:
        for guard in self._guards:
            await guard(update)

    async def match(self, update: UpdateT, /) -> bool:
        for filter in self._filters:
            if not await filter.check(update):
                return False
        return True

    def _resolve_middleware(self) -> None:
        self._middleware = ensure_unique(self._middleware)

    def _resolve_guards(self) -> None:
        self._guards = ensure_unique(self._guards)

    def _resolve_filters(self) -> None:
        check_compatibility(self._filters, False)
        self._parse_priority()

    def _parse_priority(self) -> None:
        data: FilterPriority = {}
        for filter in self._filters:
            data = merge_priority(data, filter.priority)

        tmp: list[tuple[int, tuple[int, int]]] = []
        for group in ("content", "sender", "chat"):
            if priority := data.get(group):  # type: ignore[call-overload]
                if isinstance(min_max := priority[1], int):
                    tmp.append((priority[0], (min_max, min_max)))
                else:
                    tmp.append(priority)
            else:
                tmp.append((0, (0, 0)))
        self._priority = tuple(tmp)  # type: ignore[assignment]

    def _get_guards(self) -> Iterable[HandlerGuard[UpdateT]]:
        return self._guards

    def _get_middleware(self) -> Iterable[HandlerMiddleware[UpdateT]]:
        return self._middleware

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        pass

    @property
    @abstractmethod
    def update_type(self) -> UpdateType:
        """Handler type."""

    @abstractmethod
    def on_registration(self) -> None:
        """Init handler."""


@final
class Handler(BaseHandler[UpdateT]):
    """Handler object."""

    __slots__ = (
        "_fn",
        "_update_type",
        "_middleware_stack",
        "_resolved_dependencies",
        "_kwargs",
    )

    def __init__(
        self,
        fn: HandlerCallable[UpdateT],
        update_type: UpdateType | str,
        *,
        filters: Sequence[BaseFilter[UpdateT]] | None = None,
        guards: Sequence[HandlerGuard[UpdateT]] | None = None,
        middleware: Sequence[HandlerMiddleware[UpdateT]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> None:
        """
        :param fn: Handler callback.
        :param update_type: Handler type. See :class:`~yatbaf.enums.UpdateType`
        :param filters: *Optional.* A sequence of :class:`~yatbaf.filters.base.BaseFilter`.
        :param guards: *Optional.* A sequence of :class:`~yatbaf.typing.HandlerGuard`.
        :param middleware: *Optional.* A sequence of :class:`~yatbaf.typing.HandlerMiddleware`.
        :param dependencies: *Optional.* A mapping of dependency providers.
        """  # noqa: E501
        super().__init__(
            filters=filters,
            guards=guards,
            middleware=middleware,
            dependencies=dependencies,
        )

        self._fn = fn
        self._update_type = UpdateType(update_type)
        self._middleware_stack: HandlerCallable[UpdateT] = self._handle
        self._kwargs = self._get_handler_kwargs(fn)
        self._resolved_dependencies: list[set[Dependency]] = []

    def __repr__(self) -> str:
        return f"<Handler[type={self._update_type!s},id=0x{id(self):x}]>"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Handler) and (  # yapf: disable
            other is self or (
                # type, callback and middleware is the same - handlers are
                # equal. filters don't matter.
                other._update_type == self._update_type
                and other._fn is self._fn
                and other._middleware == self._middleware
            )
        )

    @staticmethod
    def _get_handler_kwargs(fn: HandlerCallable[UpdateT]) -> set[str]:
        return set(get_parameters(fn)[1:])

    @property
    def update_type(self) -> UpdateType:
        """Handler type."""
        return self._update_type

    @property
    def fn(self) -> HandlerCallable[UpdateT]:
        """Original function."""
        return self._fn

    async def handle(self, update: UpdateT, /) -> None:
        await self._middleware_stack(update)

    async def _handle(self, update: UpdateT, /) -> None:
        try:
            if self._guards:
                await self._check_guards(update)
        except GuardException:
            return

        if not self._kwargs:
            await self._fn(update)
            return

        values = {"update": update}
        cg = await resolve_dependencies(self._resolved_dependencies, values)
        kwargs = {k: values[k] for k in self._kwargs}

        try:
            await self._fn(update, **kwargs)
        except Exception as e:
            await cg.throw(e)
            raise

        await cg.cleanup()

    @property
    def _parents(self) -> list[BaseHandler[UpdateT]]:
        result: list[BaseHandler[UpdateT]] = []
        parent: BaseHandler[UpdateT] | None = self
        while parent is not None:
            result.append(parent)
            parent = parent.parent
        return list(reversed(result))

    def _resolve_guards(self) -> None:
        guards: list[HandlerGuard[UpdateT]] = []
        for parent in self._parents:
            guards.extend(parent._get_guards())
        self._guards = ensure_unique(guards)

    def _resolve_middleware(self) -> None:
        middleware: list[HandlerMiddleware[UpdateT]] = []
        for parent in self._parents:
            middleware.extend(parent._get_middleware())
        self._middleware_stack = wrap_middleware(
            self._handle,
            ensure_unique(middleware),  # type: ignore[arg-type]
        )

    def _resolve_dependencies(self) -> None:
        if kwargs := self._kwargs:
            providers = self._get_dependency_providers()
            dependencies = set()
            for key in kwargs:
                if not is_reserved_key(key):
                    dependencies.add(create_dependency_graph(key, providers))
            batches = create_dependency_batches(dependencies)
            self._resolved_dependencies = batches

    def _get_dependency_providers(self) -> dict[str, Provide]:
        providers: dict[str, Provide] = {}
        for parent in self._parents:
            if (d := parent._dependencies) is not None:
                for k, v in d.items():
                    validate_provider(k, v, providers)
                    providers[k] = v
        return providers

    def on_registration(self) -> None:
        self._resolve_guards()
        self._resolve_middleware()
        self._resolve_filters()
        self._resolve_dependencies()


Wrapper: TypeAlias = "Callable[[HandlerCallable[UpdateT]], Handler[UpdateT]]"


@overload
def on_message(__fn: HandlerCallable[Message]) -> Handler[Message]:
    ...


@overload
def on_message(
    *,
    filters: Sequence[BaseFilter[Message]] | None = None,
    middleware: Sequence[HandlerMiddleware[Message]] | None = None,
    guards: Sequence[HandlerGuard[Message]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[Message]:
    ...


def on_message(
    __fn: HandlerCallable[Message] | None = None,
    *,
    filters: Sequence[BaseFilter[Message]] | None = None,
    middleware: Sequence[HandlerMiddleware[Message]] | None = None,
    guards: Sequence[HandlerGuard[Message]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[Message] | Handler[Message]:
    """Message handler decorator.

    Use this decorator to decorate handler for `message` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(fn: HandlerCallable[Message]) -> Handler[Message]:
        handler: Handler[Message] = Handler(
            fn=fn,
            update_type=UpdateType.MESSAGE,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_edited_message(__fn: HandlerCallable[Message]) -> Handler[Message]:
    ...


@overload
def on_edited_message(
    *,
    filters: Sequence[BaseFilter[Message]] | None = None,
    middleware: Sequence[HandlerMiddleware[Message]] | None = None,
    guards: Sequence[HandlerGuard[Message]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[Message]:
    ...


def on_edited_message(
    __fn: HandlerCallable[Message] | None = None,
    *,
    filters: Sequence[BaseFilter[Message]] | None = None,
    middleware: Sequence[HandlerMiddleware[Message]] | None = None,
    guards: Sequence[HandlerGuard[Message]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[Message] | Handler[Message]:
    """Edited message handler decorator.

    Use this decorator to decorate handler for `edited_message` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(fn: HandlerCallable[Message]) -> Handler[Message]:
        handler: Handler[Message] = Handler(
            fn=fn,
            update_type=UpdateType.EDITED_MESSAGE,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_message_reaction(
    __fn: HandlerCallable[MessageReactionUpdated]
) -> Handler[MessageReactionUpdated]:
    ...


@overload
def on_message_reaction(  # yapf: disable
    *,
    filters: Sequence[BaseFilter[MessageReactionUpdated]] | None = None,
    middleware: Sequence[HandlerMiddleware[MessageReactionUpdated]] | None = None,  # noqa: E501
    guards: Sequence[HandlerGuard[MessageReactionUpdated]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[MessageReactionUpdated]:
    ...


def on_message_reaction(  # yapf: disable
    __fn: HandlerCallable[MessageReactionUpdated] | None = None,
    *,
    filters: Sequence[BaseFilter[MessageReactionUpdated]] | None = None,
    middleware: Sequence[HandlerMiddleware[MessageReactionUpdated]] | None = None,  # noqa: E501
    guards: Sequence[HandlerGuard[MessageReactionUpdated]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[MessageReactionUpdated] | Handler[MessageReactionUpdated]:
    """Message reaction handler decorator.

    Use this decorator to decorate handler for `message_reaction` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(
        fn: HandlerCallable[MessageReactionUpdated]
    ) -> Handler[MessageReactionUpdated]:
        handler: Handler[MessageReactionUpdated] = Handler(
            fn=fn,
            update_type=UpdateType.MESSAGE_REACTION,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_message_reaction_count(
    __fn: HandlerCallable[MessageReactionCountUpdated]
) -> Handler[MessageReactionCountUpdated]:
    ...


@overload
def on_message_reaction_count(  # yapf: disable
    *,
    filters: Sequence[BaseFilter[MessageReactionCountUpdated]] | None = None,
    middleware: Sequence[HandlerMiddleware[MessageReactionCountUpdated]] | None = None,  # noqa: E501
    guards: Sequence[HandlerGuard[MessageReactionCountUpdated]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[MessageReactionCountUpdated]:
    ...


def on_message_reaction_count(  # yapf: disable
    __fn: HandlerCallable[MessageReactionCountUpdated] | None = None,
    *,
    filters: Sequence[BaseFilter[MessageReactionCountUpdated]] | None = None,
    middleware: Sequence[HandlerMiddleware[MessageReactionCountUpdated]] | None = None,  # noqa: E501
    guards: Sequence[HandlerGuard[MessageReactionCountUpdated]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[MessageReactionCountUpdated] | Handler[MessageReactionCountUpdated]:  # noqa: E501
    """Message reaction count handler decorator.

    Use this decorator to decorate handler for `message_reaction` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(
        fn: HandlerCallable[MessageReactionCountUpdated]
    ) -> Handler[MessageReactionCountUpdated]:
        handler: Handler[MessageReactionCountUpdated] = Handler(
            fn=fn,
            update_type=UpdateType.MESSAGE_REACTION_COUNT,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_channel_post(__fn: HandlerCallable[Message]) -> Handler[Message]:
    ...


@overload
def on_channel_post(
    *,
    filters: Sequence[BaseFilter[Message]] | None = None,
    middleware: Sequence[HandlerMiddleware[Message]] | None = None,
    guards: Sequence[HandlerGuard[Message]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[Message]:
    ...


def on_channel_post(
    __fn: HandlerCallable[Message] | None = None,
    *,
    filters: Sequence[BaseFilter[Message]] | None = None,
    middleware: Sequence[HandlerMiddleware[Message]] | None = None,
    guards: Sequence[HandlerGuard[Message]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[Message] | Handler[Message]:
    """Channel post handler decorator.

    Use this decorator to decorate handler for `channel_post` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(fn: HandlerCallable[Message]) -> Handler[Message]:
        handler: Handler[Message] = Handler(
            fn=fn,
            update_type=UpdateType.CHANNEL_POST,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_edited_channel_post(__fn: HandlerCallable[Message]) -> Handler[Message]:
    ...


@overload
def on_edited_channel_post(
    *,
    filters: Sequence[BaseFilter[Message]] | None = None,
    middleware: Sequence[HandlerMiddleware[Message]] | None = None,
    guards: Sequence[HandlerGuard[Message]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[Message]:
    ...


def on_edited_channel_post(
    __fn: HandlerCallable[Message] | None = None,
    *,
    filters: Sequence[BaseFilter[Message]] | None = None,
    middleware: Sequence[HandlerMiddleware[Message]] | None = None,
    guards: Sequence[HandlerGuard[Message]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[Message] | Handler[Message]:
    """Edited channel post handler decorator.

    Use this decorator to decorate handler for `edited_channel_post` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(fn: HandlerCallable[Message]) -> Handler[Message]:
        handler: Handler[Message] = Handler(
            fn=fn,
            update_type=UpdateType.EDITED_CHANNEL_POST,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_inline_query(__fn: HandlerCallable[InlineQuery]) -> Handler[InlineQuery]:
    ...


@overload
def on_inline_query(
    *,
    filters: Sequence[BaseFilter[InlineQuery]] | None = None,
    middleware: Sequence[HandlerMiddleware[InlineQuery]] | None = None,
    guards: Sequence[HandlerGuard[InlineQuery]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[InlineQuery]:
    ...


def on_inline_query(
    __fn: HandlerCallable[InlineQuery] | None = None,
    *,
    filters: Sequence[BaseFilter[InlineQuery]] | None = None,
    middleware: Sequence[HandlerMiddleware[InlineQuery]] | None = None,
    guards: Sequence[HandlerGuard[InlineQuery]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[InlineQuery] | Handler[InlineQuery]:
    """Inline query handler decorator.

    Use this decorator to decorate handler for `inline_query` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(fn: HandlerCallable[InlineQuery]) -> Handler[InlineQuery]:
        handler: Handler[InlineQuery] = Handler(
            fn=fn,
            update_type=UpdateType.INLINE_QUERY,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_chosen_inline_result(
    __fn: HandlerCallable[ChosenInlineResult]
) -> Handler[ChosenInlineResult]:
    ...


@overload
def on_chosen_inline_result(
    *,
    filters: Sequence[BaseFilter[ChosenInlineResult]] | None = None,
    middleware: Sequence[HandlerMiddleware[ChosenInlineResult]] | None = None,
    guards: Sequence[HandlerGuard[ChosenInlineResult]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[ChosenInlineResult]:
    ...


def on_chosen_inline_result(
    __fn: HandlerCallable[ChosenInlineResult] | None = None,
    *,
    filters: Sequence[BaseFilter[ChosenInlineResult]] | None = None,
    middleware: Sequence[HandlerMiddleware[ChosenInlineResult]] | None = None,
    guards: Sequence[HandlerGuard[ChosenInlineResult]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[ChosenInlineResult] | Handler[ChosenInlineResult]:
    """Chosen inline result handler decorator.

    Use this decorator to decorate handler for `chosen_inline_result` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(
        fn: HandlerCallable[ChosenInlineResult]
    ) -> Handler[ChosenInlineResult]:
        handler: Handler[ChosenInlineResult] = Handler(
            fn=fn,
            update_type=UpdateType.CHOSEN_INLINE_RESULT,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_callback_query(
    __fn: HandlerCallable[CallbackQuery]
) -> Handler[CallbackQuery]:
    ...


@overload
def on_callback_query(
    *,
    filters: Sequence[BaseFilter[CallbackQuery]] | None = None,
    middleware: Sequence[HandlerMiddleware[CallbackQuery]] | None = None,
    guards: Sequence[HandlerGuard[CallbackQuery]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[CallbackQuery]:
    ...


def on_callback_query(
    __fn: HandlerCallable[CallbackQuery] | None = None,
    *,
    filters: Sequence[BaseFilter[CallbackQuery]] | None = None,
    middleware: Sequence[HandlerMiddleware[CallbackQuery]] | None = None,
    guards: Sequence[HandlerGuard[CallbackQuery]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[CallbackQuery] | Handler[CallbackQuery]:
    """Callback query handler decorator.

    Use this decorator to decorate handler for `callback_query` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(fn: HandlerCallable[CallbackQuery]) -> Handler[CallbackQuery]:
        handler: Handler[CallbackQuery] = Handler(
            fn=fn,
            update_type=UpdateType.CALLBACK_QUERY,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_shipping_query(
    __fn: HandlerCallable[ShippingQuery]
) -> Handler[ShippingQuery]:
    ...


@overload
def on_shipping_query(
    *,
    filters: Sequence[BaseFilter[ShippingQuery]] | None = None,
    middleware: Sequence[HandlerMiddleware[ShippingQuery]] | None = None,
    guards: Sequence[HandlerGuard[ShippingQuery]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[ShippingQuery]:
    ...


def on_shipping_query(
    __fn: HandlerCallable[ShippingQuery] | None = None,
    *,
    filters: Sequence[BaseFilter[ShippingQuery]] | None = None,
    middleware: Sequence[HandlerMiddleware[ShippingQuery]] | None = None,
    guards: Sequence[HandlerGuard[ShippingQuery]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[ShippingQuery] | Handler[ShippingQuery]:
    """Shipping query handler decorator.

    Use this decorator to decorate handler for `shipping_query` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(fn: HandlerCallable[ShippingQuery]) -> Handler[ShippingQuery]:
        handler: Handler[ShippingQuery] = Handler(
            fn=fn,
            update_type=UpdateType.SHIPPING_QUERY,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_pre_checkout_query(
    __fn: HandlerCallable[PreCheckoutQuery]
) -> Handler[PreCheckoutQuery]:
    ...


@overload
def on_pre_checkout_query(
    *,
    filters: Sequence[BaseFilter[PreCheckoutQuery]] | None = None,
    middleware: Sequence[HandlerMiddleware[PreCheckoutQuery]] | None = None,
    guards: Sequence[HandlerGuard[PreCheckoutQuery]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[PreCheckoutQuery]:
    ...


def on_pre_checkout_query(
    __fn: HandlerCallable[PreCheckoutQuery] | None = None,
    *,
    filters: Sequence[BaseFilter[PreCheckoutQuery]] | None = None,
    middleware: Sequence[HandlerMiddleware[PreCheckoutQuery]] | None = None,
    guards: Sequence[HandlerGuard[PreCheckoutQuery]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[PreCheckoutQuery] | Handler[PreCheckoutQuery]:
    """Pre-checkout query handler decorator.

    Use this decorator to decorate handler for `pre_checkout_query` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(
        fn: HandlerCallable[PreCheckoutQuery]
    ) -> Handler[PreCheckoutQuery]:
        handler: Handler[PreCheckoutQuery] = Handler(
            fn=fn,
            update_type=UpdateType.PRE_CHECKOUT_QUERY,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_poll(__fn: HandlerCallable[Poll]) -> Handler[Poll]:
    ...


@overload
def on_poll(
    *,
    filters: Sequence[BaseFilter[Poll]] | None = None,
    middleware: Sequence[HandlerMiddleware[Poll]] | None = None,
    guards: Sequence[HandlerGuard[Poll]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[Poll]:
    ...


def on_poll(
    __fn: HandlerCallable[Poll] | None = None,
    *,
    filters: Sequence[BaseFilter[Poll]] | None = None,
    middleware: Sequence[HandlerMiddleware[Poll]] | None = None,
    guards: Sequence[HandlerGuard[Poll]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[Poll] | Handler[Poll]:
    """Poll handler decorator.

    Use this decorator to decorate handler for `poll` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(fn: HandlerCallable[Poll]) -> Handler[Poll]:
        handler: Handler[Poll] = Handler(
            fn=fn,
            update_type=UpdateType.POLL,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_poll_answer(__fn: HandlerCallable[PollAnswer]) -> Handler[PollAnswer]:
    ...


@overload
def on_poll_answer(
    *,
    filters: Sequence[BaseFilter[PollAnswer]] | None = None,
    middleware: Sequence[HandlerMiddleware[PollAnswer]] | None = None,
    guards: Sequence[HandlerGuard[PollAnswer]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[PollAnswer]:
    ...


def on_poll_answer(
    __fn: HandlerCallable[PollAnswer] | None = None,
    *,
    filters: Sequence[BaseFilter[PollAnswer]] | None = None,
    middleware: Sequence[HandlerMiddleware[PollAnswer]] | None = None,
    guards: Sequence[HandlerGuard[PollAnswer]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[PollAnswer] | Handler[PollAnswer]:
    """Poll answer handler decorator.

    Use this decorator to decorate handler for `poll_answer` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(fn: HandlerCallable[PollAnswer]) -> Handler[PollAnswer]:
        handler: Handler[PollAnswer] = Handler(
            fn=fn,
            update_type=UpdateType.POLL_ANSWER,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_my_chat_member(
    __fn: HandlerCallable[ChatMemberUpdated]
) -> Handler[ChatMemberUpdated]:
    ...


@overload
def on_my_chat_member(
    *,
    filters: Sequence[BaseFilter[ChatMemberUpdated]] | None = None,
    middleware: Sequence[HandlerMiddleware[ChatMemberUpdated]] | None = None,
    guards: Sequence[HandlerGuard[ChatMemberUpdated]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[ChatMemberUpdated]:
    ...


def on_my_chat_member(
    __fn: HandlerCallable[ChatMemberUpdated] | None = None,
    *,
    filters: Sequence[BaseFilter[ChatMemberUpdated]] | None = None,
    middleware: Sequence[HandlerMiddleware[ChatMemberUpdated]] | None = None,
    guards: Sequence[HandlerGuard[ChatMemberUpdated]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[ChatMemberUpdated] | Handler[ChatMemberUpdated]:
    """My chat member handler decorator.

    Use this decorator to decorate handler for `my_chat_member` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(
        fn: HandlerCallable[ChatMemberUpdated]
    ) -> Handler[ChatMemberUpdated]:
        handler: Handler[ChatMemberUpdated] = Handler(
            fn=fn,
            update_type=UpdateType.MY_CHAT_MEMBER,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_chat_member(
    __fn: HandlerCallable[ChatMemberUpdated]
) -> Handler[ChatMemberUpdated]:
    ...


@overload
def on_chat_member(
    *,
    filters: Sequence[BaseFilter[ChatMemberUpdated]] | None = None,
    middleware: Sequence[HandlerMiddleware[ChatMemberUpdated]] | None = None,
    guards: Sequence[HandlerGuard[ChatMemberUpdated]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[ChatMemberUpdated]:
    ...


def on_chat_member(
    __fn: HandlerCallable[ChatMemberUpdated] | None = None,
    *,
    filters: Sequence[BaseFilter[ChatMemberUpdated]] | None = None,
    middleware: Sequence[HandlerMiddleware[ChatMemberUpdated]] | None = None,
    guards: Sequence[HandlerGuard[ChatMemberUpdated]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[ChatMemberUpdated] | Handler[ChatMemberUpdated]:
    """Chat member handler decorator.

    Use this decorator to decorate handler for `chat_member` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(
        fn: HandlerCallable[ChatMemberUpdated]
    ) -> Handler[ChatMemberUpdated]:
        handler: Handler[ChatMemberUpdated] = Handler(
            fn=fn,
            update_type=UpdateType.CHAT_MEMBER,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_chat_join_request(
    __fn: HandlerCallable[ChatJoinRequest]
) -> Handler[ChatJoinRequest]:
    ...


@overload
def on_chat_join_request(
    *,
    filters: Sequence[BaseFilter[ChatJoinRequest]] | None = None,
    middleware: Sequence[HandlerMiddleware[ChatJoinRequest]] | None = None,
    guards: Sequence[HandlerGuard[ChatJoinRequest]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[ChatJoinRequest]:
    ...


def on_chat_join_request(
    __fn: HandlerCallable[ChatJoinRequest] | None = None,
    *,
    filters: Sequence[BaseFilter[ChatJoinRequest]] | None = None,
    middleware: Sequence[HandlerMiddleware[ChatJoinRequest]] | None = None,
    guards: Sequence[HandlerGuard[ChatJoinRequest]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[ChatJoinRequest] | Handler[ChatJoinRequest]:
    """Chat join request handler decorator.

    Use this decorator to decorate handler for `chat_join_request` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(
        fn: HandlerCallable[ChatJoinRequest]
    ) -> Handler[ChatJoinRequest]:
        handler: Handler[ChatJoinRequest] = Handler(
            fn=fn,
            update_type=UpdateType.CHAT_JOIN_REQUEST,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_chat_boost(
    __fn: HandlerCallable[ChatBoostUpdated]
) -> Handler[ChatBoostUpdated]:
    ...


@overload
def on_chat_boost(
    *,
    filters: Sequence[BaseFilter[ChatBoostUpdated]] | None = None,
    middleware: Sequence[HandlerMiddleware[ChatBoostUpdated]] | None = None,
    guards: Sequence[HandlerGuard[ChatBoostUpdated]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[ChatBoostUpdated]:
    ...


def on_chat_boost(
    __fn: HandlerCallable[ChatBoostUpdated] | None = None,
    *,
    filters: Sequence[BaseFilter[ChatBoostUpdated]] | None = None,
    middleware: Sequence[HandlerMiddleware[ChatBoostUpdated]] | None = None,
    guards: Sequence[HandlerGuard[ChatBoostUpdated]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[ChatBoostUpdated] | Handler[ChatBoostUpdated]:
    """Chat boost handler decorator.

    Use this decorator to decorate handler for `chat_boost` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(
        fn: HandlerCallable[ChatBoostUpdated]
    ) -> Handler[ChatBoostUpdated]:
        handler: Handler[ChatBoostUpdated] = Handler(
            fn=fn,
            update_type=UpdateType.CHAT_BOOST,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_removed_chat_boost(
    __fn: HandlerCallable[ChatBoostRemoved]
) -> Handler[ChatBoostRemoved]:
    ...


@overload
def on_removed_chat_boost(
    *,
    filters: Sequence[BaseFilter[ChatBoostRemoved]] | None = None,
    middleware: Sequence[HandlerMiddleware[ChatBoostRemoved]] | None = None,
    guards: Sequence[HandlerGuard[ChatBoostRemoved]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[ChatBoostRemoved]:
    ...


def on_removed_chat_boost(
    __fn: HandlerCallable[ChatBoostRemoved] | None = None,
    *,
    filters: Sequence[BaseFilter[ChatBoostRemoved]] | None = None,
    middleware: Sequence[HandlerMiddleware[ChatBoostRemoved]] | None = None,
    guards: Sequence[HandlerGuard[ChatBoostRemoved]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[ChatBoostRemoved] | Handler[ChatBoostRemoved]:
    """Removed chat boost handler decorator.

    Use this decorator to decorate handler for `removed_chat_boost` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(
        fn: HandlerCallable[ChatBoostRemoved]
    ) -> Handler[ChatBoostRemoved]:
        handler: Handler[ChatBoostRemoved] = Handler(
            fn=fn,
            update_type=UpdateType.REMOVED_CHAT_BOOST,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_business_connection(
    __fn: HandlerCallable[BusinessConnection]
) -> Handler[BusinessConnection]:
    ...


@overload
def on_business_connection(
    *,
    filters: Sequence[BaseFilter[BusinessConnection]] | None = None,
    middleware: Sequence[HandlerMiddleware[BusinessConnection]] | None = None,
    guards: Sequence[HandlerGuard[BusinessConnection]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[BusinessConnection]:
    ...


def on_business_connection(
    __fn: HandlerCallable[BusinessConnection] | None = None,
    *,
    filters: Sequence[BaseFilter[BusinessConnection]] | None = None,
    middleware: Sequence[HandlerMiddleware[BusinessConnection]] | None = None,
    guards: Sequence[HandlerGuard[BusinessConnection]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[BusinessConnection] | Handler[BusinessConnection]:
    """Business connection handler decorator.

    Use this decorator to decorate handler for `business_connection` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(
        fn: HandlerCallable[BusinessConnection]
    ) -> Handler[BusinessConnection]:
        handler: Handler[BusinessConnection] = Handler(
            fn=fn,
            update_type=UpdateType.BUSINESS_CONNECTION,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_business_message(__fn: HandlerCallable[Message]) -> Handler[Message]:
    ...


@overload
def on_business_message(
    *,
    filters: Sequence[BaseFilter[Message]] | None = None,
    middleware: Sequence[HandlerMiddleware[Message]] | None = None,
    guards: Sequence[HandlerGuard[Message]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[Message]:
    ...


def on_business_message(
    __fn: HandlerCallable[Message] | None = None,
    *,
    filters: Sequence[BaseFilter[Message]] | None = None,
    middleware: Sequence[HandlerMiddleware[Message]] | None = None,
    guards: Sequence[HandlerGuard[Message]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[Message] | Handler[Message]:
    """Business message handler decorator.

    Use this decorator to decorate handler for `business_message` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(fn: HandlerCallable[Message]) -> Handler[Message]:
        handler: Handler[Message] = Handler(
            fn=fn,
            update_type=UpdateType.BUSINESS_MESSAGE,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_edited_business_message(
    __fn: HandlerCallable[Message]
) -> Handler[Message]:
    ...


@overload
def on_edited_business_message(
    *,
    filters: Sequence[BaseFilter[Message]] | None = None,
    middleware: Sequence[HandlerMiddleware[Message]] | None = None,
    guards: Sequence[HandlerGuard[Message]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[Message]:
    ...


def on_edited_business_message(
    __fn: HandlerCallable[Message] | None = None,
    *,
    filters: Sequence[BaseFilter[Message]] | None = None,
    middleware: Sequence[HandlerMiddleware[Message]] | None = None,
    guards: Sequence[HandlerGuard[Message]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[Message] | Handler[Message]:
    """Edited business message handler decorator.

    Use this decorator to decorate handler for `edited_business_message` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(fn: HandlerCallable[Message]) -> Handler[Message]:
        handler: Handler[Message] = Handler(
            fn=fn,
            update_type=UpdateType.EDITED_BUSINESS_MESSAGE,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_deleted_business_messages(
    __fn: HandlerCallable[BusinessMessagesDeleted]
) -> Handler[BusinessMessagesDeleted]:
    ...


@overload
def on_deleted_business_messages(  # yapf: disable
    *,
    filters: Sequence[BaseFilter[BusinessMessagesDeleted]] | None = None,
    middleware: Sequence[HandlerMiddleware[BusinessMessagesDeleted]] | None = None,  # noqa: E501
    guards: Sequence[HandlerGuard[BusinessMessagesDeleted]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[BusinessMessagesDeleted]:
    ...


def on_deleted_business_messages(  # yapf: disable
    __fn: HandlerCallable[BusinessMessagesDeleted] | None = None,
    *,
    filters: Sequence[BaseFilter[BusinessMessagesDeleted]] | None = None,
    middleware: Sequence[HandlerMiddleware[BusinessMessagesDeleted]] | None = None,  # noqa: E501
    guards: Sequence[HandlerGuard[BusinessMessagesDeleted]] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Wrapper[BusinessMessagesDeleted] | Handler[BusinessMessagesDeleted]:
    """Deleted business messages handler decorator.

    Use this decorator to decorate handler for `deleted_business_messages` update.

    See :class:`Handler` for parameters.
    """  # noqa: E501

    def wrapper(
        fn: HandlerCallable[BusinessMessagesDeleted]
    ) -> Handler[BusinessMessagesDeleted]:
        handler: Handler[BusinessMessagesDeleted] = Handler(
            fn=fn,
            update_type=UpdateType.DELETED_BUSINESS_MESSAGES,
            filters=filters,
            middleware=middleware,
            guards=guards,
            dependencies=dependencies,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)
