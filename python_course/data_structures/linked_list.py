from dataclasses import dataclass
from typing import (
    Generic,
    TypeVar,
    Optional,
    Protocol,
    Union,
    Callable,
    Generator,
    Any,
)

from python_course.utils.predicate import Predicate
from python_course.utils.ord import CompareFunction

T = TypeVar("T")


class NodeInterface(Protocol[T]):
    value: T
    next: Optional["NodeInterface[T]"]


OptionalNode = Optional[NodeInterface[T]]


class ExtendedNodeInterface(Protocol[T]):
    value: T
    next: Optional["ExtendedNodeInterface[T]"]
    prev: Optional["ExtendedNodeInterface[T]"]


OptionalExtNode = Optional[ExtendedNodeInterface[T]]


@dataclass
class NodeInfo(Generic[T]):
    value: T
    index: int
    next: ExtendedNodeInterface = None
    prev: ExtendedNodeInterface = None


class Node(Generic[T], NodeInterface[T]):
    def __init__(self, value: T, next: OptionalNode = None):
        self.value: T = value
        self.next: OptionalNode = next

    def __str__(self):
        print(self.value)
        return str(self.__dict__)


class LinkedList(Generic[T]):
    def __init__(self, comparator: Optional[CompareFunction[T]] = None):
        self.length = 0
        self.comparator = comparator
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = self.head

    def __str__(self):
        output = ""
        if self.is_empty():
            return output

        current_node = self.head
        while current_node is not None:
            comma = "," if current_node.next is not None else ""
            output = output + f"{current_node.value}" + comma
            current_node = current_node.next

        return output

    def __normalize_index(self, index: int) -> int:
        return int(index)

    def is_empty(self) -> bool:
        return self.head is None and self.length == 0

    def __increment(self, value):
        self.length = self.length + value

    def __decrement(self, value):
        self.length = self.length - value

    def prepend(self, value: T):
        new_node = Node(value)

        if self.head is None:
            self.head = new_node
            self.tail = self.head
        else:
            first_node = self.head
            new_node.next = first_node
            self.head = new_node

        self.__increment(1)
        return self

    def delete(self, value: T, all_occurrences=True) -> OptionalNode:
        return self.delete_by_value(value, all_occurrences)

    def append(self, value: T):
        new_node = Node(value)

        if self.is_empty():
            self.head = new_node
            self.tail = self.head
        else:
            self.tail.next = new_node
            self.tail = new_node

        self.__increment(1)
        return self

    def traverse(self) -> Generator[NodeInfo, None, None]:

        index = 0
        prev_node = None
        current_node = self.head
        next_node = None

        while current_node:
            next_node = current_node.next

            yield NodeInfo(
                current_node.value,
                index,
                next_node,
                prev_node,
            )

            index = index + 1
            prev_node = current_node
            current_node = next_node

    def delete_by_value(self, value: T, all_occurrences=True) -> OptionalNode:
        if self.is_empty():
            return None

        current_node = self.head

        self.head = None
        self.tail = self.head

        deleted_count = 0
        deleted_node = None

        while current_node is not None:
            next_node = current_node.next
            are_equals = current_node.value == value

            if deleted_count > 0 and not all_occurrences:
                are_equals = False

            # the next node may contain the filtered value
            current_node.next = None

            if not are_equals:

                if self.tail is None:
                    self.tail = current_node
                else:
                    self.tail.next = current_node
                    self.tail = current_node

                if self.head is None:
                    self.head = self.tail

            if are_equals:
                deleted_count = deleted_count + 1
                deleted_node = current_node

            current_node = next_node

        if deleted_count > 0:
            self.__decrement(deleted_count)

        return deleted_node

    def delete_by_position(self, position: int) -> OptionalNode:
        if self.is_empty():
            return None

        deleted_node = None
        current_node = self.head

        self.head = None
        self.tail = None

        position_with_length = self.length - 1 if position >= self.length else position

        for index in range(0, self.length):
            next_node = current_node.next

            if current_node is not None:

                if index == position_with_length:
                    deleted_node = current_node
                else:
                    current_node.next = None

                    if self.tail is None:
                        self.tail = current_node
                    else:
                        self.tail.next = current_node
                        self.tail = current_node

                    if self.head is None:
                        self.head = self.tail

            current_node = next_node

        self.__decrement(1)
        return deleted_node

    def delete_tail(self) -> OptionalNode:
        if self.is_empty():
            return None

        deleted_tail = self.tail
        current_node = self.head
        prev_node = current_node

        if self.head.next is None:
            self.head = None
            self.tail = self.head
            return deleted_tail

        while current_node is not None:
            next_node = current_node.next

            if next_node is None:
                prev_node.next = None
                self.tail = prev_node
                return deleted_tail

            prev_node = current_node
            current_node = next_node

        return deleted_tail

    def find(self, matcher: Union[T, Predicate[T]]) -> OptionalNode:

        current_node = self.head
        custom_matcher = self.comparator

        while current_node is not None:
            current_value = current_node.value

            #   prefer callback over custom comparator
            if callable(matcher) and matcher(current_value):
                return current_node
            elif custom_matcher and custom_matcher(current_value, matcher) == 0:
                return current_node
            elif custom_matcher is None and matcher == current_value:
                return current_node

            current_node = current_node.next

        return None

    def to_array(self):
        output = [None] * self.length
        current_node = self.head

        index = 0
        while current_node is not None:
            output[index] = current_node.value
            index = index + 1
            current_node = current_node.next

        return output

    def reverse(self):
        if self.length < 1:
            return self

        first_node = self.head
        second_node = first_node.next

        first_node.next = None
        current_node = second_node.next if second_node.next else None

        second_node.next = first_node

        self.head = second_node
        self.tail = first_node

        while current_node is not None:
            next_node = current_node.next

            current_node.next = self.head
            self.head = current_node

            current_node = next_node

        return self

    def reset(self):
        self.head = None
        self.tail = self.head
        self.length = 0
        return self

    def delete_head(self) -> OptionalNode:
        if self.is_empty():
            return None

        deleted_head = self.head
        new_head = deleted_head.next

        if new_head is None:
            self.head = None
            self.tail = self.head
            return deleted_head

        self.head = new_head
        return deleted_head

    def insert(self, value: T, position: int):
        norm_pos = self.__normalize_index(position)

        if self.is_empty() or norm_pos >= self.length:
            return self.append(value)
        elif norm_pos <= 0:
            return self.prepend(value)
        else:
            new_node = Node(value)

            for node_info in self.traverse():

                if node_info.index == norm_pos:
                    prev_node = node_info.prev
                    next_node = (
                        prev_node.next if node_info.next is None else node_info.next
                    )

                    prev_node.next = new_node
                    new_node.next = next_node
                    self.__increment(1)
                    return

    def is_reference_type(self, obj: T) -> bool:
        return not isinstance(obj, (int, float, str, bool, bytes, tuple, frozenset))

    def get_object_properties(self, obj: T) -> dict[str, Any]:
        if isinstance(obj, dict):
            return {key: value for key, value in obj.items()}
        elif hasattr("__dict__"):
            return {
                key: value
                for key, value in vars(obj).items()
                if not callable(value) and not key.startswith("__")
            }
        else:
            raise TypeError(
                f"Unsupported object type: {type(obj)}. Must be a dictionary or object with attributes."
            )

    def get_stringifier_by_type(self) -> Callable[[T], str]:
        value = self.head.value
        if self.is_reference_type(value):
            if isinstance(value, (list, tuple)):
                return (
                    lambda t: f"[{', '.join(map(str, t))}]"
                )  # Generic array formatter

            return lambda t: ",".join(
                f"{key}:{value}" for key, value in self.get_object_properties(t).items()
            )
        return lambda t: f"{t}"

    def to_string(self, stringifier: Optional[Callable[[T], str]] = None) -> str:
        if self.is_empty():
            return ""

        string_fun = stringifier if stringifier else self.get_stringifier_by_type()
        output = ""
        for node_info in self.traverse():
            comma = "" if node_info.next is None else ","
            output = output + f"{{{string_fun(node_info.value)}}}" + comma
        return output
