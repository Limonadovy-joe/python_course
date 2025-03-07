from typing import Generic, TypeVar, Optional, Literal, Callable


T = TypeVar("T")

#   TODO
#   To ordering utils
Ordering = Literal[-1, 0, 1]
#   To function utils
CompareFunction = Callable[[T, T], Ordering]
Position = Literal["Left", "Right"]


class Node(Generic[T]):
    def __init__(
        self,
        value: T,
        next: Optional["Node[T]"] = None,
    ):
        self.value = value
        self.next = next

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.value == other.value

    def __repr__(self):
        return f"Node({self.value}, next={self.next})"


class Queue(Generic[T]):

    def __init__(self, compare: Optional[CompareFunction[T]] = None):
        self.compare = compare
        if compare is None:
            self.compare = lambda x, y: -1 if x < y else 1 if x > y else 0
        self.front: Optional[Node[T]] = None
        self.back: Optional[Node[T]] = self.front
        self.length = 0

    def __str__(self):
        if self.is_empty():
            return ""

        string = ""
        for node in self.__iterate():
            string = string + f"{node.value},"

        string = string[:-1]
        return string

    def __iterate(self):
        current_node = self.front

        while current_node is not None:
            yield current_node
            current_node = current_node.next

    def is_empty(self) -> bool:
        return self.front is None and self.back is None

    def enqueue(self, value: T) -> None:
        node = Node(value)

        if self.is_empty():
            self.front = node
            self.back = self.front
        else:
            self.back.next = node
            self.back = node

        self.length = self.length + 1

    def dequeue(self) -> Optional[T]:
        if self.is_empty():
            return None

        value = self.front.value
        next_node = self.front.next

        self.length = self.length - 1

        if next_node is None:
            self.front = None
            self.back = self.front
            return value

        self.front = next_node
        return value

    def peek(self) -> Optional[T]:
        if self.is_empty():
            return None

        return self.front.value
