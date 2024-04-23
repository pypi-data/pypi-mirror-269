import pytest

from yatbaf.filters import User

USER_ID = 1212
USER_USERNAME = "test_user"


@pytest.fixture(autouse=True)
def _set_user_attrs(user):
    user.id = USER_ID
    user.username = USER_USERNAME


def test_priority():
    assert User(123).priority == {"sender": (1, 100)}
    assert User(123, 321).priority == {"sender": (2, 100)}


@pytest.mark.asyncio
@pytest.mark.parametrize("username", ("@test_user", "test_user", USER_ID))
async def test_true(message, username):
    assert await User(username).check(message)


@pytest.mark.asyncio
@pytest.mark.parametrize("username", ("@testuser", "test_user1", 23345678))
async def test_false(message, username):
    assert not await User(username).check(message)


@pytest.mark.asyncio
@pytest.mark.parametrize("username", ("@test_user", "test_user", USER_ID))
async def test_invert(message, username):
    assert not await (~User(username)).check(message)
