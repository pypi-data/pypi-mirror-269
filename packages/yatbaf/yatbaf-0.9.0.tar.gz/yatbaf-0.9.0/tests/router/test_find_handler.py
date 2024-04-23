import pytest

from yatbaf.enums import UpdateType
from yatbaf.filters import Command
from yatbaf.handler import Handler
from yatbaf.router import OnMessage


@pytest.mark.asyncio
async def test_empty_router(message):
    router = OnMessage()
    router.on_registration()
    assert await router._find_handler(message) is None


@pytest.mark.asyncio
async def test_handler_no_filters(message, handler_fn):
    handler = Handler(handler_fn, update_type="message")
    router = OnMessage(handlers=[handler])
    router.on_registration()
    assert await router._find_handler(message) is handler


@pytest.mark.asyncio
async def test_fallback_handler(message, handler_fn):
    fallback = Handler(handler_fn, update_type=UpdateType.MESSAGE)
    router = OnMessage(handlers=[fallback])

    @router(filters=[Command("foo")])
    async def cmd_foo(_):
        pass

    router.on_registration()
    message.text = "/bar"
    assert await router._find_handler(message) is fallback
