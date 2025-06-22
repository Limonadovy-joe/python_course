from typing import TypeVar, Optional, Union, TypeGuard
from enum import Enum


from python_course.data_structures.binary_tree_node import (
    BinaryTreeNode,
)
from python_course.utils.ord import CompareFunction
from python_course.data_structures.binary_search_tree_node import BinarySearchTreeNode
from python_course.data_structures.binary_search_tree import BinarySearchTree


T = TypeVar("T")


class RedBlackTreeColor(str, Enum):
    RED = "red"
    BLACK = "black"


def is_red_black_tree_color(value: object) -> TypeGuard[RedBlackTreeColor]:
    return isinstance(value, RedBlackTreeColor)


class TreeDirection(str, Enum):
    LEFT = "left"
    RIGHT = "right"


#   prop name in dict
COLOR = "color"


class RedBlackTree(BinarySearchTree[T]):
    def __init__(
        self,
        comparator: Optional[CompareFunction[T]] = None,
    ):
        super().__init__(comparator=comparator)

    def change_node_color(
        self, node: BinaryTreeNode[T], color: RedBlackTreeColor
    ) -> BinaryTreeNode:
        node.meta["color"] = color
        return node

    def set_node_red_color(self, node: BinaryTreeNode[T]) -> BinaryTreeNode[T]:
        return self.change_node_color(node, RedBlackTreeColor.RED)

    def set_node_black_color(self, node: BinaryTreeNode[T]) -> BinaryTreeNode[T]:
        return self.change_node_color(node, RedBlackTreeColor.BLACK)

    def get_color(self, node: BinaryTreeNode[T]) -> Union[RedBlackTreeColor, str]:
        color = node.meta.get("color")
        if color is None:
            return ""
        return RedBlackTreeColor(color)

    def is_node_red(self, node: BinaryTreeNode[T]) -> bool:
        return self.get_color(node) == RedBlackTreeColor.RED

    def is_node_black(self, node: BinaryTreeNode[T]) -> bool:
        return self.get_color(node) == RedBlackTreeColor.BLACK

    def is_node_colored(self, node: BinaryTreeNode[T]) -> bool:
        return self.is_node_red(node) or self.is_node_black(node)

    def is_left_left_case(
        self,
        current_node: BinaryTreeNode[T],
        parent: BinaryTreeNode[T],
        grandparent: BinaryTreeNode[T],
    ) -> bool:
        return (
            self.is_node_red(current_node)
            and self.is_node_red(parent)
            and parent.left is not None
            and parent.left.value == current_node.value
            and grandparent.left is not None
            and grandparent.left.value == parent.value
        )

    def is_uncle_red(self, uncle: BinaryTreeNode[T]) -> bool:
        return self.is_node_red(uncle)

    def handle_uncle_red(
        self,
        parent: BinaryTreeNode[T],
        uncle: BinaryTreeNode[T],
        grandparent: BinaryTreeNode[T],
        is_grandparent_root: bool,
    ):
        self.set_node_black_color(parent)
        self.set_node_black_color(uncle)
        if is_grandparent_root:
            self.set_node_black_color(grandparent)
        else:
            self.set_node_red_color(grandparent)

    def is_uncle_black(self, uncle: BinaryTreeNode[T]) -> bool:
        return self.is_node_black(uncle)

    def is_grandparent_root_node(self, grandparent: BinaryTreeNode[T]) -> bool:
        return self.root is not None and self.root.value == grandparent.value

    def is_grandparent_from(
        self,
        grandparent: BinaryTreeNode[T],
        grand_grand_parent: BinaryTreeNode[T],
        direction: TreeDirection,
    ) -> bool:

        if grand_grand_parent and getattr(grand_grand_parent, direction):
            return getattr(grand_grand_parent, direction).value == grandparent.value

        return False

    def right_rotate_grandparent(
        self,
        parent: BinaryTreeNode[T],
        grandparent: BinaryTreeNode[T],
        is_grandparent_root: bool,
    ) -> None:
        if is_grandparent_root:
            parent.parent = None
            self.root = parent

            if parent.right:
                # when set left, if grandparent has left  ->  resets left node parent
                grandparent.set_left(parent.right)
                # maybe still reference to subtree T3
                parent.right = None
            else:
                grandparent.left = None

            parent.set_right(grandparent)
        else:
            #   whether grandparent is come from the left or right subtree
            grand_grand_parent = grandparent.parent
            if grand_grand_parent:
                if self.is_grandparent_from(
                    grandparent, grand_grand_parent, TreeDirection.LEFT
                ):
                    grand_grand_parent.set_left(parent)
                elif self.is_grandparent_from(
                    grandparent, grand_grand_parent, TreeDirection.RIGHT
                ):
                    grand_grand_parent.set_right(parent)

                if parent.right:
                    # reset grandparent left because new left - parent node in grand grand parent has this parent
                    grandparent.left = None

                    # when set left, if grandparent has left  ->  resets left node parent
                    grandparent.set_left(parent.right)
                    # maybe still reference to subtree T3
                    parent.right = None
                else:
                    grandparent.left = None

                parent.set_right(grandparent)

    def left_rotate_grandparent(
        self,
        parent: BinaryTreeNode[T],
        grandparent: BinaryTreeNode[T],
        is_grandparent_root: bool,
    ) -> None:
        if is_grandparent_root:
            parent.parent = None
            self.root = parent

            if parent.left:
                grandparent.set_right(parent.left)
                # still reference to subtree T3
                parent.left = None
            else:
                grandparent.right = None

            parent.set_left(grandparent)
        else:
            #   whether grandparent is come from the left or right subtree
            grand_grand_parent = grandparent.parent
            if grand_grand_parent:
                if self.is_grandparent_from(
                    grandparent, grand_grand_parent, TreeDirection.LEFT
                ):
                    grand_grand_parent.set_left(parent)
                elif self.is_grandparent_from(
                    grandparent, grand_grand_parent, TreeDirection.RIGHT
                ):
                    grand_grand_parent.set_right(parent)

                    #   handle T3 subtree which should be moved to grandparent
                if parent.left:
                    grandparent.set_right(parent.left)
                    # still reference to subtree T3
                    parent.left = None
                else:
                    grandparent.right = None

                parent.set_left(grandparent)

    def left_rotate_parent(
        self,
        current_node: BinaryTreeNode[T],
        parent: BinaryTreeNode[T],
        grandparent: BinaryTreeNode[T],
    ) -> None:
        grandparent.set_left(current_node)
        #   parent node now does not have Parent
        #   handle current node subtree left - T2
        if current_node.left:
            parent.set_right(current_node.left)
        else:
            parent.right = None

        current_node.set_left(parent)

    def right_rotate_parent(
        self,
        current_node: BinaryTreeNode[T],
        parent: BinaryTreeNode[T],
        grandparent: BinaryTreeNode[T],
    ) -> None:

        grandparent.set_right(current_node)

        parent.left = None
        #   handle T4 subtree should be moved if exist
        if current_node.right:
            parent.set_left(current_node.right)

        current_node.set_right(parent)

    def swap_nodes_colors(
        self, grandparent: BinaryTreeNode[T], parent: BinaryTreeNode[T]
    ) -> None:
        grandparent_color = self.get_color(grandparent)
        parent_color = self.get_color(parent)

        if is_red_black_tree_color(grandparent_color) and is_red_black_tree_color(
            parent_color
        ):
            self.change_node_color(grandparent, parent_color)
            self.change_node_color(parent, grandparent_color)

    def is_left_right_case(
        self,
        current_node: BinaryTreeNode[T],
        parent: BinaryTreeNode[T],
        grandparent: BinaryTreeNode[T],
    ) -> bool:
        return (
            self.is_node_red(current_node)
            and self.is_node_red(parent)
            and parent.right is not None
            and parent.right.value == current_node.value
            and grandparent.left is not None
            and grandparent.left.value == parent.value
        )

    def is_right_right_case(
        self,
        current_node: BinaryTreeNode[T],
        parent: BinaryTreeNode[T],
        grandparent: BinaryTreeNode[T],
    ) -> bool:
        return (
            self.is_node_red(current_node)
            and self.is_node_red(parent)
            and parent.right is not None
            and parent.right.value == current_node.value
            and grandparent.right is not None
            and grandparent.right.value == parent.value
        )

    def is_right_left_case(
        self,
        current_node: BinaryTreeNode[T],
        parent: BinaryTreeNode[T],
        grandparent: BinaryTreeNode[T],
    ) -> bool:
        return (
            self.is_node_red(current_node)
            and self.is_node_red(parent)
            and parent.left is not None
            and parent.left.value == current_node.value
            and grandparent.right is not None
            and grandparent.right.value == parent.value
        )

    def balance(self, current_node: BinaryTreeNode[T]) -> None:
        parent = current_node.parent
        grandparent = parent.parent if parent else None
        uncle = current_node.uncle

        if parent and grandparent:
            is_grandparent_root = self.is_grandparent_root_node(grandparent)

            if self.is_left_left_case(current_node, parent, grandparent):

                if uncle and self.is_uncle_red(uncle):
                    return self.handle_uncle_red(
                        parent, uncle, grandparent, is_grandparent_root
                    )

                #   else uncle is black or none
                self.right_rotate_grandparent(parent, grandparent, is_grandparent_root)
                self.swap_nodes_colors(grandparent, parent)
            elif self.is_left_right_case(current_node, parent, grandparent):

                if uncle and self.is_uncle_red(uncle):
                    return self.handle_uncle_red(
                        parent, uncle, grandparent, is_grandparent_root
                    )

                self.left_rotate_parent(current_node, parent, grandparent)
                self.right_rotate_grandparent(
                    current_node, grandparent, is_grandparent_root
                )
                self.swap_nodes_colors(grandparent, current_node)
            elif self.is_right_right_case(current_node, parent, grandparent):
                if uncle and self.is_uncle_red(uncle):
                    return self.handle_uncle_red(
                        parent, uncle, grandparent, is_grandparent_root
                    )
                self.left_rotate_grandparent(parent, grandparent, is_grandparent_root)
                self.swap_nodes_colors(grandparent, parent)
            elif self.is_right_left_case(current_node, parent, grandparent):
                if uncle and self.is_uncle_red(uncle):
                    return self.handle_uncle_red(
                        parent, uncle, grandparent, is_grandparent_root
                    )
                self.right_rotate_parent(current_node, parent, grandparent)
                self.left_rotate_grandparent(
                    current_node, grandparent, is_grandparent_root
                )
                self.swap_nodes_colors(grandparent, current_node)

    def insert(self, value: T) -> BinarySearchTreeNode[T]:

        node = super().insert(value)
        inserted_node = node
        is_root_node = node.parent is None

        if is_root_node:
            self.set_node_black_color(node)
        else:
            self.set_node_red_color(node)

        while node is not None:
            self.balance(node)
            if node.parent:
                node = node.parent.parent
            else:
                node = None

        return inserted_node
