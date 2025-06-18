from typing import TypeVar, Optional, Generic, List, Literal, Tuple, Union
from enum import Enum


from python_course.utils.ord import CompareFunction
from python_course.data_structures.binary_search_tree_node import BinarySearchTreeNode

T = TypeVar("T")


class Position(str, Enum):
    LEFT = "Left"
    RIGHT = "Right"
    ROOT = "Root"


Inorder = Tuple[Literal[Position.LEFT], Literal[Position.ROOT], Literal[Position.RIGHT]]
inorder: Inorder = (Position.LEFT, Position.ROOT, Position.RIGHT)

InorderReversed = Tuple[
    Literal[Position.RIGHT], Literal[Position.ROOT], Literal[Position.LEFT]
]
inorder_reversed = (
    Position.RIGHT,
    Position.ROOT,
    Position.LEFT,
)

Order = Union[Inorder, InorderReversed]


def create_inorder() -> Inorder:
    return (Position.LEFT, Position.ROOT, Position.RIGHT)


def create_reversed_inorder() -> InorderReversed:
    return (Position.RIGHT, Position.ROOT, Position.LEFT)


def get_child(
    node: "BinarySearchTreeNode[T]", position: Position
) -> Optional["BinarySearchTreeNode[T]"]:
    if position == Position.LEFT:
        return node.left
    elif position == Position.RIGHT:
        return node.right
    else:
        return None


class BinarySearchTree(Generic[T]):

    def __init__(
        self,
        comparator: Optional[CompareFunction[T]] = None,
    ):
        #   TODO
        # Support custom comparison functions for objects
        self.root = BinarySearchTreeNode[T]()
        self.comparator = comparator

    def to_string(self) -> str:
        return self.root.to_string()

    def is_root_empty(self) -> bool:
        return self.root is None or self.root.value is None

    def insert(self, value: T) -> "BinarySearchTreeNode[T]":
        if self.is_root_empty():
            self.root = BinarySearchTreeNode(value)
            return self.root
        node = self.root.insert(value)
        if node is None:
            raise RuntimeError(
                f"Value '{value}' already exists in the binary search tree and cannot be inserted again."
            )
        return node

    def find(self, value: T) -> "BinarySearchTreeNode[T]":
        node = self.root.find(value)
        if node is None:
            raise RuntimeError(
                f"Value '{value}' was not found in the binary search tree."
            )
        return node

    def remove(self, value: T) -> bool:
        node_removed = self.root.remove(value)
        return node_removed is not None

    def in_order_traversal_rec(
        self,
        order: Order,
        node: Optional["BinarySearchTreeNode[T]"] = None,
    ) -> List[T]:
        output = []
        node_to_traverse = self.root if node is None else node

        position_first, position_root, position_second = order
        first_child, second_child = [
            get_child(node_to_traverse, pos)
            for pos in (position_first, position_second)
        ]

        # Map Position to attribute name

        if first_child is not None:
            left_values = self.in_order_traversal_rec(order, first_child)
            output.extend(left_values)

        output.append(node_to_traverse.value)

        if second_child is not None:
            right_values = self.in_order_traversal_rec(order, second_child)
            output.extend(right_values)

        return output

    def in_order_traversal(
        self,
        reverse: bool = False,
    ) -> List[T]:
        order: Order = create_reversed_inorder() if reverse else create_inorder()
        return self.in_order_traversal_rec(order)

    #   Inorder Tree Traversal without Recursion
    def in_order_traversal_using_stack(self) -> List[T]:
        node = self.root
        output: List[T] = []
        if not BinarySearchTreeNode.is_defined(node):
            return output

        stack: List["BinarySearchTreeNode[T]"] = []

        while len(stack) > 0 or node is not None:

            #   get left-most node
            while node is not None:
                stack.append(node)
                node = node.left

            node = stack.pop()
            output.append(node.value)
            node = node.right

        return output
