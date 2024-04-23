import pytest

from yatbaf.di import Provide
from yatbaf.exceptions import DependencyError


def sync_func():
    pass


async def func():
    return "func"


async def gen():
    yield "gen"


def sync_gen():
    yield "sync_gen"


async def func_params(fn_param):
    return fn_param


async def gen_params(gen_param):
    yield gen_param


class Class:
    val = "class-val"

    def __init__(self) -> None:
        self.val = "inst-val"

    @classmethod
    async def class_method(cls) -> int:
        return cls.val

    @staticmethod
    async def static_method() -> str:
        return "static-val"

    async def method(self) -> int:
        return self.val

    async def __call__(self):
        return "call-val"


class ClassParams:

    def __init__(self, init_param):
        self.init_param = init_param

    async def __call__(self, call_param):
        return call_param


@pytest.mark.parametrize("obj", [sync_gen, sync_func, "str", 123])
def test_sync_func(obj):
    with pytest.raises(DependencyError):
        Provide(obj)


@pytest.mark.parametrize(
    "dep,exp", [
        [func, False],
        [gen, True],
        [Class, True],
        [Class(), False],
    ]
)
def test_sync_call(dep, exp):
    assert Provide(dep).sync_call is exp


@pytest.mark.parametrize(
    "dep,exp", [
        [func, False],
        [gen, True],
        [Class, False],
        [Class(), False],
    ]
)
def test_is_generator(dep, exp):
    assert Provide(dep).is_generator is exp


@pytest.mark.parametrize(
    "dep,exp",
    [
        [func, frozenset()],
        [gen, frozenset()],
        [Class, frozenset()],
        [func_params, frozenset(["fn_param"])],
        [gen_params, frozenset(["gen_param"])],
        [ClassParams, frozenset(["init_param"])],
        [ClassParams(1), frozenset(["call_param"])],
    ]
)
def test_dependency_kwargs(dep, exp):
    assert Provide(dep).dependency_kwargs == exp


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "dep,exp",
    [
        [func, "func"],
        [Class(), "call-val"],
        [Class.class_method, "class-val"],
        [Class.static_method, "static-val"],
        [Class().method, "inst-val"],
    ]
)
async def test_result(dep, exp):
    assert await Provide(dep)() == exp


def test_eq():
    assert Provide(func) == Provide(func)
    assert Provide(func) != Provide(func_params)
