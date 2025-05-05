import sys
import os

# Dynamically add the root directory of the project to the Python path
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)

from dataclasses import dataclass
from typing import Generic, TypeVar, Optional, Callable


from python_course.data_structures.binary_tree_node import (
    BinaryTreeNode,
    BinaryTreeNodeInterface,
)

T = TypeVar("T")

NodeCallback = Callable[[BinaryTreeNodeInterface[T]], None]
NodeChildCallback = Callable[[BinaryTreeNodeInterface[T]], bool]


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


@dataclass
class NormalizedTraversalCallbacks(Generic[T]):
    allow_traversal: NodeChildCallback[T]
    enter_node: NodeCallback[T]
    leave_node: NodeCallback[T]


def init_callbacks(
    callbacks: Optional[TraversalCallbacks[T]],
) -> "NormalizedTraversalCallbacks[T]":
    node_cb: NodeCallback[T] = lambda node: None
    allow_traversal: NodeChildCallback[T] = lambda node: True

    norm_callbacks = NormalizedTraversalCallbacks(
        allow_traversal=allow_traversal,
        enter_node=node_cb,
        leave_node=node_cb,
    )

    defined_callbacks = (
        list(callbacks.get_properties().items()) if callbacks is not None else []
    )

    for prop, value in defined_callbacks:
        if value is not None:
            setattr(norm_callbacks, prop, value)

    return norm_callbacks


def breadth_first_search(
    node: BinaryTreeNodeInterface[T],
    input_callbacks: Optional[TraversalCallbacks[T]] = None,
) -> None:
    callbacks = init_callbacks(input_callbacks)
    enter_node = callbacks.enter_node
    leave_node = callbacks.leave_node
    allow_traversal = callbacks.allow_traversal

    nodes = [node]

    while nodes:
        node_to_traverse = nodes.pop(0)  # Remove the first item from the list
        enter_node(node_to_traverse)
        should_traverse = allow_traversal(node_to_traverse)

        if (
            node_to_traverse.left
            and should_traverse
            and allow_traversal(node_to_traverse.left)
        ):
            nodes.append(node_to_traverse.left)

        if (
            node_to_traverse.right
            and should_traverse
            and allow_traversal(node_to_traverse.right)
        ):
            nodes.append(node_to_traverse.right)

        leave_node(node_to_traverse)
