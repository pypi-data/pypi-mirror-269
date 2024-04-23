import pytest

from yatbaf.enums import AdminFlag
from yatbaf.helpers import create_bot_deeplink
from yatbaf.helpers import create_channel_deeplink
from yatbaf.helpers import create_game_deeplink
from yatbaf.helpers import create_group_deeplink
from yatbaf.helpers import create_user_link
from yatbaf.helpers import create_webapp_deeplink


@pytest.mark.parametrize("username", ("bot123", "user_bot"))
def test_create_user_link(username):
    assert create_user_link(username) == f"https://t.me/{username}"


@pytest.mark.parametrize("username", ("bot-123", "bt", "@bot"))
def test_create_user_link_error(username):
    with pytest.raises(ValueError):
        create_user_link(username)


@pytest.mark.parametrize("parameter", ("123-payload", None))
def test_create_bot_deeplink(parameter):
    bot_username = "username_bot"
    result = create_bot_deeplink(bot_username, parameter)
    if parameter is not None:
        assert result == f"https://t.me/{bot_username}?start={parameter}"
    else:
        assert result == f"https://t.me/{bot_username}"


def test_create_bot_deeplink_parameter_gt64():
    with pytest.raises(ValueError):
        create_bot_deeplink("botusername", "parameter" * 10)


@pytest.mark.parametrize("parameter", (
    "param@",
    "param&",
    ";;;",
    "foo bar",
))
def test_create_bot_deeplink_parameter_invalid_chars(parameter):
    with pytest.raises(ValueError):
        create_bot_deeplink("botusername", parameter)


def test_create_group_deeplink_empty():
    bot = "botusername"
    assert create_group_deeplink(bot) == f"https://t.me/{bot}?startgroup"


def test_create_group_deeplink_parameter():
    bot = "botusername"
    parameter = "parameter_123"
    assert (
        create_group_deeplink(bot, parameter) ==
        f"https://t.me/{bot}?startgroup={parameter}"
    )


def test_create_group_deeplink_parameter_empty():
    bot = "botusername"
    assert create_group_deeplink(bot, "") == f"https://t.me/{bot}?startgroup"


def test_create_group_deeplink_admin():
    bot = "botusername"
    flags = [AdminFlag.CHANGE_INFO, AdminFlag.EDIT_MESSAGES]
    assert (
        create_group_deeplink(bot, admin=flags) ==
        f"https://t.me/{bot}?startgroup&admin=change_info+edit_messages"
    )


def test_create_group_deeplink_admin_empty():
    bot = "botusername"
    assert (
        create_group_deeplink(bot, admin=[]) == f"https://t.me/{bot}?startgroup"
    )


def test_create_group_deeplink_parameter_admin():
    bot = "botusername"
    parameter = "param_foo-bar"
    flags = [
        AdminFlag.EDIT_MESSAGES,
        AdminFlag.INVITE_USERS,
        AdminFlag.DELETE_MESSAGES,
    ]
    assert (
        create_group_deeplink(bot, parameter, flags) == (
            f"https://t.me/{bot}?startgroup={parameter}"
            "&admin=edit_messages+invite_users+delete_messages"
        )
    )


def test_create_group_deeplink_parameter_error():
    with pytest.raises(ValueError):
        create_group_deeplink("botusername", "parameter#")


def test_create_channel_deeplink():
    bot = "botusername"
    flags = [
        AdminFlag.EDIT_MESSAGES,
        AdminFlag.DELETE_MESSAGES,
    ]
    assert (
        create_channel_deeplink(bot, flags) == (
            f"https://t.me/{bot}?startchannel"
            "&admin=edit_messages+delete_messages"
        )
    )


def test_create_channel_deeplink_admin_empty():
    with pytest.raises(ValueError):
        create_channel_deeplink("botusername", [])


def test_create_game_deeplink():
    bot = "botusername"
    game = "gameshortname"
    assert create_game_deeplink(bot, game) == f"https://t.me/{bot}?game={game}"


def test_create_game_deeplink_error():
    with pytest.raises(ValueError):
        create_game_deeplink("invalidbot#", "gameshortname")


def test_create_webapp_deeplink():
    bot = "botusername"
    webapp = "webappname"
    assert (
        create_webapp_deeplink(bot, webapp) ==
        f"https://t.me/{bot}/{webapp}?startapp"
    )


def test_create_webapp_deeplink_parameter():
    bot = "botusername"
    webapp = "webappname"
    parameter = "parameter"
    assert (
        create_webapp_deeplink(bot, webapp, parameter) ==
        f"https://t.me/{bot}/{webapp}?startapp={parameter}"
    )


def test_create_webapp_deeplink_parameter_empty():
    bot = "botusername"
    webapp = "webappname"
    parameter = ""
    assert (
        create_webapp_deeplink(bot, webapp, parameter) ==
        f"https://t.me/{bot}/{webapp}?startapp"
    )


def test_create_webapp_deeplink_parameter_error():
    with pytest.raises(ValueError):
        create_webapp_deeplink("botusername", "webapp", "invalidparam#")
