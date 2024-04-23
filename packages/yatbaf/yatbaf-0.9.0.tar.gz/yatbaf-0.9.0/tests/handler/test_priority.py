import pytest

from yatbaf import filters as f
from yatbaf.handler import on_message


@pytest.mark.parametrize(
    "filters,priority",
    [
        [
            [f.Command("foo")],
            ((1, (1000, 1000)), (0, (0, 0)), (0, (0, 0))),
        ],
        [
            [f.Command("foo") | f.Text(startswith="foo")],
            ((2, (1000, 150)), (0, (0, 0)), (0, (0, 0))),
        ],
        [
            [f.Command("foo"), f.Chat("private")],
            ((1, (1000, 1000)), (0, (0, 0)), (1, (100, 100))),
        ],
        [
            [f.Command("foo"), f.User(1), f.Chat("private")],
            ((1, (1000, 1000)), (1, (100, 100)), (1, (100, 100))),
        ],
        [
            [f.Command("foo", "bar"), f.User(1), f.Chat("private")],
            ((2, (1000, 1000)), (1, (100, 100)), (1, (100, 100))),
        ],
        [
            [f.Command("foo", "bar"), f.User(1), f.Chat("group"), f.ChatId(1)],
            ((2, (1000, 1000)), (1, (100, 100)), (2, (150, 100))),
        ],
    ],
)
def test_priority(filters, priority):

    @on_message(filters=filters)
    async def handler(_):  # noqa: U101
        pass

    handler._parse_priority()
    assert handler._priority == priority
