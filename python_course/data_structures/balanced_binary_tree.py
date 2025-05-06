from typing import TypeVar, Optional


from python_course.data_structures.binary_tree_node import (
    BinaryTreeNode,
)

T = TypeVar("T")


def is_balanced_top_down(root: Optional[BinaryTreeNode[T]]) -> bool:

    if root is None:
        return True

    if abs(root.left_height - root.right_height) > 1:
        return False

    return True


# bottom up
def is_balanced_rec(root: Optional[BinaryTreeNode[T]]) -> int:

    if root is None:
        return 0

    left_height = is_balanced_rec(root.left)
    right_height = is_balanced_rec(root.right)

    if left_height == -1 or right_height == -1 or abs(left_height - right_height) > 1:
        return -1

    return max(left_height, right_height) + 1


def is_balanced_bottom_up(root: Optional[BinaryTreeNode[T]]) -> bool:
    return is_balanced_rec(root) > 0
