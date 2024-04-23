import pytest

from yatbaf.di import Provide
from yatbaf.di import _is_async_callable
from yatbaf.di import _is_async_generator
from yatbaf.di import validate_provider
from yatbaf.exceptions import DependencyError


def sync_gen():
    yield


async def async_gen():
    yield


def sync_fn():
    return


async def async_fn():
    return


class SyncCallable:

    def __call__(self):
        return


class SyncGenerator:

    def __call__(self):
        yield


class AsyncCallable:

    async def __call__(self):
        return


class AsyncGenerator:

    async def __call__(self):
        yield


@pytest.mark.parametrize("obj", [async_fn, AsyncCallable()])
def test_is_async_callable_true(obj):
    assert _is_async_callable(obj)


@pytest.mark.parametrize(
    "obj",
    [
        sync_fn,
        sync_gen,
        async_gen,
        SyncCallable(),
        SyncGenerator(),
        AsyncGenerator(),
    ]
)
def test_is_async_callable_false(obj):
    assert not _is_async_callable(obj)


@pytest.mark.parametrize("obj", [async_gen, AsyncGenerator()])
def test_is_async_generator_true(obj):
    assert _is_async_generator(obj)


@pytest.mark.parametrize(
    "obj", [
        async_fn,
        sync_fn,
        sync_gen,
        SyncCallable(),
        SyncGenerator(),
    ]
)
def test_is_async_generator_false(obj):
    assert not _is_async_generator(obj)


def test_validate_provider_reserved_name():
    provider = Provide(async_fn)
    with pytest.raises(DependencyError):
        validate_provider("update", provider, {})


def test_validate_provider_override():
    with pytest.raises(DependencyError):
        validate_provider(
            "data1", Provide(async_fn), {"data": Provide(async_fn)}
        )
