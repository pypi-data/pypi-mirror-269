import pytest

from yatbaf.handler import Handler
from yatbaf.router import OnMessage


def create_middleware(mark):

    def middleware(handler):

        async def wrapper(update):
            update.ctx["test"].append(mark)
            await handler(update)

        return wrapper

    return middleware


def create_callback(mark):

    async def handler(update):
        update.ctx["test"].append(mark)

    return handler


def test_resolve_middleware():
    mdlw1 = create_middleware(1)
    mdlw2 = create_middleware(2)

    router = OnMessage(
        middleware=[
            mdlw1,
            mdlw2,
            mdlw2,
        ],
    )
    router._resolve_middleware()
    assert router._middleware == [mdlw1, mdlw2]


@pytest.mark.asyncio
async def test_router_middleware_order(message):
    message.ctx["test"] = []
    router = OnMessage(
        handlers=[Handler(create_callback("h"), "message")],
        middleware=[create_middleware(f"rm{i}") for i in range(5)],
    )
    router.on_registration()
    await router.handle(message)
    assert message.ctx["test"] == [f"rm{i}" for i in range(5)] + ["h"]


@pytest.mark.asyncio
async def test_handler_middleware_order(message):
    message.ctx["test"] = []
    router = OnMessage(
        handlers=[Handler(create_callback("h"), update_type="message")],
        handler_middleware=[create_middleware(f"hm{i}") for i in range(5)],
    )
    router.on_registration()
    await router.handle(message)
    assert message.ctx["test"] == [f"hm{i}" for i in range(5)] + ["h"]


@pytest.mark.asyncio
async def test_router_handler_middleware_order(message):
    message.ctx["test"] = []
    router = OnMessage(
        handlers=[Handler(create_callback("h"), update_type="message")],
        handler_middleware=[create_middleware(f"hm{i}") for i in range(5)],
        middleware=[create_middleware(f"rm{i}") for i in range(5)],
    )
    router.on_registration()
    await router.handle(message)
    assert message.ctx["test"] == (  # yapf: disable
        [f"rm{i}" for i in range(5)] + [f"hm{i}" for i in range(5)] + ["h"]
    )
