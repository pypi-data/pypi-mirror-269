import pytest

from yatbaf.enums import ContentType
from yatbaf.filters import Content


def test_empty():
    with pytest.raises(ValueError):
        Content()


def test_wrong_type():
    with pytest.raises(ValueError):
        Content("typo")


def test_priority():
    assert Content("text").priority == {"content": (1, 100)}
    assert Content("text", "document").priority == {"content": (2, 100)}


@pytest.mark.asyncio
@pytest.mark.parametrize("content", ["text", ContentType.TEXT])
async def test_true(message, content):
    message.text = "123"
    assert await Content(content).check(message)


@pytest.mark.asyncio
@pytest.mark.parametrize("content", ["document", ContentType.DOCUMENT])
async def test_filter_content_false(message, content):
    message.text = "123"
    message.document = None
    assert not await Content(content).check(message)
