from yatbaf.utils import wrap_middleware


def create_middleware(lst: list, m: int):

    def middleware(fn):

        def wrapper():
            lst.append(m)
            fn()

        return wrapper

    return middleware


def test_wrap():
    list_ = []
    middleware = [create_middleware(list_, i) for i in range(4)]

    def target():
        list_.append("fn")

    result = wrap_middleware(target, middleware)
    result()
    assert list_ == [0, 1, 2, 3, "fn"]
