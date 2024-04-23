import time
import unittest.mock as mock

import pytest

from yatbaf.exceptions import GuardException
from yatbaf.types import Chat
from yatbaf.types import Message
from yatbaf.types import Update
from yatbaf.types import User


@pytest.fixture
def token():
    return "12345678:testtoken"


@pytest.fixture
def user():
    return User(
        id=1010,
        username="testuser",
        is_bot=False,
        first_name="Test",
    )


@pytest.fixture
def chat():
    return Chat(
        id=101010,
        type="group",
        username="testchat",
    )


@pytest.fixture
def message(chat, user):
    return Message(
        from_=user,
        chat=chat,
        date=int(time.time()),
        message_id=101010,
    )


@pytest.fixture
def update(message):
    return Update(
        update_id=9999,
        message=message,
    )


@pytest.fixture
def mock_mark():
    return mock.Mock()


@pytest.fixture
def handler_fn(mock_mark):

    async def fn(update):  # noqa: U100
        mock_mark(update)

    return fn


@pytest.fixture
def guard_true():

    async def fn(_):  # noqa: U101
        return

    return fn


@pytest.fixture
def guard_false():

    async def fn(_):  # noqa: U101
        raise GuardException

    return fn
