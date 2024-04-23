from __future__ import annotations

__all__ = (
    "OnMessage",
    "OnEditedMessage",
    "OnChannelPost",
    "OnEditedChannelPost",
    "OnBusinessConnection",
    "OnBusinessMessage",
    "OnEditedBusinessMessage",
    "OnDeletedBusinessMessages",
    "OnMessageReaction",
    "OnMessageReactionCount",
    "OnInlineQuery",
    "OnChosenInlineResult",
    "OnCallbackQuery",
    "OnShippingQuery",
    "OnPreCheckoutQuery",
    "OnPoll",
    "OnPollAnswer",
    "OnMyChatMember",
    "OnChatMember",
    "OnChatJoinRequest",
    "OnChatBoost",
    "OnRemovedChatBoost",
)

from collections import defaultdict
from itertools import count
from typing import TYPE_CHECKING
from typing import Any
from typing import Final
from typing import TypeVar
from typing import cast
from typing import final
from typing import overload

from .enums import UpdateType
from .exceptions import FrozenInstanceError
from .exceptions import GuardException
from .handler import BaseHandler
from .handler import Handler
from .middleware import Middleware
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
from .typing import UpdateT
from .utils import wrap_middleware
from .warnings import warn_duplicate

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Iterable
    from collections.abc import Iterator
    from collections.abc import Sequence

    from .di import Provide
    from .filters.base import BaseFilter
    from .typing import HandlerCallable
    from .typing import HandlerCallableType
    from .typing import HandlerGuard
    from .typing import HandlerMiddleware
    from .typing import Handlers
    from .typing import MiddlewareCallable
    from .typing import Scope

_router_count = count(1).__next__


class Router(BaseHandler[UpdateT]):
    """Base class for routers."""

    __slots__ = (
        "_name",
        "_frozen",
        "_routers",
        "_handlers",
        "_handler_guards",
        "_handler_middleware",
        "_middleware_stack",
        "_sort_handlers",
        "_sort_routers",
        "_exclude_locals",
        "_stop_propagate",
    )

    def __init__(  # yapf: disable
        self,
        *,
        filters: Sequence[BaseFilter[UpdateT]] | None = None,
        handlers: Sequence[Handler[UpdateT]] | None = None,
        dependencies: dict[str, Provide] | None = None,
        handler_guards: Sequence[HandlerGuard[UpdateT] | tuple[HandlerGuard[UpdateT], Scope]] | None = None,  # noqa: E501
        handler_middleware: Sequence[HandlerMiddleware[UpdateT] | tuple[HandlerMiddleware[UpdateT], Scope]] | None = None,  # noqa: E501
        routers: Sequence[Router[UpdateT]] | None = None,
        guards: Sequence[HandlerGuard[UpdateT]] | None = None,
        middleware: Sequence[HandlerMiddleware[UpdateT]] | None = None,
        name: str | None = None,
        sort_handlers: bool = True,
        sort_routers: bool = True,
        stop_propagate: bool | None = None,
    ) -> None:
        """
        :param handlers: *Optional.* A sequence of :class:`~yatbaf.typing.Handler`.
        :param dependencies: *Optional.* A mapping of dependency providers.
        :param handler_guards: *Optional.* A sequence of :class:`~yatbaf.typing.HandlerGuard`.
        :param handler_middleware: *Optional.* A sequence of :class:`~yatbaf.typing.HandlerMiddleware`.
        :param routers: *Optional.* A sequence of :class:`Router`.
        :param guards: *Optional.* A sequence of :class:`~yatbaf.typing.HandlerGuard`.
        :param middleware: *Optional.* A sequence of :class:`~yatbaf.typing.HandlerMiddleware`.
        :param name: *Optional.* Router name.
        :param sort_handlers: *Optional.* Pass ``False``, if you don't want to
            sort handlers.
        :param sort_routers: *Optional.* Pass ``False``, if you don't want to
            sort routers.
        :param stop_propagate: *Optional.* Pass ``True`` to stop propagate to
            next router even if no handler is found. Default ``bool(filters)``.
        """  # noqa: E501
        super().__init__(
            filters=filters,
            guards=guards,
            middleware=middleware,
            dependencies=dependencies,
        )

        self._name: Final[str] = name if name else f"router-{_router_count()}"
        self._frozen = False
        self._exclude_locals = False
        self._middleware_stack: HandlerCallableType[UpdateT] = self._handle
        self._sort_handlers = sort_handlers
        self._sort_routers = sort_routers
        self._stop_propagate = (
            stop_propagate if stop_propagate is not None else bool(filters)
        )

        self._handler_guards = list(handler_guards or [])
        self._handler_middleware = list(handler_middleware or [])

        self._handlers: list[Handler[UpdateT]] = []
        for handler in (handlers or []):
            self.add_handler(handler)

        self._routers: list[Router[UpdateT]] = []
        for router in (routers or []):
            self.add_router(router)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}[name={self._name}]>"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Router) and (  # yapf: disable
            other is self or (
                other.update_type == self.update_type
                and other._handlers == self._handlers
                and other._handler_guards == self._handler_guards
                and other._handler_middleware == self._handler_middleware
                and other._routers == self._routers
                and other._guards == self._guards
                and other._middleware == self._middleware
                and other._dependencies == self._dependencies
            )
        )

    @property
    def name(self) -> str:
        """Router name."""
        return self._name

    def add_guard(
        self, obj: HandlerGuard[UpdateT], /, scope: Scope = "handler"
    ) -> None:
        """Add a new guard.

        :param obj: :class:`~yatbaf.typing.HandlerGuard` object.
        :param scope: *Optional.* Scope of guard.
        :raises FrozenInstanceError: If you try to register a Guard after Bot
            object has been initialized.
        """
        if self._frozen:
            raise FrozenInstanceError(
                "It is not possible to add a new Guard at runtime "
                "after Bot object has been initialized."
            )

        if scope == "router":
            self._guards.append(obj)
        else:
            self._handler_guards.append(
                obj if scope != "local" else (obj, "local")
            )

    def add_middleware(  # yapf: disable
        self, obj: HandlerMiddleware[UpdateT], /, scope: Scope = "handler"
    ) -> None:
        """Add a new middleware.

        Usage::

            def middleware(handler: HandlerCallableType[UpdateT]) -> HandlerCallableType[UpdateT]:
                async def wrapper(update: UpdateT) -> None:
                    await handler(update)
                return wrapper

            router.add_middleware(middleware)

        :param obj: :class:`~yatbaf.typing.HandlerMiddleware` object.
        :param scope: *Optional.* Scope of middleware.
        :raises FrozenInstanceError: If you try to register a Middleware after
            Bot object has been initialized.
        """  # noqa: E501
        if self._frozen:
            raise FrozenInstanceError(
                "It is not possible to add a new Middleware at runtime "
                "after Bot object has been initialized."
            )

        if scope == "router":
            self._middleware.append(obj)
        else:
            self._handler_middleware.append(
                obj if scope != "local" else (obj, "local")
            )

    @overload
    def add_handler(self, handler: Handler[UpdateT], /) -> None:
        ...

    @overload
    def add_handler(
        self,
        handler: HandlerCallable[UpdateT],
        *,
        filters: Sequence[BaseFilter[UpdateT]] | None = None,
        middleware: Sequence[HandlerMiddleware[UpdateT]] | None = None,
        guards: Sequence[HandlerGuard[UpdateT]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> None:
        ...

    def add_handler(
        self,
        handler: HandlerCallable[UpdateT] | Handler[UpdateT],
        *,
        filters: Sequence[BaseFilter[UpdateT]] | None = None,
        middleware: Sequence[HandlerMiddleware[UpdateT]] | None = None,
        guards: Sequence[HandlerGuard[UpdateT]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> None:
        """Use this method to register a new handler.

        :param handler: :class:`~yatbaf.handler.Handler` or :class:`~yatbaf.typing.HandlerCallable`.
        :param filters: *Optional.* A sequence of :class:`~yatbaf.filters.base.BaseFilter`.
        :param middleware: *Optional.* A sequence of :class:`~yatbaf.typing.HandlerMiddleware`.
        :param guards: *Optional.* A sequence of :class:`~yatbaf.typing.HandlerGuard`.
        :param dependencies: *Optional.* A mapping of dependency providers.
        :raises FrozenInstanceError: If you try to register a Handler after Bot
            object has been initialized.
        """  # noqa: E501
        if self._frozen:
            raise FrozenInstanceError(
                f"{self!r} is frozen. It is not possible to add a new Handler "
                "at runtime after Bot object has been initialized."
            )

        if not isinstance(handler, Handler):
            handler = Handler(
                fn=handler,
                update_type=self.update_type,
                filters=filters,
                middleware=middleware,
                guards=guards,
                dependencies=dependencies,
            )

        self._validate_handler(handler)
        if handler.parent or (handler in self._handlers):
            warn_duplicate(handler, self)
            return

        self._handlers.append(handler)
        handler.parent = self

    def add_router(self, router: Router[UpdateT], /) -> None:
        """Use this method to add a nested router.

        .. warning::

            The nested router must handle the same type of updates as the
            current one.

        :param router: Instance of :class:`Router`
        :raises ValueError: If ``router`` already registered in another router
            or router type is different.
        :raises FrozenInstanceError: If you try to register a Router after Bot
            object has been initialized.
        """
        if self._frozen:
            raise FrozenInstanceError(
                f"{self!r} is frozen. It is not possible to add a new Router "
                "at runtime after Bot object has been initialized."
            )

        self._validate_router(router)
        if router.parent or (router in self._routers):
            warn_duplicate(router, self)
            return

        self._routers.append(router)
        router.parent = self

    def _validate_router(self, router: Router[UpdateT]) -> None:
        if router is self:
            raise ValueError(f"It is not possible to add {router!r} to itself.")
        if self.update_type != router.update_type:
            raise ValueError(
                f"Incompatible type! Cannot add {router!r} to {self!r}"
            )
        if (parent := router.parent) and parent is not self:
            raise ValueError(f"{router!r} already registered in {parent!r}")

    def _validate_handler(self, handler: Handler[UpdateT]) -> None:
        if handler.update_type != self.update_type:
            raise ValueError(
                f"Incompatible type! Cannot add {handler!r} to {self!r}"
            )
        if (parent := handler.parent) and parent is not self:
            raise ValueError(f"{handler!r} alredy registered in {parent!r}")

    @overload
    def __call__(  # yapf: disable
        self, __fn: HandlerCallable[UpdateT], /
    ) -> HandlerCallable[UpdateT]:
        ...

    @overload
    def __call__(
        self,
        *,
        filters: Sequence[BaseFilter[UpdateT]] | None = None,
        middleware: Sequence[HandlerMiddleware[UpdateT]] | None = None,
        guards: Sequence[HandlerGuard[UpdateT]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> MiddlewareCallable[HandlerCallable[UpdateT]]:
        ...

    def __call__(  # yapf: disable
        self,
        __fn: HandlerCallable[UpdateT] | None = None,
        *,
        filters: Sequence[BaseFilter[UpdateT]] | None = None,
        middleware: Sequence[HandlerMiddleware[UpdateT]] | None = None,
        guards: Sequence[HandlerGuard[UpdateT]] | None = None,
        dependencies: dict[str, Provide] | None = None,
    ) -> MiddlewareCallable[HandlerCallable[UpdateT]] | HandlerCallable[UpdateT]:  # noqa: E501
        """Handler decorator.

        See :meth:`add_handler`.

        Use this decorator to register a new handler::

            @router
            async def handler(message):
                # handle any message
                ...


            @router(filters=[Command("foo")])
            async def handler(message):
                # handle command `/foo`
                ...
        """

        def wrapper(fn: HandlerCallable[UpdateT]) -> HandlerCallable[UpdateT]:
            self.add_handler(
                handler=fn,
                filters=filters,
                middleware=middleware,
                guards=guards,
                dependencies=dependencies,
            )
            return fn

        if __fn is not None:
            return wrapper(__fn)
        return wrapper

    # yapf: disable
    @overload
    def middleware(
        self, __fn: HandlerMiddleware[UpdateT], /
    ) -> HandlerMiddleware[UpdateT]:
        ...

    @overload
    def middleware(
        self, __scope: Scope = ..., /, *args: Any, **kwargs: Any
    ) -> MiddlewareCallable[HandlerMiddleware[UpdateT]]:
        ...

    def middleware(
        self,
        __fn_scope: HandlerMiddleware[UpdateT] | Scope = "handler", /,
        *args: Any,
        **kwargs: Any,
    ) -> MiddlewareCallable[HandlerMiddleware[UpdateT]] | HandlerMiddleware[UpdateT]:  # noqa: E501
        """Middleware decorator.

        Use this decorator to register a new middleware::

            @router.middleware
            def middleware(handler: HandlerCallableType[Message]) -> HandlerCallableType[Message]:
                async def wrapper(message: Message) -> None:
                    await handler(message)
                return wrapper


            @router.middleware("handler", 1, y=2)
            def middleware(handler: HandlerCallableType[Message], x, y) -> HandlerCallableType[Message]:
                async def wrapper(message: Message) -> None:
                    log.info(f"{x=}, {y=}")
                    await handler(message)
                return wrapper
        """  # noqa: E501
        # yapf: enable

        def wrapper(
            fn: HandlerMiddleware[UpdateT]
        ) -> HandlerMiddleware[UpdateT]:
            scope: Scope = __fn_scope  # type: ignore[assignment]
            if args or kwargs:
                self.add_middleware(Middleware(fn, *args, **kwargs), scope)
            else:
                self.add_middleware(fn, scope)
            return fn

        if not isinstance(__fn_scope, str):
            fn = __fn_scope
            __fn_scope = "handler"
            return wrapper(fn)
        return wrapper

    # yapf: disable
    @overload
    def guard(self, __fn: HandlerGuard[UpdateT], /) -> HandlerGuard[UpdateT]:
        ...

    @overload
    def guard(
        self, __scope: Scope = ..., /
    ) -> Callable[[HandlerGuard[UpdateT]], HandlerGuard[UpdateT]]:
        ...

    def guard(
        self, __fn_scope: HandlerGuard[UpdateT] | Scope = "handler"
    ) -> HandlerGuard[UpdateT] | Callable[[HandlerGuard[UpdateT]], HandlerGuard[UpdateT]]:  # noqa: E501
        """Guard decorator.

        Use this decorator to register a guard for handlers or router::

            users = [...]

            @router.guard
            async def guard(message: Message) -> None:
                if message.from_.id not in users:
                    raise GuardException


            @router.guard("router")
            async def guard(message: Message) -> None:
                if message.from_.id not in users:
                    raise GuardException
        """
        # yapf: enable

        def wrapper(fn: HandlerGuard[UpdateT]) -> HandlerGuard[UpdateT]:
            scope: Scope = __fn_scope  # type: ignore[assignment]
            self.add_guard(fn, scope)
            return fn

        if not isinstance(__fn_scope, str):
            fn = __fn_scope
            __fn_scope = "handler"
            return wrapper(fn)
        return wrapper

    async def _find_handler(self, update: UpdateT) -> Handler[UpdateT] | None:
        for handler in self._handlers:
            if await handler.match(update):
                return handler
        return None

    async def _handle(self, update: UpdateT, /) -> None:
        try:
            if self._guards:
                await self._check_guards(update)
        except GuardException:
            update.__usrctx__["handled"] = self._stop_propagate
            return

        if handler := await self._find_handler(update):
            update.__usrctx__["handled"] = True
            await handler.handle(update)
            return

        for router in self._routers:
            await router.handle(update)
            if update.__usrctx__["handled"]:
                return

        # skip other routers
        update.__usrctx__["handled"] = self._stop_propagate

    async def handle(self, update: UpdateT, /) -> None:
        update.__usrctx__["handled"] = False
        if not self._filters or await self.match(update):
            await self._middleware_stack(update)

    def _get_guards(self) -> Iterable[HandlerGuard[UpdateT]]:
        return _unpack(self._handler_guards, self._exclude_locals)

    def _get_middleware(self) -> Iterable[HandlerMiddleware[UpdateT]]:
        return _unpack(self._handler_middleware, self._exclude_locals)

    def _prepare_handlers(self) -> None:
        for handler in self._handlers:
            handler.on_registration()

        if self._sort_handlers:
            self._handlers.sort(reverse=True)
        self._exclude_locals = True

    def _prepare_routers(self) -> None:
        for router in self._routers:
            router.on_registration()

        if self._sort_routers:
            self._routers.sort(reverse=True)

    def on_registration(self) -> None:
        self._resolve_filters()
        self._prepare_handlers()
        self._resolve_guards()
        self._resolve_middleware()
        self._prepare_routers()

        self._middleware_stack = wrap_middleware(
            self._handle,
            self._middleware,  # type: ignore[arg-type]
        )
        self._frozen = True


T = TypeVar("T")


def _unpack(
    objs: Sequence[T | tuple[T, str]],
    exclude_local: bool = False,
) -> Iterator[T]:
    for obj in objs:
        scope = ""
        if isinstance(obj, tuple):
            obj, scope = obj
            if scope == "local" and exclude_local:
                continue
        yield cast("T", obj)


@final
class OnMessage(Router[Message]):
    """message router.

    See :attr:`Update.message <yatbaf.types.update.Update.message>`
    """

    __slots__ = ()
    update_type: UpdateType = UpdateType.MESSAGE


@final
class OnEditedMessage(Router[Message]):
    """edited_message router.

    See :attr:`Update.edited_message <yatbaf.types.update.Update.edited_message>`
    """  # noqa: E501

    __slots__ = ()
    update_type: UpdateType = UpdateType.EDITED_MESSAGE


@final
class OnChannelPost(Router[Message]):
    """channel_post router.

    See :attr:`Update.channel_post <yatbaf.types.update.Update.channel_post>`
    """

    __slots__ = ()
    update_type: UpdateType = UpdateType.CHANNEL_POST


@final
class OnEditedChannelPost(Router[Message]):
    """edited_channel_post router.

    See :attr:`Update.edited_channel_post <yatbaf.types.update.Update.edited_channel_post>`
    """  # noqa: E501

    __slots__ = ()
    update_type: UpdateType = UpdateType.EDITED_CHANNEL_POST


@final
class OnBusinessConnection(Router[BusinessConnection]):
    """business_connection router.

    See :attr:`~yatbaf.types.update.Update.business_connection`
    """  # noqa: E501

    __slots__ = ()
    update_type: UpdateType = UpdateType.BUSINESS_CONNECTION


@final
class OnBusinessMessage(Router[Message]):
    """business_message router.

    See :attr:`~yatbaf.types.update.Update.business_message`
    """  # noqa: E501

    __slots__ = ()
    update_type: UpdateType = UpdateType.BUSINESS_MESSAGE


@final
class OnEditedBusinessMessage(Router[Message]):
    """edited_business_message router.

    See :attr:`~yatbaf.types.update.Update.edited_business_message`
    """  # noqa: E501

    __slots__ = ()
    update_type: UpdateType = UpdateType.EDITED_BUSINESS_MESSAGE


@final
class OnDeletedBusinessMessages(Router[BusinessMessagesDeleted]):
    """deleted_business_messages router.

    See :attr:`~yatbaf.types.update.Update.deleted_business_messages`
    """  # noqa: E501

    __slots__ = ()
    update_type: UpdateType = UpdateType.DELETED_BUSINESS_MESSAGES


@final
class OnMessageReaction(Router[MessageReactionUpdated]):
    """message_reaction router.

    See :attr:`Update.message_reaction <yatbaf.types.update.Update.message_reaction>`
    """  # noqa: E501

    __slots__ = ()
    update_type: UpdateType = UpdateType.MESSAGE_REACTION


@final
class OnMessageReactionCount(Router[MessageReactionCountUpdated]):
    """message_reaction router.

    See :attr:`Update.message_reaction_count <yatbaf.types.update.Update.message_reaction_count>`
    """  # noqa: E501

    __slots__ = ()
    update_type: UpdateType = UpdateType.MESSAGE_REACTION_COUNT


@final
class OnInlineQuery(Router[InlineQuery]):
    """inline_query router.

    See :attr:`Update.inline_query <yatbaf.types.update.Update.inline_query>`
    """

    __slots__ = ()
    update_type: UpdateType = UpdateType.INLINE_QUERY


@final
class OnChosenInlineResult(Router[ChosenInlineResult]):
    """chosen_inline_result router.

    See :attr:`Update.chosen_inline_result <yatbaf.types.update.Update.chosen_inline_result>`
    """  # noqa: E501

    __slots__ = ()
    update_type: UpdateType = UpdateType.CHOSEN_INLINE_RESULT


@final
class OnCallbackQuery(Router[CallbackQuery]):
    """callback_query router.

    See :attr:`Update.callback_query <yatbaf.types.update.Update.callback_query>`
    """  # noqa: E501

    __slots__ = ()
    update_type: UpdateType = UpdateType.CALLBACK_QUERY


@final
class OnShippingQuery(Router[ShippingQuery]):
    """shipping_query router.

    See :attr:`Update.shipping_query <yatbaf.types.update.Update.shipping_query>`
    """  # noqa: E501

    __slots__ = ()
    update_type: UpdateType = UpdateType.SHIPPING_QUERY


@final
class OnPreCheckoutQuery(Router[PreCheckoutQuery]):
    """pre_checkout_query router.

    See :attr:`Update.pre_checkout_query <yatbaf.types.update.Update.pre_checkout_query>`
    """  # noqa: E501

    __slots__ = ()
    update_type: UpdateType = UpdateType.PRE_CHECKOUT_QUERY


@final
class OnPoll(Router[Poll]):
    """poll router.

    See :attr:`Update.poll <yatbaf.types.update.Update.poll>`
    """

    __slots__ = ()
    update_type: UpdateType = UpdateType.POLL


@final
class OnPollAnswer(Router[PollAnswer]):
    """poll_answer router.

    See :attr:`Update.poll_answer <yatbaf.types.update.Update.poll_answer>`
    """

    __slots__ = ()
    update_type: UpdateType = UpdateType.POLL_ANSWER


@final
class OnMyChatMember(Router[ChatMemberUpdated]):
    """my_chat_member router.

    See :attr:`Update.my_chat_member <yatbaf.types.update.Update.my_chat_member>`
    """  # noqa: E501

    __slots__ = ()
    update_type: UpdateType = UpdateType.MY_CHAT_MEMBER


@final
class OnChatMember(Router[ChatMemberUpdated]):
    """chat_member router.

    See :attr:`Update.chat_member <yatbaf.types.update.Update.chat_member>`
    """

    __slots__ = ()
    update_type: UpdateType = UpdateType.CHAT_MEMBER


@final
class OnChatJoinRequest(Router[ChatJoinRequest]):
    """chat_join_request router.

    See :attr:`Update.chat_join_request <yatbaf.types.update.Update.chat_join_request>`
    """  # noqa: E501

    __slots__ = ()
    update_type: UpdateType = UpdateType.CHAT_JOIN_REQUEST


@final
class OnChatBoost(Router[ChatBoostUpdated]):
    """chat_boost router.

    See :attr:`Update.chat_boost <yatbaf.types.update.Update.chat_boost>`
    """  # noqa: E501

    __slots__ = ()
    update_type: UpdateType = UpdateType.CHAT_BOOST


@final
class OnRemovedChatBoost(Router[ChatBoostRemoved]):
    """removed_chat_boost router.

    See :attr:`Update.removed_chat_boost <yatbaf.types.update.Update.removed_chat_boost>`
    """  # noqa: E501

    __slots__ = ()
    update_type: UpdateType = UpdateType.REMOVED_CHAT_BOOST


_router_map: dict[str, type[Router]] = {
    "message": OnMessage,
    "edited_message": OnEditedMessage,
    "channel_post": OnChannelPost,
    "edited_channel_post": OnEditedChannelPost,
    "business_connection": OnBusinessConnection,
    "business_message": OnBusinessMessage,
    "edited_business_message": OnEditedBusinessMessage,
    "deleted_business_messages": OnDeletedBusinessMessages,
    "message_reaction": OnMessageReaction,
    "message_reaction_count": OnMessageReactionCount,
    "inline_query": OnInlineQuery,
    "chosen_inline_result": OnChosenInlineResult,
    "callback_query": OnCallbackQuery,
    "shipping_query": OnShippingQuery,
    "pre_checkout_query": OnPreCheckoutQuery,
    "poll": OnPoll,
    "poll_answer": OnPollAnswer,
    "my_chat_member": OnMyChatMember,
    "chat_member": OnChatMember,
    "chat_join_request": OnChatJoinRequest,
    "chat_boost": OnChatBoost,
    "removed_chat_boost": OnRemovedChatBoost,
}


def parse_handlers(
    *,
    handlers: Sequence[Handler] | None = None,
    routers: Sequence[Router] | None = None,
    dependencies: dict[str, Provide] | None = None,
) -> Handlers:
    """:meta private:"""
    handlers = list(handlers or [])
    routers = list(routers or [])
    dependencies = dependencies or {}
    if not handlers and not routers:
        raise ValueError("You must use at least one handler or router.")

    # yapf: disable
    tmp: dict[str, tuple[list[Handler], list[Router]]] = (
        defaultdict(lambda: ([], []))
    )
    # yapf: enable
    for handler_ in handlers:
        tmp[handler_.update_type][0].append(handler_)

    for router_ in routers:
        tmp[router_.update_type][1].append(router_)

    result = {}
    for type_, (h, r) in tmp.items():
        router: BaseHandler
        if h:
            router = _router_map[type_](
                handlers=h,
                routers=r,
                dependencies=dependencies,
            )
        elif r:
            if len(r) == 1:
                router = r[0]
                router._dependencies = {
                    **dependencies,
                    **router._dependencies,
                }
            else:
                router = _router_map[type_](
                    routers=r,
                    dependencies=dependencies,
                )
        result[type_] = router
        router.on_registration()

    return cast("Handlers", result)
