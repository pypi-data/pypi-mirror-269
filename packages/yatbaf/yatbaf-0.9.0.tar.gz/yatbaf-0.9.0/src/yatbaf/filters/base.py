from __future__ import annotations

__all__ = (
    "BaseFilter",
    "And",
    "Or",
    "Not",
)

from abc import ABC
from abc import abstractmethod
from collections import defaultdict
from typing import TYPE_CHECKING
from typing import Generic
from typing import final

from yatbaf.exceptions import FilterCompatError
from yatbaf.typing import UpdateT

if TYPE_CHECKING:
    from collections.abc import Sequence

    from yatbaf.typing import FilterPriority


class BaseFilter(ABC, Generic[UpdateT]):
    """Base class for filters."""

    @final
    def __or__(self, other: object) -> BaseFilter[UpdateT]:
        if not isinstance(other, BaseFilter):
            return NotImplemented
        return Or(self, other)

    @final
    def __and__(self, other: object) -> BaseFilter[UpdateT]:
        if not isinstance(other, BaseFilter):
            return NotImplemented
        return And(self, other)

    @final
    def __invert__(self) -> BaseFilter[UpdateT]:
        return Not(self)

    @final
    @classmethod
    def incompat(cls, filter: type[BaseFilter]) -> None:
        _conflicts_map[cls].add(filter)
        _conflicts_map[filter].add(cls)

    @property
    @abstractmethod
    def priority(self) -> FilterPriority:
        pass

    @abstractmethod
    async def check(self, update: UpdateT) -> bool:
        """Check filter"""


@final
class And(BaseFilter[UpdateT]):

    def __init__(
        self, f1: BaseFilter[UpdateT], f2: BaseFilter[UpdateT]
    ) -> None:
        self.f1 = f1
        self.f2 = f2

    @property
    def priority(self) -> FilterPriority:
        return merge_priority(self.f1.priority, self.f2.priority)

    async def check(self, update: UpdateT) -> bool:
        return await self.f1.check(update) and await self.f2.check(update)


@final
class Or(BaseFilter[UpdateT]):

    def __init__(
        self, f1: BaseFilter[UpdateT], f2: BaseFilter[UpdateT]
    ) -> None:
        self.f1 = f1
        self.f2 = f2

    @property
    def priority(self) -> FilterPriority:
        return merge_priority(self.f1.priority, self.f2.priority)

    async def check(self, update: UpdateT) -> bool:
        return await self.f1.check(update) or await self.f2.check(update)


@final
class Not(BaseFilter[UpdateT]):

    def __init__(self, f: BaseFilter[UpdateT]) -> None:
        self.f = f

    @property
    def priority(self) -> FilterPriority:
        return self.f.priority

    async def check(self, update: UpdateT) -> bool:
        return not await self.f.check(update)


_conflicts_map: dict[type[BaseFilter], set[type[BaseFilter]]] = defaultdict(set)


def merge_priority(p1: FilterPriority, p2: FilterPriority) -> FilterPriority:
    """:meta private:"""
    result = {**p1}
    for p2_group, p2_prior in p2.items():
        prior: tuple[int, int | tuple[int, int]]
        if p1_prior := result.get(p2_group):
            max_p1, min_p1 = _unpack(p1_prior[1])
            max_p2, min_p2 = _unpack(p2_prior[1])

            prior = (
                p1_prior[0] + p2_prior[0],
                (max([max_p1, max_p2]), min(min_p1, min_p2)),
            )
        else:
            prior = p2_prior

        result[p2_group] = prior
    return result


def _unpack(value: int | tuple[int, int]) -> tuple[int, int]:
    """:meta private:"""
    if isinstance(value, int):
        return value, value
    return value


def is_compat(filter1: BaseFilter, filter2: BaseFilter) -> None:
    """:meta private:"""
    if isinstance(filter1, And | Or):
        for filter in (filter1.f1, filter1.f2):
            is_compat(filter, filter2)

    if isinstance(filter2, And | Or):
        for filter in (filter2.f1, filter2.f2):
            is_compat(filter1, filter)

    if conflicts := _conflicts_map[type(filter1)]:
        if type(filter2) in conflicts:
            raise FilterCompatError(
                f"{type(filter1)} cannot be used with {type(filter2)}."
            )


def check_compatibility(filters: Sequence[BaseFilter], any_: bool) -> None:
    """:meta private:"""
    for i, target in enumerate(filters, start=1):
        if isinstance(target, Not):
            target = target.f

        # check filters inside `And` or `Or` filters
        if isinstance(target, And | Or):
            check_compatibility((target.f1, target.f2), isinstance(target, Or))

        # do not check compat between filters inside the `Or` filter
        if any_:
            continue

        for filter in filters[i:]:
            if isinstance(filter, Not):
                filter = filter.f
            is_compat(target, filter)
