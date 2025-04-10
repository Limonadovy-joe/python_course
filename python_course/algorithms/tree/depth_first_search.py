from typing import Generic, TypeVar, Optional, Protocol, List, Callable

from python_course.data_structures.binary_tree_node import (
    BinaryTreeNodeInterface,
)

T = TypeVar("T")

NodeCallback = Callable[[BinaryTreeNodeInterface[T]], BinaryTreeNodeInterface[T]]
NodeChildCallback = Callable[
    [BinaryTreeNodeInterface[T], BinaryTreeNodeInterface[T]], bool
]


class TraversalCallbacks(Generic[T]):
    def __init__(
        self,
        allow_traversal: Optional[NodeChildCallback[T]] = None,
        enter_node: Optional[NodeCallback[T]] = None,
        leave_node: Optional[NodeCallback[T]] = None,
    ):
        self.allow_traversal = allow_traversal
        self.enter_node = enter_node
        self.leave_node = leave_node

    def get_properties(self):
        return vars(self)


def init_callbacks(
    callbacks: Optional[TraversalCallbacks[T]],
) -> "TraversalCallbacks[T]":
    node_cb: NodeCallback[T] = lambda node: node
    allow_traversal: NodeChildCallback[T] = lambda node, child: True

    default_callbacks = TraversalCallbacks[T](
        allow_traversal=allow_traversal,
        enter_node=node_cb,
        leave_node=node_cb,
    )

    if callbacks is not None:
        for prop, value in callbacks.get_properties().items():
            if value is not None:
                setattr(default_callbacks, prop, value)

    return default_callbacks


def depth_first_search_recursive(
    node: BinaryTreeNodeInterface[T], callbacks: TraversalCallbacks[T]
) -> None:

    callbacks.enter_node(node)

    allow_traversal = callbacks.allow_traversal

    if node.left is not None and allow_traversal(node, node.left):
        depth_first_search_recursive(node.left, callbacks)

    if node.right is not None and allow_traversal(node, node.right):
        depth_first_search_recursive(node.right, callbacks)

    callbacks.leave_node(node)


def depth_first_search(
    node: BinaryTreeNodeInterface[T],
    traversal_callbacks: Optional[TraversalCallbacks[T]] = None,
) -> None:
    callbacks = init_callbacks(traversal_callbacks)

    return depth_first_search_recursive(node, callbacks)
