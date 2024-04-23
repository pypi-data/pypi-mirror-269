from yatbaf.middleware import Middleware
from yatbaf.router import OnMessage


def middleware(handler):

    async def wrapper(update):
        await handler(update)

    return wrapper


def test_init_middleware_handler():
    router = OnMessage(handler_middleware=[middleware])
    assert router._handler_middleware == [middleware]
    assert not router._middleware


def test_init_middleware_handler_local():
    router = OnMessage(handler_middleware=[(middleware, "local")])
    assert router._handler_middleware == [(middleware, "local")]
    assert not router._middleware


def test_init_middleware_router():
    router = OnMessage(middleware=[middleware])
    assert router._middleware == [middleware]
    assert not router._handler_middleware


def test_add_middleware_handler():
    router = OnMessage()
    router.add_middleware(middleware)
    assert router._handler_middleware == [middleware]
    assert not router._middleware


def test_add_middleware_handler_local():
    router = OnMessage()
    router.add_middleware(middleware, scope="local")
    assert router._handler_middleware == [(middleware, "local")]
    assert not router._middleware


def test_add_middleware_router():
    router = OnMessage()
    router.add_middleware(middleware, "router")
    assert router._middleware == [middleware]
    assert not router._handler_middleware


def test_middleware_decorator_handler():
    router = OnMessage()

    @router.middleware
    def func(_):
        pass

    assert router._handler_middleware == [func]
    assert not router._middleware


def test_middleware_decorator_handler_local():
    router = OnMessage()

    @router.middleware("local")
    def func(_):
        pass

    assert router._handler_middleware == [(func, "local")]
    assert not router._middleware


def test_middleware_decorator_router():
    router = OnMessage()

    @router.middleware("router")
    def func(_):
        pass

    assert router._middleware == [func]
    assert not router._handler_middleware


def test_middleware_decorator_handler_args():
    router = OnMessage()

    @router.middleware("handler", 1, y=2)
    def func(_, x, *, y):  # noqa: U100
        pass

    assert router._handler_middleware == [Middleware(func, 1, y=2)]


def test_middleware_decorator_handler_local_args():
    router = OnMessage()

    @router.middleware("local", 1, y=2)
    def func(_, x, *, y):  # noqa: U100
        pass

    assert router._handler_middleware == [(Middleware(func, 1, y=2), "local")]


def test_middleware_decorator_duplicate():
    router = OnMessage()

    @router.middleware
    @router.middleware
    def func(_):
        pass

    assert router._handler_middleware == [func, func]


def test_middleware_decorator_router_args():
    router = OnMessage()

    @router.middleware("router", 1)
    def func(_, p):  # noqa: U100,U101
        pass

    assert router._middleware == [Middleware(func, 1)]


def test_middleware_decorator_handler_diff_args():
    router = OnMessage()

    @router.middleware("handler", p=1)
    @router.middleware("hadnler", p=2)
    def func(_, p):  # noqa: U100,U101
        pass

    assert router._handler_middleware == [
        Middleware(func, p=2), Middleware(func, p=1)
    ]
