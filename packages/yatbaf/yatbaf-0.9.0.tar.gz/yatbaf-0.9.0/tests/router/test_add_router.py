import pytest

from yatbaf.exceptions import BotWarning
from yatbaf.exceptions import FrozenInstanceError
from yatbaf.handler import Handler
from yatbaf.router import OnMessage
from yatbaf.router import OnPoll


def test_init():
    router = OnMessage(routers=[nested := OnMessage()])
    assert router._routers == [nested]
    assert nested.parent is router


def test_add_router():
    router = OnMessage()
    nested = OnMessage()
    router.add_router(nested)
    assert router._routers == [nested]
    assert nested.parent is router


def test_add_router_self():
    router = OnMessage()
    with pytest.raises(ValueError):
        router.add_router(router)


def test_add_router_wrong_type():
    router = OnMessage()
    with pytest.raises(ValueError):
        router.add_router(OnPoll())


def test_add_router_registered():
    _ = OnMessage(
        routers=[
            nested := OnMessage(),
        ],
    )
    router2 = OnMessage()
    with pytest.raises(ValueError):
        router2.add_router(nested)


def test_add_router_duplicate_same_obj():
    router = OnMessage(
        routers=[
            nested := OnMessage(),
        ],
    )
    with pytest.warns(BotWarning):
        router.add_router(nested)
    assert router._routers == [nested]


def test_add_router_duplicate_equal_obj():

    async def fn(_):
        pass

    router = OnMessage(
        routers=[nested := OnMessage(handlers=[Handler(fn, "message")])]
    )
    dup = OnMessage(handlers=[Handler(fn, "message")])
    with pytest.warns(BotWarning):
        router.add_router(dup)
    assert router._routers == [nested]


def test_add_router_frozen():
    router = OnMessage()
    router.on_registration()
    with pytest.raises(FrozenInstanceError):
        router.add_router(OnMessage())
