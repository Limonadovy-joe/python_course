from typing import Generic, TypeVar, Optional, Protocol, List

from python_course.utils.ord import CompareFunction


T = TypeVar("T")


OptionalBinaryTreeNode = Optional["BinaryTreeNodeInterface[T]"]


class BinaryTreeNodeInterface(Protocol[T]):
    value: Optional[T]
    comparator: Optional[CompareFunction[T]]
    parent: OptionalBinaryTreeNode
    left: OptionalBinaryTreeNode
    right: OptionalBinaryTreeNode
    height: int


class BinaryTreeNode(Generic[T], BinaryTreeNodeInterface[T]):
    def __init__(
        self,
        value: Optional[T] = None,
        comparator: Optional[CompareFunction[T]] = None,
        parent: OptionalBinaryTreeNode = None,
        left: OptionalBinaryTreeNode = None,
        right: OptionalBinaryTreeNode = None,
    ):
        self.value = value

        self.comparator = comparator or self._default_comparator

        self.parent = parent
        self.left = left
        self.right = right

    def __str__(self):
        if self.value is None:
            return ""
        return str(self.value)

    def _default_comparator(self, x: T, y: T) -> int:
        """Default comparator assuming T supports comparison operators."""
        return -1 if x < y else 1 if x > y else 0  # Returns -1, 0, or 1

    def __reset_parent(
        self, node: BinaryTreeNodeInterface
    ) -> BinaryTreeNodeInterface[T]:
        node.parent = None
        return node

    def set_value(self, value: T) -> None:
        self.value = value

    def set_left(self, node: BinaryTreeNodeInterface[T]):
        if self.left is not None:
            self.__reset_parent(self.left)

        self.left = node
        if self.left is not None:
            self.left.parent = self

        return self

    def set_right(self, node: BinaryTreeNodeInterface[T]):
        if self.right is not None:
            self.__reset_parent(self.right)

        self.right = node
        if self.right is not None:
            self.right.parent = self
        return self

    def has_left(self) -> bool:
        return self.left is not None

    def has_right(self) -> bool:
        return self.right is not None

    def traverse_in_order(self) -> List[T]:
        out = []

        if self.has_left():
            out.extend(self.left.traverse_in_order())

        out.append(self.value)

        if self.has_right():
            out.extend(self.right.traverse_in_order())

        return out

    def are_nodes_equal(
        self, node_fst: BinaryTreeNodeInterface[T], node_snd: BinaryTreeNodeInterface[T]
    ) -> bool:
        return self.comparator(node_fst.value, node_snd.value) == 0

    def remove_child(self, node: BinaryTreeNodeInterface[T]) -> bool:
        for prop in ["left", "right"]:
            child: OptionalBinaryTreeNode[T] = getattr(self, prop)
            if child is not None and self.are_nodes_equal(child, node):
                child.parent = None
                setattr(self, prop, None)
                return True
        return False

    def replace_child(
        self,
        node_to_replace: BinaryTreeNodeInterface[T],
        replacement: BinaryTreeNodeInterface[T],
    ) -> bool:
        for prop, child in [("left", self.left), ("right", self.right)]:
            if child is not None and self.are_nodes_equal(child, node_to_replace):
                child.parent = None
                replacement.parent = self
                setattr(self, prop, replacement)
                return True
        return False

    @property
    def left_height(self) -> int:
        if not self.has_left():
            return 0

        return self.left.height + 1

    @property
    def right_height(self) -> int:
        if not self.has_right():
            return 0

        return self.right.height + 1

    @property
    def height(self) -> int:
        return max(self.left_height, self.right_height)

    @property
    def balance_factor(self) -> int:
        return self.left_height - self.right_height

    @property
    def uncle(self) -> OptionalBinaryTreeNode:
        uncle = None
        if self.parent is not None and self.parent.parent is not None:
            grand_parent = self.parent.parent

            if (
                grand_parent.left is not None
                and grand_parent.left.value == self.parent.value
            ):
                uncle = grand_parent.right
            else:
                uncle = grand_parent.left
        return uncle

    @staticmethod
    def copy_node(source: OptionalBinaryTreeNode) -> OptionalBinaryTreeNode:
        if source is None:
            return None

        new_node = BinaryTreeNode(source.value)

        new_node.left = BinaryTreeNode.copy_node(source.left)
        new_node.right = BinaryTreeNode.copy_node(source.right)

        if new_node.left is not None:
            new_node.left.parent = new_node

        if new_node.right is not None:
            new_node.right.parent = new_node

        return new_node
