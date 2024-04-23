import pytest


def test_bind_bot_obj(message):
    bot = object()
    message._bind_bot_obj(bot)
    assert message.bot is bot
    assert message.from_.bot is bot
    assert message.chat.bot is bot


def test_bot_not_bound(message):
    with pytest.raises(RuntimeError):
        message.bot
