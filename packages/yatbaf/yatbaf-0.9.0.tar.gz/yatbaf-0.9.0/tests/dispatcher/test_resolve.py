import pytest

from yatbaf.dispatcher import Dispatcher
from yatbaf.handler import Handler
from yatbaf.router import OnMessage
from yatbaf.router import OnPoll


@pytest.mark.asyncio
async def test_resolve(handler_fn, update, mock_mark):
    router = OnMessage(handlers=[Handler(handler_fn, "message")])
    router.on_registration()

    dispatcher = Dispatcher(handlers={"message": router})
    await dispatcher.resolve(update)
    mock_mark.assert_called_once_with(update.event)


@pytest.mark.asyncio
async def test_resolve_none(handler_fn, update, mock_mark):
    dispatcher = Dispatcher(
        handlers={"poll": OnPoll(handlers=[Handler(handler_fn, "poll")])}
    )
    await dispatcher.resolve(update)
    mock_mark.assert_not_called()
