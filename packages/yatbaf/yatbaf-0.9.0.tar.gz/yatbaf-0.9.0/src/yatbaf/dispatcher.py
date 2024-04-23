from __future__ import annotations

__all__ = ("Dispatcher",)

import logging
from typing import TYPE_CHECKING

from .abc import AbstractRouter
from .exceptions import GuardException
from .utils import ensure_unique
from .utils import wrap_middleware

if TYPE_CHECKING:
    from collections.abc import Sequence

    from .types import Update
    from .typing import Handlers
    from .typing import RouterGurad
    from .typing import RouterMiddleware

log = logging.getLogger(__name__)


class Dispatcher(AbstractRouter):
    """Dispatcher object."""

    __slots__ = (
        "_handlers",
        "_guards",
        "_middleware_stack",
    )

    def __init__(
        self,
        handlers: Handlers,
        guards: Sequence[RouterGurad] | None = None,
        middleware: Sequence[RouterMiddleware] | None = None,
    ) -> None:
        """
        :param handlers: Handlers map.
        :param guards: *Optional.* A sequence of :class:`~yatbaf.typing.RouterGurad`.
        :param middleware: *Optional.* A sequence of :class:`~yatbaf.typing.RouterMiddleware`.
        """  # noqa: E501
        self._handlers: Handlers = handlers
        self._guards = ensure_unique(guards or [])
        self._middleware_stack = wrap_middleware(
            self._resolve,
            ensure_unique(middleware or []),  # type: ignore[arg-type]
        )

    async def _check_guards(self, update: Update) -> None:
        for fn in self._guards:
            await fn(update)

    async def _resolve(self, update: Update, /) -> None:
        if handler := self._handlers.get(update.event_type):
            try:
                if self._guards:
                    await self._check_guards(update)
            except GuardException:
                return

            await handler.handle(update.event)  # type: ignore[attr-defined]

    async def resolve(self, update: Update, /) -> None:
        await self._middleware_stack(update)
