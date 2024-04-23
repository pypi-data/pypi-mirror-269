import pytest

from yatbaf.filters.base import BaseFilter


class FalseFilter(BaseFilter):
    priority = {"content": (1, 100)}

    async def check(self, _):
        return False


class TrueFilter(BaseFilter):
    priority = {"content": (1, 100)}

    async def check(self, _):
        return True


@pytest.mark.asyncio
async def test_not_true(message):
    assert await (~FalseFilter()).check(message)


@pytest.mark.asyncio
async def test_not_false(message):
    assert not await (~TrueFilter()).check(message)


@pytest.mark.asyncio
async def test_or_true(message):
    assert await (FalseFilter() | TrueFilter()).check(message)


@pytest.mark.asyncio
async def test_or_false(message):
    assert not await (FalseFilter() | FalseFilter()).check(message)


@pytest.mark.asyncio
async def test_and_true(message):
    assert await (TrueFilter() & TrueFilter()).check(message)


@pytest.mark.asyncio
async def test_and_false(message):
    assert not await (TrueFilter() & FalseFilter()).check(message)
