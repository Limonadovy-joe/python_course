from typing import (
    Generic,
    TypeVar,
    Optional,
    Protocol,
    Callable,
    Literal,
)


T = TypeVar("T")
Predicate = Callable[[T], bool]

Ordering = Literal[-1, 0, 1]
CompareFunction = Callable[[T, T], Ordering]


class DoublyLinkedNodeInterface(Protocol[T]):
    value: T
    next: Optional["DoublyLinkedNodeInterface[T]"]
    previous: Optional["DoublyLinkedNodeInterface[T]"]


OptionalDoublyLinkedNode = Optional[DoublyLinkedNodeInterface]


class DoublyLinkedNode(Generic[T]):
    def __init__(
        self,
        value: T,
        next: OptionalDoublyLinkedNode = None,
        previous: OptionalDoublyLinkedNode = None,
    ):
        self.value: T = value
        self.next: OptionalDoublyLinkedNode = next
        self.previous: OptionalDoublyLinkedNode = previous

    def __str__(self):
        print("Node", self.value)
        return str(self.__dict__)


class DoublyLinkedList(Generic[T]):

    def __init__(
        self,
        compare: Optional[CompareFunction[T]] = lambda x, y: (
            -1 if x < y else 1 if x > y else 0
        ),
    ):
        self.length = 0
        self.head: OptionalDoublyLinkedNode = None
        self.tail: OptionalDoublyLinkedNode = self.head
        self.compare = compare

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

    def is_empty(self) -> bool:
        return self.length == 0

    #   TODO
    #   optimalize
    def append(self, value: T) -> None:
        new_node = DoublyLinkedNode(value)

        if self.is_empty():
            self.head = new_node
            self.tail = self.head
        else:
            last_node = self.tail
            last_node.next = new_node
            new_node.previous = last_node
            self.tail = new_node

        self.length = self.length + 1

    def prepend(self, value: T) -> None:
        if self.is_empty():
            return self.append(value)

        new_node = DoublyLinkedNode(value)
        first_node = self.head
        first_node.previous = new_node
        new_node.next = first_node
        self.head = new_node

        self.length = self.length + 1

    def are_equal(self, value_fst: T, value_snd: T) -> bool:
        return self.compare(value_fst, value_snd) == 0

    def is_node_defined(
        self, node: OptionalDoublyLinkedNode
    ) -> DoublyLinkedNodeInterface:
        return bool(node is not None)

    def is_head(self, node: OptionalDoublyLinkedNode) -> bool:
        return bool(self.is_node_defined(node) and node.previous is None)

    def is_tail(self, node: OptionalDoublyLinkedNode) -> bool:
        return bool(self.is_node_defined(node) and node.next is None)

    def has_next(self, node: DoublyLinkedNodeInterface) -> bool:
        return bool(self.is_node_defined(node.next))

    def has_previous(self, node: DoublyLinkedNodeInterface) -> bool:
        return bool(self.is_node_defined(node.previous))

    def delete_head(self) -> OptionalDoublyLinkedNode:
        deleted_node = None
        if self.is_empty():
            return deleted_node

        current_node = self.head
        if self.has_next(current_node):
            next_node = current_node.next
            next_node.previous = None

            self.head = next_node
        else:
            self.head = None
            self.tail = self.head

        current_node.next = None
        deleted_node = current_node

        self.length = self.length - 1

        return deleted_node

    def delete_tail(self) -> OptionalDoublyLinkedNode:
        deleted_node = None

        if self.is_empty():
            return deleted_node

        current_node = self.tail
        if self.has_previous(current_node):
            previous_node = current_node.previous
            previous_node.next = None

            current_node.previous = None

            self.tail = previous_node

        else:
            self.head = None
            self.tail = self.head

        deleted_node = current_node

        self.length = self.length - 1

        return deleted_node

    def delete(self, value: T) -> OptionalDoublyLinkedNode:
        deleted_node = None
        if self.is_empty():
            return deleted_node

        current_node = self.head
        while current_node is not None:
            value_to_find = current_node.value

            if self.are_equal(value, value_to_find):
                if self.is_head(current_node):
                    current_node = current_node.next
                    deleted_node = self.delete_head()
                elif self.is_tail(current_node):
                    deleted_node = self.delete_tail()
                    current_node = None
                else:

                    previous_node = current_node.previous
                    previous_node.next = None

                    next_node = current_node.next
                    next_node.previous = None

                    current_node.previous = None
                    current_node.next = current_node.previous
                    deleted_node = current_node

                    previous_node.next = next_node
                    next_node.previous = previous_node

                    current_node = next_node
                    self.length = self.length - 1

            else:
                current_node = current_node.next

        return deleted_node

    def swap_head_and_tail(self) -> None:
        tmp_head = self.head
        self.head = self.tail
        self.head.previous = None
        self.head.next = tmp_head

        self.tail = tmp_head
        self.tail.next = None
        self.tail.previous = self.head

    def reverse(self) -> None:
        if self.is_empty() or self.length == 1:
            return None

            #   TODO
            #   First solution  swap
        current_node = self.tail.previous

        self.head = self.tail
        self.head.previous = None

        self.tail = self.head
        self.tail.next = None

        while current_node is not None:
            prev_node = current_node.previous

            current_node.next = None
            current_node.previous = self.tail

            self.tail.next = current_node
            self.tail = current_node

            current_node = prev_node

    def __normalize_index(self, index) -> int:
        length = self.length
        LAST_NODE_INDEX = length - 1
        FIRST_NODE_INDEX = 0

        return (
            FIRST_NODE_INDEX
            if index < 0
            else LAST_NODE_INDEX if index >= length else index
        )

    def insert(self, value: T, index: int) -> None:
        new_node = DoublyLinkedNode(value)

        if self.is_empty():
            self.head = new_node
            self.tail = self.head
            self.length = self.length + 1
        elif index <= 0:
            self.__insert_before(self.head, new_node)
        elif index >= self.length:
            self.__insert_after(self.tail, new_node)
        else:

            current_node = self.head
            index_iteration = 0

            while current_node is not None:
                if index_iteration == index:
                    if current_node.previous is not None:
                        return self.__insert_after(current_node.previous, new_node)

                index_iteration = index_iteration + 1
                current_node = current_node.next
            self.length = self.length + 1

    def __insert_after(
        self, node: DoublyLinkedNodeInterface, new_node: DoublyLinkedNodeInterface
    ) -> None:
        self.length = self.length + 1

        if self.is_tail(node):
            new_node.previous = self.tail
            self.tail.next = new_node
            self.tail = new_node
        else:
            tmp_next_node = node.next

            node.next = new_node
            new_node.previous = node

            new_node.next = tmp_next_node
            tmp_next_node.previous = new_node

    def __insert_before(
        self, node: DoublyLinkedNodeInterface, new_node: DoublyLinkedNodeInterface
    ) -> None:
        if self.is_head(node):
            new_node.next = self.head
            self.head.previous = new_node
            self.head = new_node
        else:
            tmp_prev_node = node.previous

            tmp_prev_node.next = new_node
            new_node.previous = tmp_prev_node
            new_node.next = node
            node.previous = new_node

        self.length = self.length + 1

    def is_index_lower_equal(self, index: int) -> bool:
        FIRST_NODE_INDEX = 0
        return index <= FIRST_NODE_INDEX

    def is_index_higher_equal(self, index: int, boundary: int) -> bool:
        return index >= boundary

    def delete_by_position(self, index: int) -> OptionalDoublyLinkedNode:
        deleted_node = None
        if self.is_empty():
            return deleted_node

        if self.length == 1:
            deleted_node = self.head

            self.head = None
            self.tail = self.head
            self.length = 0
            return deleted_node
        elif self.is_index_lower_equal(index):
            next_node = self.head.next

            deleted_node = self.head
            deleted_node.next = None

            next_node.previous = None
            self.head = next_node

            self.length = self.length - 1

            return deleted_node
        elif self.is_index_higher_equal(index, self.length - 1):
            previous_node = self.tail.previous
            previous_node.next = None

            deleted_node = self.tail
            deleted_node.previous = None

            self.tail = previous_node

            self.length = self.length - 1

            return deleted_node
        else:
            index_to_find = 1
            current_node = self.head.next

            while current_node is not None:
                if self.are_equal(index, index_to_find):
                    previous_node = current_node.previous
                    next_node = current_node.next

                    previous_node.next = next_node
                    next_node.previous = previous_node

                    current_node.next = None
                    current_node.previous = current_node.next

                    self.length = self.length - 1

                    return deleted_node

                index_to_find = index_to_find + 1
                current_node = current_node.next
