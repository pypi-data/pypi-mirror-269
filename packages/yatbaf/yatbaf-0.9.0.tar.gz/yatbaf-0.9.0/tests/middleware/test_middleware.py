from yatbaf.middleware import Middleware


def test_middleware():

    class SimpleMiddleware:

        def __init__(self, next_):
            self.next_ = next_

    middleware = Middleware(SimpleMiddleware)

    result = middleware(next_ := object())
    assert result.next_ is next_


def test_middleware_params():

    class ParamsMiddleware:

        def __init__(self, next_, param1, param2):
            self.next_ = next_
            self.param1 = param1
            self.param2 = param2

    middleware = Middleware(
        ParamsMiddleware,
        param1=1,
        param2=2,
    )

    result = middleware(next_ := object())
    assert result.next_ is next_
    assert result.param1 == 1
    assert result.param2 == 2
