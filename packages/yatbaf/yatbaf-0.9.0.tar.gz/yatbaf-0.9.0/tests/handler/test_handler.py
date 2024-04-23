import unittest.mock as mock

import pytest

from yatbaf.enums import UpdateType
from yatbaf.filters import Chat
from yatbaf.handler import Handler


def test_new_hander(handler_fn):
    handler = Handler(handler_fn, update_type=UpdateType.MESSAGE)
    assert not handler._filters
    assert not handler._middleware
    assert handler._update_type is UpdateType.MESSAGE
    assert str(handler) == f"<Handler[type=message,id=0x{id(handler):x}]>"
    assert handler.fn is handler_fn


def test_on_registration(monkeypatch, handler_fn):
    monkeypatch.setattr(Handler, "_resolve_guards", rg := mock.Mock())
    monkeypatch.setattr(Handler, "_resolve_dependencies", rd := mock.Mock())
    monkeypatch.setattr(Handler, "_resolve_middleware", rm := mock.Mock())
    handler = Handler(handler_fn, "message")
    handler.on_registration()
    rg.assert_called_once()
    rm.assert_called_once()
    rd.assert_called_once()


async def fn(_):
    pass


def middleware(handler):

    async def wrapper(update):
        await handler(update)

    return wrapper


@pytest.mark.parametrize(
    "objs",
    [
        (
            Handler(fn=fn, update_type=UpdateType.MESSAGE),
            Handler(fn=fn, update_type=UpdateType.MESSAGE),
        ),
        (
            Handler(
                fn=fn,
                update_type=UpdateType.MESSAGE,
            ),
            Handler(
                fn=fn,
                update_type=UpdateType.MESSAGE,
                filters=[Chat("group")],
            ),
        ),
        (
            Handler(
                fn=fn,
                update_type=UpdateType.MESSAGE,
                middleware=[middleware],
            ),
            Handler(
                fn=fn,
                update_type=UpdateType.MESSAGE,
                middleware=[middleware],
            ),
        ),
    ]
)
def test_eq(objs):
    handler1, handler2 = objs
    assert handler1 == handler2


async def fn2(_):
    pass


@pytest.mark.parametrize("h1", [Handler(fn, update_type=UpdateType.MESSAGE)])
@pytest.mark.parametrize(
    "h2",
    [
        Handler(fn, update_type=UpdateType.EDITED_MESSAGE),
        Handler(fn, update_type=UpdateType.MESSAGE, middleware=[object()]),
        Handler(fn2, update_type=UpdateType.MESSAGE),
    ]
)
def test_not_eq(h1, h2):
    assert h1 != h2
