from typing import Generic, TypeVar, Protocol

from utils.node import OptionalNode


T = TypeVar("T")


class Traversable(Protocol, Generic[T]):
    head: OptionalNode[T]
    tail: OptionalNode[T]
    value: T
