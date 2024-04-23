import pytest

from yatbaf import filters as f
from yatbaf.router import OnMessage


@pytest.mark.asyncio
async def test_filters_true(message, user):
    user.id = 123
    router = OnMessage(filters=[f.User(123)])

    @router
    async def handler(message):
        message.ctx["test"] = True

    router.on_registration()
    await router.handle(message)
    assert message.ctx.get("test", False)


@pytest.mark.asyncio
async def test_filters_false(message, user):
    user.id = 321
    router = OnMessage(filters=[f.User(123)])

    @router
    async def handler(message):
        message.ctx["test"] = True

    router.on_registration()
    await router.handle(message)
    assert not message.ctx.get("test", False)
