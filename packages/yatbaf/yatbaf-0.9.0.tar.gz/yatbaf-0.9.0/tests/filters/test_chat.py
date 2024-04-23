import pytest

from yatbaf.enums import ChatType
from yatbaf.filters import Chat
from yatbaf.filters import ChatId

CHAT_ID = 123232


@pytest.fixture(autouse=True)
def _set_chat_id(chat):
    chat.id = CHAT_ID


def test_priority():
    assert ChatId(123).priority == {"chat": (1, 150)}
    assert ChatId(123, 321).priority == {"chat": (2, 150)}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "t", [
        ChatType.GROUP,
        ChatType.SUPERGROUP,
        ChatType.PRIVATE,
        ChatType.CHANNEL,
    ]
)
async def test_chat_type(message, t):
    message.chat.type = t
    assert await Chat(t).check(message)


@pytest.mark.asyncio
async def test_chat_type_mix(message):
    message.chat.type = ChatType.GROUP
    assert await Chat("group", "channel").check(message)


@pytest.mark.asyncio
async def test_chat_id(message):
    assert await ChatId(CHAT_ID).check(message)
    assert await ChatId(CHAT_ID, 123).check(message)
