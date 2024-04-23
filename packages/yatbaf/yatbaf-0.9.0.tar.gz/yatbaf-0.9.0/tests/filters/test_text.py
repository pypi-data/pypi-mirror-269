import re

import pytest

from yatbaf.filters import Text


def test_no_params():
    with pytest.raises(ValueError):
        Text()


def test_priority():
    assert Text(startswith="foo").priority == {"content": (1, 150)}
    assert Text(
        startswith="foo",
        endswith="bar",
    ).priority == {
        "content": (2, 150)
    }


@pytest.mark.asyncio
async def test_is_text(message):
    message.text = None
    assert not await Text(startswith="foo").check(message)


@pytest.mark.asyncio
@pytest.mark.parametrize("f,ic", (("FOO", False), ("foo", True)))
async def test_startswith(message, f, ic):
    message.text = "FOO bar"
    assert await Text(startswith=f, ignore_case=ic).check(message)


@pytest.mark.asyncio
@pytest.mark.parametrize("f,ic", (("BAR", False), ("bar", True)))
async def test_endswith(message, f, ic):
    message.text = "foo BAR"
    assert await Text(endswith=f, ignore_case=ic).check(message)


@pytest.mark.asyncio
async def test_start_end(message):
    message.text = "foo baz bar"
    assert await Text(startswith="foo", endswith="bar").check(message)


@pytest.mark.asyncio
async def test_start_end_any(message):
    message.text = "foo bar baz"
    assert await (
        Text(startswith="foo", endswith="bar", any_=True).check(message)
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("m,ic", (("Foo Bar", False), ("foo bar", True)))
async def test_match(message, m, ic):
    message.text = "Foo Bar"
    assert await Text(match=m, ignore_case=ic).check(message)


@pytest.mark.asyncio
async def test_match_false(message):
    message.text = "foo bar"
    assert not await Text(match="foo b").check(message)


@pytest.mark.asyncio
@pytest.mark.parametrize("c", ("bar", ["oof", "foo"]))
async def test_contains(message, c):
    message.text = "foo bar baz"
    assert await Text(contains=c).check(message)


@pytest.mark.asyncio
async def test_contains_false(message):
    message.text = "foo bar baz"
    assert not await Text(contains="foobar").check(message)


@pytest.mark.asyncio
@pytest.mark.parametrize("t", ("foobarbaz", "foo bar baz"))
async def test_start_end_contains(message, t):
    message.text = t
    assert await Text(
        startswith="fo",
        endswith="az",
        contains="bar",
    ).check(message)


@pytest.mark.asyncio
@pytest.mark.parametrize("exp", (".+baz.*$", re.compile("^f.+az$")))
async def test_regexp(message, exp):
    message.text = "foo bar baz"
    assert await Text(regexp=exp).check(message)
