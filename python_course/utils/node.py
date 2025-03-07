from typing import Generic, TypeVar, Optional, Protocol


T = TypeVar("T")


class NodeInterface(Protocol[T]):
    value: T
    next: Optional["NodeInterface[T]"]


OptionalNode = Optional[NodeInterface[T]]


class Node(Generic[T], NodeInterface[T]):
    def __init__(self, value: T, next: OptionalNode = None):
        self.value: T = value
        self.next: OptionalNode = next

    def __str__(self):
        print(self.value)
        return str(self.__dict__)
