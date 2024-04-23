import pytest

from yatbaf.dispatcher import Dispatcher
from yatbaf.handler import on_message


@on_message
async def _handler(update):
    update.ctx["test"].append("h")


handlers = {"message": _handler}


def create_middleware(mark):

    def middleware(handler):

        async def wrapper(update):
            update.event.ctx["test"].append(mark)
            await handler(update)

        return wrapper

    return middleware


@pytest.mark.asyncio
async def test_middleware(update):
    update.event.ctx["test"] = []
    dispatcher = Dispatcher(handlers, middleware=[create_middleware("m")])
    await dispatcher.resolve(update)
    assert update.event.ctx["test"] == ["m", "h"]


@pytest.mark.asyncio
async def test_middleware_order(update):
    update.event.ctx["test"] = []
    dispatcher = Dispatcher(
        handlers,
        middleware=[
            create_middleware(1),
            create_middleware(2),
            create_middleware(3),
        ]
    )
    await dispatcher.resolve(update)
    assert update.event.ctx["test"] == [1, 2, 3, "h"]
