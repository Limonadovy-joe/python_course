from typing import Generic, TypeVar, List, Optional, Literal, Callable, Tuple

from collections import deque

T = TypeVar("T")

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


class Stack(Generic[T]):

    def __init__(self, compare: Optional[CompareFunction[T]] = None):
        self.compare = compare
        if compare is None:
            self.compare = lambda x, y: -1 if x < y else 1 if x > y else 0
        self.top: Optional[Node[T]] = None
        self.bottom: Optional[Node[T]] = self.top
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
        current_node = self.top

        while current_node is not None:
            yield current_node
            current_node = current_node.next

    def is_empty(self) -> bool:
        return self.top is None and self.bottom is None

    def push(self, value: T) -> None:
        new_node = Node(value)

        if self.is_empty():
            self.top = new_node
            self.bottom = self.top
        else:
            current_node = self.top
            new_node.next = current_node
            self.top = new_node

        self.length = self.length + 1

    def peek(self) -> Optional[T]:
        return self.top.value if not self.is_empty() else None

    def pop(self) -> Optional[T]:
        if self.is_empty():
            return None

        current_node = self.top
        next_node = current_node.next
        popped_node = current_node

        if next_node is None:
            self.top = None
            self.bottom = self.top
            self.length = 0
            return popped_node.value

        self.top = next_node
        self.length = self.length - 1

        return popped_node.value

    def to_array(self) -> List[T]:

        arr = []
        if self.is_empty():
            return arr

        for node in self.__iterate():
            arr.append(node.value)

        return arr
