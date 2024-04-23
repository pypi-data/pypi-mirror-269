import random

import pytest

from yatbaf import filters as f
from yatbaf.handler import on_message


def create_handler(filters=None):

    @on_message(filters=filters)
    async def handler(_):
        pass

    handler.on_registration()
    return handler


fallback = create_handler()

command = create_handler([f.Command("foo")])
command2 = create_handler([f.Command("foo", "bar")])
command_or_text = create_handler([f.Command("foo") | f.Text(startswith="foo")])
command_chat = create_handler([f.Command("foo"), f.Chat("group")])

text = create_handler([f.Text(startswith="hello")])
text2 = create_handler([
    f.Text(
        startswith="hello",
        endswith="world",
    ),
])
text2_any = create_handler([
    f.Text(
        startswith="hello",
        endswith="world",
        any_=True,
    )
])
text3_any = create_handler([
    f.Text(
        startswith="hello",
        endswith="world",
        match="hello-world",
        any_=True,
    )
])

chat = create_handler([f.Chat("private")])
chat2 = create_handler([f.Chat("private", "group")])
chat3 = create_handler([f.Chat("private", "group", "supergroup")])
group_user = create_handler([f.Chat("group"), f.User(123)])

chat_id = create_handler([f.ChatId(1)])
chat_id2 = create_handler([f.ChatId(1, 2)])

content = create_handler([f.Content("text")])
content2 = create_handler([f.Content("text", "document")])
content3 = create_handler([f.Content("text", "document", "audio")])
content_chat = create_handler([f.Content("text"), f.Chat("private")])

user = create_handler([f.User(1)])
user2 = create_handler([f.User(1, 2)])
user3 = create_handler([f.User(1, 2, 3)])
user4 = create_handler([f.User(1, 2, 3, 4)])
not_user = create_handler([~f.User(123)])
user_command = create_handler([f.Command("foo"), f.User("user")])
user_command2 = create_handler([f.Command("foo", "bar"), f.User("user")])
user3_command = create_handler([f.User(1, 2, 3, 4), f.Command("foo")])
user_chat_command = create_handler([
    f.Chat("group"),
    f.User(123),
    f.Command("foo"),
])
user_chat2_command = create_handler([
    f.User(123),
    f.Chat("group") | f.Chat("private"),
    f.Command("foo"),
])
user2_chatid2_command2 = create_handler([
    f.User(1, 2),
    f.ChatId(1, 2),
    f.Command("foo", "bar"),
])


@pytest.mark.parametrize(
    "input_,sorted_",
    [
        [  # 0
            [fallback],
            [fallback],
        ],
        [  # 1
            [
                command,
                command2,
            ],
            [
                command2,
                command,
            ],
        ],
        [  # 2
            [
                command,
                fallback,
                command2,
            ],
            [
                command2,
                command,
                fallback,
            ],
        ],
        [  # 3
            [
                command,
                text,
                text2,
                command_or_text,
            ],
            [
                command_or_text,
                command,
                text2,
                text,
            ],
        ],
        [  # 4
            [
                text,
                command,
                user,
            ],
            [
                command,
                text,
                user,
            ],
        ],
        [  # 5
            [
                text,
                command,
                user,
                chat,
            ],
            [
                command,
                text,
                user,
                chat,
            ],
        ],
        [  # 6
            [
                text,
                command,
                text2,
                chat2,
                chat3,
                user,
                chat,
            ],
            [
                command,
                text2,
                text,
                user,
                chat3,
                chat2,
                chat,
            ],
        ],
        [  # 7
            [
                user,
                user_command,
                user_command2,
                text,
                fallback,
                command,
                command2,
            ],
            [
                user_command2,
                user_command,
                command2,
                command,
                text,
                user,
                fallback,
            ],
        ],
        [  # 8
            [
                user,
                user_command,
                text,
                fallback,
                command,
                command2,
                user_command2,
                text2,
                user2,
                command_or_text,
                user_chat2_command,
            ],
            [
                user_chat2_command,
                user_command2,
                user_command,
                command2,
                command_or_text,
                command,
                text2,
                text,
                user2,
                user,
                fallback,
            ],
        ],
        [  # 9
            [
                user,
                user_command2,
                text,
                fallback,
                user3_command,
                text3_any,
                text2,
                command2,
                chat3,
                chat2,
                user_command,
                chat_id,
                user4,
                chat_id2,
                command,
                group_user,
                command_or_text,
                user_chat_command,
            ],
            [
                user_chat_command,
                user3_command,
                user_command2,
                user_command,
                command2,
                command_or_text,
                command,
                text3_any,
                text2,
                text,
                group_user,
                user4,
                user,
                chat_id2,
                chat_id,
                chat3,
                chat2,
                fallback,
            ],
        ],
        [  # 10
            [
                user,
                user_command,
                user_command2,
                group_user,
                text,
                fallback,
                command,
                command2,
            ],
            [
                user_command2,
                user_command,
                command2,
                command,
                text,
                group_user,
                user,
                fallback,
            ],
        ],
        [  # 11
            [
                chat,
                not_user,
                chat2,
            ],
            [
                not_user,
                chat2,
                chat,
            ],
        ],
        [  # 12
            [
                not_user,
                chat,
                command_or_text,
            ],
            [
                command_or_text,
                not_user,
                chat,
            ],
        ],
        [  # 13
            [
                chat,
                user2_chatid2_command2,
                content,
                text,
                chat2,
                user_command,
                command_or_text,
            ],
            [
                user2_chatid2_command2,
                user_command,
                command_or_text,
                text,
                content,
                chat2,
                chat,
            ],
        ],
        [  # 14
            [
                command2,
                command_chat,
            ],
            [
                command_chat,
                command2,
            ],
        ],
        [  # 15
            [
                command2,
                text2,
                command_chat,
                text3_any,
                user_chat_command,
                user_chat2_command,
                command_or_text,
                group_user,
                not_user,
            ],
            [
                user_chat2_command,
                user_chat_command,
                command_chat,
                command2,
                command_or_text,
                text3_any,
                text2,
                group_user,
                not_user,
            ],
        ],
    ],
)
def test_priority(input_, sorted_):
    random.shuffle(input_)
    assert sorted(input_, reverse=True) == sorted_
    random.shuffle(input_)
    assert sorted(input_, reverse=True) == sorted_
