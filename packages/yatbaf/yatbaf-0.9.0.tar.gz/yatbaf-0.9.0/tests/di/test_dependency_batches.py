import pytest

from yatbaf.di import Dependency
from yatbaf.di import Provide
from yatbaf.di import create_dependency_batches


async def dummy() -> None:
    pass


DEPENDENCY_A = Dependency("A", Provide(dummy), [])
DEPENDENCY_B = Dependency("B", Provide(dummy), [])
DEPENDENCY_C1 = Dependency("C1", Provide(dummy), [])
DEPENDENCY_C2 = Dependency("C2", Provide(dummy), [DEPENDENCY_C1])
DEPENDENCY_ALL_EXCEPT_A = Dependency(
    "D", Provide(dummy), [DEPENDENCY_B, DEPENDENCY_C1, DEPENDENCY_C2]
)


@pytest.mark.parametrize(
    "dependency_tree,expected_batches",
    [
        (set(), []),
        ({DEPENDENCY_A}, [{DEPENDENCY_A}]),
        (
            {DEPENDENCY_A, DEPENDENCY_B},
            [
                {DEPENDENCY_A, DEPENDENCY_B},
            ],
        ),
        (
            {DEPENDENCY_C1, DEPENDENCY_C2},
            [
                {DEPENDENCY_C1},
                {DEPENDENCY_C2},
            ],
        ),
        (
            {
                DEPENDENCY_A,
                DEPENDENCY_B,
                DEPENDENCY_C1,
                DEPENDENCY_C2,
                DEPENDENCY_ALL_EXCEPT_A
            },
            [
                {DEPENDENCY_A, DEPENDENCY_B, DEPENDENCY_C1},
                {DEPENDENCY_C2},
                {DEPENDENCY_ALL_EXCEPT_A},
            ],
        ),
        (
            {DEPENDENCY_ALL_EXCEPT_A},
            [
                {DEPENDENCY_B, DEPENDENCY_C1},
                {DEPENDENCY_C2},
                {DEPENDENCY_ALL_EXCEPT_A},
            ],
        ),
    ],
)
def test_dependency_batches(dependency_tree, expected_batches) -> None:
    calculated_batches = create_dependency_batches(dependency_tree)
    assert calculated_batches == expected_batches
