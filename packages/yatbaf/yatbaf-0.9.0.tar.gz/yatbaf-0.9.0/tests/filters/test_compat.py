import pytest

from yatbaf import filters as f
from yatbaf.exceptions import FilterCompatError
from yatbaf.filters.base import check_compatibility
from yatbaf.filters.base import is_compat


def test_validate():
    with pytest.raises(FilterCompatError):
        is_compat(f.Chat("group"), f.Command("boo") | f.Chat("group"))


@pytest.mark.parametrize(
    "filters",
    [  # yapf: disable
        [f.Command("foo"), f.Command("bar")],
        [f.Command("foo"), f.Text(startswith="bar")],
        [f.Text(startswith="bar"), f.Command("foo")],
        [f.Content("text"), f.Content("document")],
        [f.User(123), f.User(321)],
        [f.User(123), f.User(321) & f.Command("foo")],
        [f.User(321) & f.Command("foo"), f.User(123)],
        [f.User(123) & f.Chat("group"), f.User(321)],
        [f.User(123) & (f.Chat("private") | f.Chat("group")), f.Command("foo"), ~f.User(321)],  # noqa: E501
        [f.Chat("group"), f.Chat("private")],
        [f.Chat("group") & f.Chat("private")],
        [~f.Chat("group"), f.Chat("private")],
        [f.Content("audio") & f.Chat("private"), f.Command("foo")],
        [f.Content("audio") & f.Chat("private") & f.Command("foo")],
        [f.Chat("private"), f.User(123), f.Command("foo"), f.Content("text")],
        [(f.Chat("private") & f.User(123)) & f.User(321)],
        [f.Chat("group"), f.Text(startswith="foo") & f.Text(endswith="bar"), f.Content("text")],   # noqa: E501
    ]
)
def test_conflicts(filters):
    with pytest.raises(FilterCompatError):
        check_compatibility(filters, False)


@pytest.mark.parametrize(
    "filters",
    [  # yapf: disable
        [f.Command("foo"), f.User(123)],
        [f.Text(startswith="bar"), f.Text(endswith="foo")],
        [f.Command("foo"), (f.Chat("private") & f.ChatId(123)) | f.User(123)],
        [f.User(123), f.Chat("group"), f.Command("foo")],
        [f.Content("text") | f.Content("document"), f.Chat("private")],
        [~(f.Content("text") | f.Content("document")), f.Chat("private")],
    ]
)
def test_no_conflicts(filters):
    check_compatibility(filters, False)
