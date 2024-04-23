import asyncio
import sys
import unittest.mock as mock
from collections.abc import Iterator
from typing import Any

import pytest
from httpx import ConnectError

from yatbaf import LongPolling
from yatbaf.exceptions import RequestTimeoutError

MODULE = "yatbaf.long_polling"
module_obj = sys.modules[MODULE]


class AwaitableMock(mock.AsyncMock):

    def __await__(self) -> Iterator[Any]:
        self.await_count += 1
        return iter([])


@pytest.fixture
def asyncio_mock():
    asyncio_module = mock.Mock()
    asyncio_module.gather = mock.AsyncMock()
    asyncio_module.sleep = mock.AsyncMock()
    asyncio_module.wait_for = mock.AsyncMock()
    asyncio_module.CancelledError = asyncio.CancelledError
    return asyncio_module


@pytest.fixture(autouse=True)
def __mock(monkeypatch, asyncio_mock):
    monkeypatch.setattr(module_obj, "asyncio", asyncio_mock)


@pytest.fixture
def bot_mock():
    bot = mock.AsyncMock()
    bot._api_client = mock.Mock()
    bot._api_client.invoke = mock.AsyncMock()
    bot._api_client.close = mock.AsyncMock()
    return bot


@pytest.mark.asyncio
async def test_startup_running():
    polling = LongPolling(None)
    polling._running = True

    await polling._startup()


@pytest.mark.asyncio
async def test_startup():
    polling = LongPolling(None)

    await polling._startup()
    polling._event.clear.assert_called_once()
    assert polling._running


@pytest.mark.asyncio
async def test_startup_func(bot_mock):
    polling = LongPolling(
        bot_mock, on_startup=[
            mock.AsyncMock(),
            mock.AsyncMock(),
        ]
    )
    await polling._startup()
    for func in polling._on_startup:
        func.assert_awaited_once_with(bot_mock)


@pytest.mark.asyncio
async def test_startup_func_error(bot_mock):
    polling = LongPolling(
        bot_mock, on_startup=[
            mock.AsyncMock(side_effect=ValueError()),
        ]
    )
    with pytest.raises(ValueError):
        await polling._startup()
    assert not polling._running


@pytest.mark.asyncio
async def test_shutdown_not_running(bot_mock):
    polling = LongPolling(bot_mock)
    polling._running = False
    await polling._shutdown()
    bot_mock.shutdown.assert_not_awaited()


@pytest.mark.asyncio
async def test_shutdown_func(bot_mock):
    polling = LongPolling(
        bot_mock, on_shutdown=[
            mock.AsyncMock(),
            mock.AsyncMock(),
        ]
    )
    polling._running = True

    await polling._shutdown()
    bot_mock.shutdown.assert_awaited_once()
    for func in polling._on_shutdown:
        func.assert_awaited_once_with(bot_mock)


@pytest.mark.asyncio
async def test_shutdown_func_error(bot_mock):
    polling = LongPolling(
        bot_mock, on_shutdown=[
            mock.AsyncMock(side_effect=ValueError()),
        ]
    )
    polling._running = True
    with pytest.raises(ValueError):
        await polling._shutdown()
    bot_mock.shutdown.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_updates_params(bot_mock):
    polling = LongPolling(bot_mock)
    polling._event.is_set.side_effect = [False, True]
    result = mock.Mock(result=[])
    bot_mock._api_client.invoke.return_value = result
    queue = mock.Mock()

    await polling._get_updates(queue)
    queue.put_nowait.assert_not_called()
    bot_mock._api_client.invoke.assert_awaited_once_with(
        polling._method,
        timeout=(polling._method.timeout + 5),
    )


@pytest.mark.asyncio
async def test_get_updates(bot_mock):
    polling = LongPolling(bot_mock)
    polling._event.is_set.side_effect = [False, False, True]
    result = mock.Mock(result=[])
    bot_mock._api_client.invoke.return_value = result
    queue = mock.Mock()

    await polling._get_updates(queue)
    queue.put_nowait.assert_not_called()
    bot_mock._api_client.invoke.assert_awaited()
    assert bot_mock._api_client.invoke.call_count == 2


@pytest.mark.asyncio
async def test_get_updates_queue(bot_mock, update):
    polling = LongPolling(bot_mock)
    polling._event.is_set.side_effect = [False, True]
    result = mock.Mock(result=[object(), update])
    bot_mock._api_client.invoke.return_value = result
    queue = mock.Mock()

    await polling._get_updates(queue)
    queue.put_nowait.assert_called_once_with(result.result)
    bot_mock._api_client.invoke.assert_awaited_once()
    assert polling._method.offset == update.update_id + 1
    assert bot_mock._api_client.invoke.call_count == 1


@pytest.mark.asyncio
async def test_get_updates_timeout_error(bot_mock, asyncio_mock):
    bot_mock._error_handler = error_handler = mock.AsyncMock()
    polling = LongPolling(bot_mock)
    polling._event.is_set.side_effect = [False, False, True]
    result = mock.Mock(result=[])
    bot_mock._api_client.invoke.side_effect = [
        result, RequestTimeoutError("", None), result
    ]
    queue = mock.Mock()

    await polling._get_updates(queue)
    error_handler.on_error.assert_not_awaited()
    asyncio_mock.sleep.assert_awaited_once_with(polling._timeout_delay)
    assert bot_mock._api_client.invoke.call_count == 2


@pytest.mark.asyncio
async def test_get_updates_connection_error(bot_mock, asyncio_mock):
    bot_mock._error_handler = error_handler = mock.AsyncMock()
    polling = LongPolling(bot_mock)
    polling._event.is_set.side_effect = [False, False, True]
    result = mock.Mock(result=[])
    bot_mock._api_client.invoke.side_effect = [result, ConnectError(""), result]
    queue = mock.Mock()

    await polling._get_updates(queue)
    error_handler.on_error.assert_not_awaited()
    asyncio_mock.sleep.assert_awaited_once_with(polling._connection_delay)
    assert bot_mock._api_client.invoke.call_count == 2


@pytest.mark.asyncio
@pytest.mark.parametrize("result", [False, True])
async def test_get_updates_error(bot_mock, result):
    polling = LongPolling(
        bot_mock,
        on_error=(error_handler := mock.AsyncMock(return_value=result)),
    )
    polling._event = mock.Mock()
    polling._event.is_set.side_effect = [False, True]
    bot_mock._api_client.invoke.side_effect = exc = ValueError()
    queue = mock.Mock()
    await polling._get_updates(queue)
    error_handler.assert_awaited_once_with(exc)

    if result:
        polling._event.set.assert_not_called()
    else:
        polling._event.set.assert_called_once()


@pytest.mark.asyncio
async def test_main_loop(monkeypatch, bot_mock, asyncio_mock, update):
    tg = mock.AsyncMock()
    tg.__aenter__.return_value = tg
    tg.create_task = mock.Mock()
    asyncio_mock.TaskGroup.return_value = tg

    asyncio_mock.Queue.return_value = queue = mock.Mock()
    monkeypatch.setattr(  # yapf: disable
        LongPolling,
        "_get_updates",
        get_updates := mock.Mock(
            return_value=(
                get_updates_coro := object()
            )
        )
    )
    polling = LongPolling(bot_mock)
    polling._event.is_set.side_effect = [False, True]
    asyncio_mock.create_task.side_effect = [
        get_updates_task := AwaitableMock(cancel=mock.Mock()),
    ]
    bot_mock.process_update = mock.Mock(return_value=(coro := object()))
    asyncio_mock.wait_for.return_value = [update]
    await polling._main_loop()

    get_updates.assert_called_once_with(queue)
    asyncio_mock.create_task.assert_called_once_with(
        get_updates_coro,
        name="_get_updates",
    )
    get_updates_task.cancel.assert_called_once()
    get_updates_task.assert_awaited_once()
    tg.create_task.assert_called_once_with(coro, name=mock.ANY)


@pytest.mark.asyncio
async def test_run(monkeypatch):
    monkeypatch.setattr(LongPolling, "_startup", startup := mock.AsyncMock())
    monkeypatch.setattr(LongPolling, "_main_loop", loop := mock.AsyncMock())
    monkeypatch.setattr(LongPolling, "_shutdown", shutdown := mock.AsyncMock())

    polling = LongPolling(None)
    await polling._run()
    startup.assert_awaited_once()
    loop.assert_awaited_once()
    shutdown.assert_awaited_once()


@pytest.mark.asyncio
async def test_run_startup_error(monkeypatch):
    monkeypatch.setattr(
        LongPolling,
        "_startup",
        startup := mock.AsyncMock(side_effect=ValueError())
    )
    monkeypatch.setattr(LongPolling, "_main_loop", loop := mock.AsyncMock())
    monkeypatch.setattr(LongPolling, "_shutdown", shutdown := mock.AsyncMock())

    polling = LongPolling(None)
    await polling._run()
    assert not polling._running
    startup.assert_awaited_once()
    loop.assert_not_awaited()
    shutdown.assert_not_awaited()


def test_start(monkeypatch, asyncio_mock):
    monkeypatch.setattr(
        LongPolling,
        "_run",
        mock.Mock(return_value=(coro := mock.Mock())),
    )
    LongPolling(None).start()
    asyncio_mock.run.assert_called_once_with(coro)


def test_stop():
    polling = LongPolling(None)
    polling.stop()
    polling._event.set.assert_called_once()
