import pytest

from yatbaf.handler import Handler
from yatbaf.router import OnMessage


def test_resolve_guards(guard_false, guard_true):
    router = OnMessage(handler_guards=[guard_true])

    @router(guards=[guard_false])
    async def fn(_):
        pass

    handler = router._handlers[0]
    router.on_registration()
    assert handler._guards == [guard_true, guard_false]


def test_resolve_guards_local(guard_false, guard_true):
    router = OnMessage(
        handler_guards=[(guard_true, "local")],
        routers=[nested := OnMessage()],
    )

    @nested(guards=[guard_false])
    async def fn(_):
        pass

    handler = nested._handlers[0]
    router.on_registration()
    assert handler._guards == [guard_false]


@pytest.mark.asyncio
async def test_guard_true(update, handler_fn, guard_true, mock_mark):
    handler = Handler(
        fn=handler_fn,
        update_type=update.event_type,
        guards=[guard_true],
    )
    await handler.handle(update.event)
    mock_mark.assert_called_once_with(update.event)


@pytest.mark.asyncio
async def test_guard_false(update, handler_fn, guard_false, mock_mark):
    handler = Handler(
        fn=handler_fn,
        update_type=update.event_type,
        guards=[guard_false],
    )
    await handler.handle(update.event)
    mock_mark.assert_not_called()
