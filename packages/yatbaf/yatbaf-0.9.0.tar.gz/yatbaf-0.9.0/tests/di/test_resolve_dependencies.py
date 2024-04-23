import pytest

from yatbaf.di import Provide
from yatbaf.di import create_dependency_batches
from yatbaf.di import create_dependency_graph
from yatbaf.di import resolve_dependencies


async def provide_error():
    raise ValueError


async def provide_data():
    return "data"


dependencies = {
    "data": Provide(provide_data),
    "error": Provide(provide_error),
}


@pytest.mark.asyncio
async def test_exception_single_dep():
    error_graph = create_dependency_graph("error", dependencies)
    batches = create_dependency_batches({error_graph})
    with pytest.raises(ValueError):
        await resolve_dependencies(batches, {})


@pytest.mark.asyncio
async def test_exception_multi_deps():
    error_graph = create_dependency_graph("error", dependencies)
    data_graph = create_dependency_graph("data", dependencies)
    batches = create_dependency_batches({data_graph, error_graph})
    with pytest.raises(ValueError):
        await resolve_dependencies(batches, {})
