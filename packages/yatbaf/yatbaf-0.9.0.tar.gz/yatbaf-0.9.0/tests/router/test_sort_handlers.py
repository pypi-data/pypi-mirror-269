from yatbaf import filters as f
from yatbaf.handler import on_message
from yatbaf.router import OnMessage


def test_fallback():

    @on_message
    async def any_message(_):
        pass

    @on_message(filters=[f.Command("foo"), f.Chat("private")])
    async def foo_private(_):
        pass

    @on_message(filters=[f.Command("foo")])
    async def foo_any(_):
        pass

    router = OnMessage(handlers=[
        any_message,
        foo_any,
        foo_private,
    ])

    assert router._handlers == [
        any_message,
        foo_any,
        foo_private,
    ]

    router.on_registration()
    assert router._handlers == [
        foo_private,
        foo_any,
        any_message,
    ]
