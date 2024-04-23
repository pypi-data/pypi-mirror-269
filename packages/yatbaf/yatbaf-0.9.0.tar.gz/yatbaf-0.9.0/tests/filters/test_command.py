import pytest

from yatbaf.filters import Command


def test_empty():
    with pytest.raises(ValueError):
        Command()


def test_priority():
    assert Command("foo").priority == {"content": (1, 1000)}
    assert Command("foo", "bar").priority == {"content": (2, 1000)}


@pytest.mark.asyncio
async def test_true(message):
    message.text = "/ping"
    assert await Command("ping").check(message)


@pytest.mark.asyncio
async def test_false(message):
    message.text = "/pong"
    assert not await Command("ping").check(message)


@pytest.mark.asyncio
async def test_mix_true(message):
    message.text = "/pong"
    assert await Command("ping", "pong").check(message)


@pytest.mark.asyncio
async def test_text_is_none(message):
    message.text = None
    assert not await Command("ping").check(message)


@pytest.mark.asyncio
@pytest.mark.parametrize("filter", ["start", "/start", "START", "Start"])
async def test_case(message, filter):
    message.text = "/start"
    assert await Command(filter).check(message)
