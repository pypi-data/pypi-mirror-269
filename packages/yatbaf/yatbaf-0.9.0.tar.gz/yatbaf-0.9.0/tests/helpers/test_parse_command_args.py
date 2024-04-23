import pytest

from yatbaf.helpers import parse_command_args


@pytest.mark.parametrize(
    "text,result",
    [
        ("/foo", []),
        ("/foo bar", ["bar"]),
        ("/foo@bot bar baz", ["bar", "baz"]),
        ("/foo Bar baZ 123", ["Bar", "baZ", "123"]),
    ],
)
def test_parse_args(text, result):
    assert parse_command_args(text) == result
