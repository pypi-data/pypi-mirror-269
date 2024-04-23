import pytest

from yatbaf.di import CleanupGroup


@pytest.fixture
def generator(mock_mark):

    async def _generator():
        yield 1
        mock_mark()

    return _generator


@pytest.mark.asyncio
async def test_cleanup(generator, mock_mark):
    cg = CleanupGroup()
    gen = generator()
    await anext(gen)
    cg.add(gen)

    await cg.cleanup()
    mock_mark.assert_called_once()


@pytest.mark.asyncio
async def test_cleanup1(generator, mock_mark):
    cg = CleanupGroup()
    gen1 = generator()
    gen2 = generator()
    await anext(gen1)
    await anext(gen2)
    cg.add(gen1)
    cg.add(gen2)

    await cg.cleanup()
    assert mock_mark.call_count == 2
