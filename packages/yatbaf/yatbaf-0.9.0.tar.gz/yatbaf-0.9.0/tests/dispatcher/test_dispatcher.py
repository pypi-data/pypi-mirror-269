from yatbaf.dispatcher import Dispatcher


def test_dispatcher():
    handlers = {}
    dispatcher = Dispatcher(handlers)
    assert dispatcher._middleware_stack == dispatcher._resolve
    assert not dispatcher._guards
    assert dispatcher._handlers is handlers
