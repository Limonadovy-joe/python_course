from typing import (
    TypeVar,
    Literal,
    Callable,
)


V = TypeVar("V")
Ordering = Literal[-1, 0, 1]
CompareFunction = Callable[[V, V], Ordering]


def compare_int(x: int, y: int) -> Ordering:
    return -1 if x < y else 1 if x > y else 0
