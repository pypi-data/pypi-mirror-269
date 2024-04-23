import pytest

from yatbaf.dispatcher import Dispatcher
from yatbaf.handler import Handler


@pytest.mark.asyncio
async def test_resolve_guard_false(guard_false, handler_fn, update, mock_mark):

    dispatcher = Dispatcher(
        handlers={"message": Handler(handler_fn, "message")},
        guards=[guard_false],
    )
    await dispatcher.resolve(update)
    mock_mark.assert_not_called()


@pytest.mark.asyncio
async def test_resolve_guard_true(guard_true, handler_fn, update, mock_mark):
    dispatcher = Dispatcher(
        handlers={"message": Handler(handler_fn, "message")},
        guards=[guard_true],
    )
    await dispatcher.resolve(update)
    mock_mark.assert_called_once_with(update.event)
