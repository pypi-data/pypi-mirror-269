import pytest

from yatbaf.di import Provide
from yatbaf.enums import UpdateType
from yatbaf.handler import Handler
from yatbaf.router import OnBusinessConnection
from yatbaf.router import OnBusinessMessage
from yatbaf.router import OnCallbackQuery
from yatbaf.router import OnChannelPost
from yatbaf.router import OnChatBoost
from yatbaf.router import OnChatJoinRequest
from yatbaf.router import OnChatMember
from yatbaf.router import OnChosenInlineResult
from yatbaf.router import OnDeletedBusinessMessages
from yatbaf.router import OnEditedBusinessMessage
from yatbaf.router import OnEditedChannelPost
from yatbaf.router import OnEditedMessage
from yatbaf.router import OnInlineQuery
from yatbaf.router import OnMessage
from yatbaf.router import OnMessageReaction
from yatbaf.router import OnMessageReactionCount
from yatbaf.router import OnMyChatMember
from yatbaf.router import OnPoll
from yatbaf.router import OnPollAnswer
from yatbaf.router import OnPreCheckoutQuery
from yatbaf.router import OnRemovedChatBoost
from yatbaf.router import OnShippingQuery
from yatbaf.router import parse_handlers


async def fn(_):
    pass


@pytest.mark.parametrize(
    "handler,exp",
    [
        [
            Handler(fn, UpdateType.MESSAGE), {
                "message": OnMessage(
                    handlers=[Handler(fn, UpdateType.MESSAGE)]
                )
            }
        ],
        [
            Handler(fn, UpdateType.EDITED_MESSAGE),
            {
                "edited_message": OnEditedMessage(
                    handlers=[Handler(fn, UpdateType.EDITED_MESSAGE)]
                )
            }
        ],
        [
            Handler(fn, UpdateType.CHANNEL_POST),
            {
                "channel_post": OnChannelPost(
                    handlers=[Handler(fn, UpdateType.CHANNEL_POST)]
                )
            }
        ],
        [
            Handler(fn, UpdateType.EDITED_CHANNEL_POST),
            {
                "edited_channel_post": OnEditedChannelPost(
                    handlers=[Handler(fn, UpdateType.EDITED_CHANNEL_POST)]
                )
            }
        ],
        [
            Handler(fn, UpdateType.INLINE_QUERY),
            {
                "inline_query": OnInlineQuery(
                    handlers=[Handler(fn, UpdateType.INLINE_QUERY)]
                )
            }
        ],
        [
            Handler(fn, UpdateType.CHOSEN_INLINE_RESULT),
            {
                "chosen_inline_result": OnChosenInlineResult(
                    handlers=[Handler(fn, UpdateType.CHOSEN_INLINE_RESULT)]
                )
            }
        ],
        [
            Handler(fn, UpdateType.CALLBACK_QUERY),
            {
                "callback_query": OnCallbackQuery(
                    handlers=[Handler(fn, UpdateType.CALLBACK_QUERY)]
                )
            }
        ],
        [
            Handler(fn, UpdateType.SHIPPING_QUERY),
            {
                "shipping_query": OnShippingQuery(
                    handlers=[Handler(fn, UpdateType.SHIPPING_QUERY)]
                )
            }
        ],
        [
            Handler(fn, UpdateType.PRE_CHECKOUT_QUERY),
            {
                "pre_checkout_query": OnPreCheckoutQuery(
                    handlers=[Handler(fn, UpdateType.PRE_CHECKOUT_QUERY)]
                )
            }
        ],
        [
            Handler(fn, UpdateType.POLL), {
                "poll": OnPoll(handlers=[Handler(fn, UpdateType.POLL)])
            }
        ],
        [
            Handler(fn, UpdateType.POLL_ANSWER),
            {
                "poll_answer": OnPollAnswer(
                    handlers=[Handler(fn, UpdateType.POLL_ANSWER)]
                )
            }
        ],
        [
            Handler(fn, UpdateType.MY_CHAT_MEMBER),
            {
                "my_chat_member": OnMyChatMember(
                    handlers=[Handler(fn, UpdateType.MY_CHAT_MEMBER)]
                )
            }
        ],
        [
            Handler(fn, UpdateType.CHAT_MEMBER),
            {
                "chat_member": OnChatMember(
                    handlers=[Handler(fn, UpdateType.CHAT_MEMBER)]
                )
            }
        ],
        [
            Handler(fn, UpdateType.CHAT_JOIN_REQUEST),
            {
                "chat_join_request": OnChatJoinRequest(
                    handlers=[Handler(fn, UpdateType.CHAT_JOIN_REQUEST)]
                )
            }
        ],
        [
            Handler(fn, UpdateType.MESSAGE_REACTION),
            {
                "message_reaction": OnMessageReaction(
                    handlers=[Handler(fn, UpdateType.MESSAGE_REACTION)]
                )
            }
        ],
        [
            Handler(fn, UpdateType.MESSAGE_REACTION_COUNT),
            {
                "message_reaction_count": OnMessageReactionCount(
                    handlers=[Handler(fn, UpdateType.MESSAGE_REACTION_COUNT)]
                )
            }
        ],
        [
            Handler(fn, UpdateType.CHAT_BOOST),
            {
                "chat_boost": OnChatBoost(
                    handlers=[Handler(fn, UpdateType.CHAT_BOOST)]
                )
            }
        ],
        [
            Handler(fn, UpdateType.REMOVED_CHAT_BOOST),
            {
                "removed_chat_boost": OnRemovedChatBoost(
                    handlers=[Handler(fn, UpdateType.REMOVED_CHAT_BOOST)]
                )
            }
        ],
        [
            Handler(fn, UpdateType.BUSINESS_CONNECTION),
            {
                "business_connection": OnBusinessConnection(
                    handlers=[Handler(fn, UpdateType.BUSINESS_CONNECTION)]
                )
            }
        ],
        [
            Handler(fn, UpdateType.BUSINESS_MESSAGE),
            {
                "business_message": OnBusinessMessage(
                    handlers=[Handler(fn, UpdateType.BUSINESS_MESSAGE)]
                )
            }
        ],
        [
            Handler(fn, UpdateType.EDITED_BUSINESS_MESSAGE),
            {
                "edited_business_message": OnEditedBusinessMessage(
                    handlers=[Handler(fn, UpdateType.EDITED_BUSINESS_MESSAGE)]
                )
            }
        ],
        [
            Handler(fn, UpdateType.DELETED_BUSINESS_MESSAGES),
            {
                "deleted_business_messages": OnDeletedBusinessMessages(
                    handlers=[
                        Handler(fn, UpdateType.DELETED_BUSINESS_MESSAGES)
                    ]
                )
            }
        ],
    ]
)
def test_parse(handler, exp):
    assert parse_handlers(handlers=[handler]) == exp


def test_one_router(handler_fn):
    router = OnMessage(handlers=[Handler(handler_fn, "message")])
    result = parse_handlers(routers=[router])
    assert result == {"message": router}
    assert result["message"] is router


def test_routers(handler_fn):
    result = parse_handlers(
        routers=[
            OnMessage(),
            OnMessage(handlers=[Handler(handler_fn, "message")]),
            OnPoll(handlers=[Handler(handler_fn, "poll")]),
            OnCallbackQuery(handlers=[Handler(handler_fn, "callback_query")])
        ]
    )
    assert result == {
        "message": OnMessage(
            routers=[
                OnMessage(),
                OnMessage(handlers=[Handler(handler_fn, "message")],)
            ],
        ),
        "callback_query": OnCallbackQuery(
            handlers=[Handler(handler_fn, "callback_query")]
        ),
        "poll": OnPoll(handlers=[Handler(handler_fn, "poll")]),
    }


def test_handlers_routers(handler_fn):
    result = parse_handlers(
        handlers=[
            Handler(handler_fn, "poll"),
            Handler(handler_fn, "message"),
            Handler(handler_fn, "callback_query"),
        ],
        routers=[
            OnMessage(handlers=[Handler(handler_fn, "message")]),
            OnCallbackQuery(handlers=[Handler(handler_fn, "callback_query")]),
        ],
    )
    assert result == {
        "message": OnMessage(
            handlers=[Handler(handler_fn, "message")],
            routers=[OnMessage(handlers=[Handler(handler_fn, "message")])],
        ),
        "poll": OnPoll(handlers=[Handler(handler_fn, "poll")]),
        "callback_query": OnCallbackQuery(
            handlers=[Handler(handler_fn, "callback_query")],
            routers=[
                OnCallbackQuery(
                    handlers=[Handler(handler_fn, "callback_query")]
                )
            ]
        ),
    }


async def provide_data1():
    return 1


async def provide_data2():
    return 2


@pytest.mark.parametrize(
    "gd,rd,exp",
    [  # yapf: disable
        [{}, {}, {}],
        [
            {"data1": Provide(provide_data1)},
            {},
            {"data1": Provide(provide_data1)},
        ],
        [
            {},
            {"data1": Provide(provide_data1)},
            {"data1": Provide(provide_data1)},
        ],
        [
            {"data1": Provide(provide_data1)},
            {"data1": Provide(provide_data2)},
            {"data1": Provide(provide_data2)},
        ],
        [
            {"data1": Provide(provide_data1)},
            {"data2": Provide(provide_data2)},
            {
                "data1": Provide(provide_data1),
                "data2": Provide(provide_data2),
            },
        ],
    ]
)
def test_deps_one_router_merge(gd, rd, exp):
    router = OnMessage(dependencies=rd)
    result = parse_handlers(routers=[router], dependencies=gd)
    assert result == {"message": OnMessage(dependencies=exp)}


def test_deps_handler(handler_fn):
    dependencies = {"data": Provide(provide_data1)}
    result = parse_handlers(
        handlers=[Handler(handler_fn, UpdateType.MESSAGE)],
        dependencies=dependencies,
    )
    assert result == {
        "message": OnMessage(
            handlers=[Handler(handler_fn, UpdateType.MESSAGE)],
            dependencies=dependencies,
        )
    }


def test_deps_routers():
    router1 = OnMessage(dependencies={"data1": Provide(provide_data1)})
    router2 = OnMessage(dependencies={"data2": Provide(provide_data2)})
    router3 = OnCallbackQuery()
    result = parse_handlers(
        routers=[router1, router2, router3],
        dependencies={"data1": Provide(provide_data1)}
    )
    assert result == {
        "message": OnMessage(
            routers=[
                OnMessage(dependencies={"data1": Provide(provide_data1)}),
                OnMessage(dependencies={"data2": Provide(provide_data2)}),
            ],
            dependencies={"data1": Provide(provide_data1)},
        ),
        "callback_query": OnCallbackQuery(
            dependencies={"data1": Provide(provide_data1)},
        )
    }
