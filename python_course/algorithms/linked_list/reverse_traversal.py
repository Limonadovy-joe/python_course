from typing import Generic, TypeVar, Optional, Protocol, Callable, Union

from traversal import traversal

from data_structures.linked_list import LinkedList

T = TypeVar("T")


class Node(Protocol, Generic[T]):
    value: T
    next: Optional["Node[T]"]


OptionalNode = Optional[Node[T]]
Callback = Callable[[Node[T]], None]


class Traversable(Protocol, Generic[T]):
    head: OptionalNode[T]
    tail: OptionalNode[T]


def reverse(traversable: Traversable[T]) -> Traversable[T]:
    if traversable.head is None and traversable.tail is None:
        return traversable
    elif traversable.head.next is None:
        return traversable

    if traversable.head.next.next is None:
        new_tail = traversable.head
        new_head = new_tail.next
        new_head.next = new_tail
        new_tail.next = None

        traversable.tail = new_tail
        traversable.head = new_head

        return traversable

    new_head = traversable.tail
    next_node = traversable.head.next
    traversable.tail = traversable.head

    new_tail = traversable.head
    new_tail.next = None

    while next_node is not None:
        tmp_next_node = next_node.next

        tmp_tail = next_node
        tmp_tail.next = new_tail

        new_tail = tmp_tail

        next_node = tmp_next_node
        if next_node.next is None:
            break

    new_head.next = new_tail
    traversable.head = new_head

    return traversable


def reverse_traversal(traversable: Traversable[T], callback: Callback[T]) -> None:
    reversed_traversable: Traversable[T] = reverse(traversable)
    return traversal(reversed_traversable, callback)


ll = LinkedList[int]()

ll.append(1)
ll.append(2)

reverse_traversal(ll, lambda node: print("node", node, "value", node.value))
