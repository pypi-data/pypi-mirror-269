import pytest

from yatbaf.filters.base import merge_priority


@pytest.mark.parametrize(
    "p1, p2, excpect",
    [
        [
            {
                "source": (1, 100)
            },
            {
                "source": (1, 100)
            },
            {
                "source": (2, (100, 100))
            },
        ],
        [
            {
                "source": (1, (1000, 100))
            },
            {
                "content": (1, 100)
            },
            {
                "source": (1, (1000, 100)),
                "content": (1, 100),
            },
        ],
        [
            {
                "source": (2, 100),
                "content": (1, 100),
            },
            {
                "content": (1, 110)
            },
            {
                "source": (2, 100),
                "content": (2, (110, 100)),
            },
        ],
        [
            {
                "source": (2, 100),
                "content": (1, 100),
                "user": (1, 100),
            },
            {
                "content": (2, 1000)
            },
            {
                "source": (2, 100),
                "content": (3, (1000, 100)),
                "user": (1, 100),
            },
        ],
        [
            {
                "source": (2, 100),
                "content": (1, 100),
                "user": (2, 230),
            },
            {
                "content": (2, 1000),
                "user": (1, 100),
            },
            {
                "source": (2, 100),
                "content": (3, (1000, 100)),
                "user": (3, (230, 100)),
            },
        ],
    ]
)
def test_merge(p1, p2, excpect):
    assert merge_priority(p1, p2) == excpect
