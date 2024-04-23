# Based on litestar's di, distributed under MIT license.
# github.com/litestar-org/litestar/blob/main/LICENSE

from __future__ import annotations

__all__ = ("Provide",)

import asyncio
import inspect
from typing import TYPE_CHECKING
from typing import Any
from typing import Final

from .exceptions import DependencyError

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator
    from collections.abc import Callable

    from .typing import HandlerDependency

RESERVED_KWARGS: Final = frozenset(["update"])


class Provide:
    """Wrapper class for dependency injection."""

    __slots__ = (
        "dependency",
        "dependency_kwargs",
        "sync_call",
        "is_generator",
    )

    def __init__(self, dependency: HandlerDependency) -> None:
        """
        :param dependency: Callable to call or class to instantiate. The result
            is then injected as a dependency.
        """
        if not callable(dependency):
            raise DependencyError("dependency must be callable")

        self.dependency = dependency
        self.dependency_kwargs = frozenset(get_parameters(dependency))

        is_class = inspect.isclass(dependency)
        is_generator = not is_class and _is_async_generator(dependency)

        if not (is_class or is_generator):
            if not _is_async_callable(dependency):
                raise DependencyError("dependency must be async callable")

        self.sync_call = is_class or is_generator
        self.is_generator = is_generator

    async def __call__(self, **kwargs: Any) -> Any:
        if self.sync_call:
            return self.dependency(**kwargs)
        return await self.dependency(**kwargs)  # type: ignore[misc]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Provide) and (  # yapf: disable
            other is self or other.dependency == self.dependency
        )


class Dependency:

    __slots__ = (
        "key",
        "provider",
        "dependencies",
    )

    def __init__(
        self, key: str, provider: Provide, dependencies: list[Dependency]
    ) -> None:
        self.key = key
        self.provider = provider
        self.dependencies = dependencies

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Dependency) and (
            other is self or (  # yapf: disable
                other.key == self.key
                and other.provider == self.provider
                and other.dependencies == self.dependencies
            )
        )

    def __hash__(self) -> int:
        return hash(self.key)


class CleanupGroup:

    __slots__ = ("generators",)

    def __init__(self) -> None:
        self.generators: list[AsyncGenerator[Any, None]] = []

    def add(self, gen: AsyncGenerator[Any, None]) -> None:
        self.generators.append(gen)

    async def cleanup(self) -> None:
        if not self.generators:
            return

        if len(self.generators) == 1:
            await anext(self.generators[0], None)
            return

        async with asyncio.TaskGroup() as tg:
            for gen in self.generators:
                tg.create_task(anext(gen, None))

    async def throw(self, exc: BaseException) -> None:
        for gen in self.generators:
            try:
                await gen.athrow(exc)
            except StopAsyncIteration:
                continue


def get_parameters(fn: Callable[..., Any]) -> list[str]:
    return list(inspect.signature(fn).parameters)


def is_reserved_key(key: str) -> bool:
    return key in RESERVED_KWARGS


def _is_async_generator(fn: Callable[..., Any]) -> bool:
    return (
        inspect.isasyncgenfunction(fn)
        or inspect.isasyncgenfunction(fn.__call__)  # type: ignore[operator]
    )


def _is_async_callable(fn: Callable[..., Any]) -> bool:
    return (
        inspect.iscoroutinefunction(fn)
        or inspect.iscoroutinefunction(fn.__call__)  # type: ignore[operator]
    )


def validate_provider(
    key: str,
    provider: Provide,
    dependencies: dict[str, Provide],
) -> None:
    if is_reserved_key(key):
        raise DependencyError(f"name {key!r} is reserved.")

    for k, v in dependencies.items():
        if v == provider:
            raise DependencyError(
                f"Provider {key!r} is already registered as {k!r}! "
                "Use the same name to override provider."
            )


async def _resolve_dependency(
    dependency: Dependency, kwargs: dict[str, Any], cleanup_group: CleanupGroup
) -> None:
    dependency_kwargs = {
        k: kwargs[k]
        for k in dependency.provider.dependency_kwargs
    }
    value = await dependency.provider(**dependency_kwargs)
    if dependency.provider.is_generator:
        cleanup_group.add(value)
        value = await anext(value)
    kwargs[dependency.key] = value


async def resolve_dependencies(
    dependencies: list[set[Dependency]], kwargs: dict[str, Any]
) -> CleanupGroup:
    cleanup_group = CleanupGroup()
    for batch in dependencies:
        if len(batch) == 1:
            await _resolve_dependency(next(iter(batch)), kwargs, cleanup_group)
        else:
            try:
                async with asyncio.TaskGroup() as tg:
                    for dependency in batch:
                        tg.create_task(
                            _resolve_dependency(
                                dependency,
                                kwargs,
                                cleanup_group,
                            )
                        )
            except ExceptionGroup as eg:
                raise eg.exceptions[0] from eg

    return cleanup_group


def create_dependency_graph(
    key: str, dependencies: dict[str, Provide]
) -> Dependency:
    try:
        provider = dependencies[key]
    except KeyError:
        raise DependencyError(f"Provider is missing: {key!r}") from None

    sub_dependencies = [
        k for k in provider.dependency_kwargs if k not in RESERVED_KWARGS
    ]
    return Dependency(
        key,
        provider,
        dependencies=[
            create_dependency_graph(k, dependencies) for k in sub_dependencies
        ]
    )


def create_dependency_batches(
    expected_dependencies: set[Dependency]
) -> list[set[Dependency]]:
    dependencies_to: dict[Dependency, set[Dependency]] = {}
    for dependency in expected_dependencies:
        if dependency not in dependencies_to:
            map_dependencies_recursively(dependency, dependencies_to)

    batches = []
    while dependencies_to:
        current_batch = {  # yapf: disable
            dependency
            for dependency, remaining_sub_dependencies in dependencies_to.items()  # noqa: E501
            if not remaining_sub_dependencies
        }

        for dependency in current_batch:
            del dependencies_to[dependency]
            for others_dependencies in dependencies_to.values():
                others_dependencies.discard(dependency)

        batches.append(current_batch)

    return batches


def map_dependencies_recursively(
    dependency: Dependency,
    dependencies_to: dict[Dependency, set[Dependency]],
) -> None:
    dependencies_to[dependency] = set(dependency.dependencies)
    for sub in dependency.dependencies:
        if sub not in dependencies_to:
            map_dependencies_recursively(sub, dependencies_to)
