import pytest

from yatbaf.di import Provide
from yatbaf.exceptions import DependencyError
from yatbaf.handler import on_message
from yatbaf.router import OnMessage


async def data1():
    return 1


async def data2():
    return 2


def test_get_dependency_providers_empty():

    @on_message
    async def handler(_):
        pass

    assert handler._get_dependency_providers() == {}


def test_get_dependency_providers_local():

    @on_message(dependencies={"val": Provide(data1)})
    async def handler(_):
        pass

    assert handler._get_dependency_providers() == {"val": Provide(data1)}


def test_get_dependency_providers_router():

    @on_message
    async def handler(_):
        pass

    _ = OnMessage(
        dependencies={"val": Provide(data1)},
        handlers=[handler],
    )

    assert handler._get_dependency_providers() == {"val": Provide(data1)}


def test_get_dependency_providers_router_local():

    @on_message(dependencies={"d2": Provide(data2)})
    async def handler(_):
        pass

    _ = OnMessage(
        dependencies={"d1": Provide(data1)},
        handlers=[handler],
    )

    assert handler._get_dependency_providers() == {
        "d1": Provide(data1),
        "d2": Provide(data2),
    }


def test_get_dependency_providers_override():

    @on_message(dependencies={"val": Provide(data2)})
    async def handler(_):
        pass

    _ = OnMessage(
        dependencies={"val": Provide(data1)},
        handlers=[handler],
    )

    assert handler._get_dependency_providers() == {"val": Provide(data2)}


def test_get_dependency_providers_unique():

    @on_message(dependencies={"data": Provide(data1)})
    async def handler(_):
        pass

    _ = OnMessage(
        dependencies={"val": Provide(data1)},
        handlers=[handler],
    )

    with pytest.raises(DependencyError):
        handler._get_dependency_providers()


def test_resolve_dependencies_missing_provider():

    @on_message
    async def handler(_, val):  # noqa: U100
        pass

    with pytest.raises(DependencyError):
        handler._resolve_dependencies()


@pytest.mark.asyncio
async def test_provide_update_arg(message):

    async def provide_val():
        return "update-arg"

    @on_message(dependencies={"foo": Provide(provide_val)})
    async def handler(message, foo):
        message.ctx["test"] = foo

    handler.on_registration()
    await handler.handle(message)
    assert message.ctx["test"] == "update-arg"


@pytest.mark.asyncio
async def test_provide_update_kwarg(message):

    async def provide_val():
        return "foo"

    @on_message(dependencies={"foo": Provide(provide_val)})
    async def handler(message, foo, update):
        update.ctx["test"] = foo
        message.ctx["test"] += "bar"

    handler.on_registration()
    await handler.handle(message)
    assert message.ctx["test"] == "foobar"


@pytest.mark.asyncio
async def test_dependency_exception(message, mock_mark):

    async def provide_data():
        try:
            yield 1
        except ValueError:
            mock_mark()

    @on_message(dependencies={"data": Provide(provide_data)})
    async def handler(message, data):  # noqa: U100
        raise ValueError()

    handler.on_registration()
    with pytest.raises(ValueError):
        await handler.handle(message)
    mock_mark.assert_called_once()


@pytest.mark.asyncio
async def test_dependency_cleanup(message, mock_mark):

    async def provide_data():
        yield 1
        mock_mark()

    @on_message(dependencies={"data": Provide(provide_data)})
    async def handler(message, data):  # noqa: U100
        return

    handler.on_registration()
    await handler.handle(message)
    mock_mark.assert_called_once()


@pytest.mark.asyncio
async def test_handler_no_kwargs(message, mock_mark):

    async def provide_data():
        mock_mark()
        return 1

    @on_message(dependencies={"data": Provide(provide_data)})
    async def handler(message):  # noqa: U100
        pass

    handler.on_registration()
    await handler.handle(message)
    mock_mark.assert_not_called()
