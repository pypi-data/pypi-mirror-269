import pytest

from yatbaf.handler import on_message
from yatbaf.router import OnMessage


@pytest.fixture(autouse=True)
def __init_message(message):
    message.ctx["test"] = []


def create_handler(mark):

    @on_message
    async def handler(msg):
        msg.ctx["test"].append(mark)

    return handler


def test_resolve_guards(guard_true, guard_false):
    router = OnMessage(
        guards=[
            guard_true,
            guard_false,
            guard_true,
            guard_true,
        ]
    )
    router._resolve_guards()
    assert router._guards == [guard_true, guard_false]


@pytest.mark.asyncio
async def test_guard_false(message, guard_false):
    router = OnMessage(
        guards=[guard_false],
        handlers=[create_handler(1)],
    )
    router.on_registration()
    await router.handle(message)
    assert message.ctx["test"] == []


@pytest.mark.asyncio
async def test_guard_true(message, guard_true):
    router = OnMessage(
        guards=[guard_true],
        handlers=[create_handler(1)],
    )
    router.on_registration()
    await router.handle(message)
    assert message.ctx["test"] == [1]


@pytest.mark.asyncio
async def test_parent_guard_true(message, guard_true):
    router = OnMessage(
        guards=[guard_true],
        handlers=[create_handler(1)],
        routers=[OnMessage(handlers=[create_handler(2)])],
    )
    router.on_registration()
    await router.handle(message)
    assert message.ctx["test"] == [1]


@pytest.mark.asyncio
async def test_parent_guard_false(message, guard_false):
    router = OnMessage(
        handlers=[create_handler(1)],
        guards=[guard_false],
        routers=[OnMessage(handlers=[create_handler(2)])]
    )
    router.on_registration()
    await router.handle(message)
    assert message.ctx["test"] == []


@pytest.mark.asyncio
async def test_guard_false_both(message, guard_false):
    router = OnMessage(
        guards=[guard_false],
        handlers=[create_handler(1)],
        routers=[
            OnMessage(
                guards=[guard_false],
                handlers=[create_handler(2)],
            ),
        ],
    )
    router.on_registration()
    await router.handle(message)
    assert message.ctx["test"] == []
