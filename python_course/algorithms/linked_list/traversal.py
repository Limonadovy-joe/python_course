from typing import (
    TypeVar,
    Callable,
)


from utils.node import OptionalNode

from data_structures.linked_list import LinkedList

from .traversable import Traversable

T = TypeVar("T")


Callback = Callable[[OptionalNode[T]], None]


def traversal(traversable: Traversable[T], callback: Callback[T]) -> None:
    current_node: OptionalNode[T] = traversable.head

    while current_node is not None:
        callback(current_node)
        current_node = current_node.next


ll = LinkedList[int]()
ll.append(1)
ll.append(2)
ll.append(3)
ll.append(4)
ll.append(5)


traversal(ll, lambda node: print("node", node, "value", node.value))
