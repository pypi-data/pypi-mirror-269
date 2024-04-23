import pytest

from yatbaf.exceptions import FrozenInstanceError
from yatbaf.router import OnMessage


async def _guard_func(_):
    return


def test_init_guard_handler():
    router = OnMessage(handler_guards=[_guard_func])
    assert router._handler_guards == [_guard_func]


def test_init_guard_handler_local():
    router = OnMessage(handler_guards=[(_guard_func, "local")])
    assert router._handler_guards == [(_guard_func, "local")]


def test_init_guard_router():
    router = OnMessage(guards=[_guard_func])
    assert router._guards == [_guard_func]


def test_add_guard_handler():
    router = OnMessage()
    router.add_guard(_guard_func)
    assert router._handler_guards == [_guard_func]


def test_add_guard_handler_local():
    router = OnMessage()
    router.add_guard(_guard_func, scope="local")
    assert router._handler_guards == [(_guard_func, "local")]


def test_add_guard_router():
    router = OnMessage()
    router.add_guard(_guard_func, "router")
    assert router._guards == [_guard_func]


def test_add_guard_duplicate():
    router = OnMessage(
        handler_guards=[
            _guard_func,
            _guard_func,
        ],
    )
    assert router._handler_guards == [_guard_func, _guard_func]


def test_guard_decorator_handler():
    router = OnMessage()

    @router.guard
    async def guard(_):
        pass

    assert router._handler_guards == [guard]


def test_guard_decorator_handler_local():
    router = OnMessage()

    @router.guard("local")
    async def guard(_):
        pass

    assert router._handler_guards == [(guard, "local")]


def test_guard_decorator_router():
    router = OnMessage()

    @router.guard("router")
    async def guard(_):
        pass

    assert router._guards == [guard]


def test_frozen():
    router = OnMessage()
    router.on_registration()

    with pytest.raises(FrozenInstanceError):
        router.add_guard(_guard_func)

    with pytest.raises(FrozenInstanceError):

        @router.guard
        async def g_h(_):
            pass

    with pytest.raises(FrozenInstanceError):

        @router.guard("router")
        async def g_r(_):
            pass
