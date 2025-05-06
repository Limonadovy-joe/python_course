import pytest

from python_course.data_structures.binary_tree_node import BinaryTreeNode
from python_course.data_structures.balanced_binary_tree import (
    is_balanced_bottom_up,
    is_balanced_top_down,
)


def test_is_balanced_top_down():
    # Arrange: Create test cases for balanced and unbalanced trees
    balanced_tree = BinaryTreeNode(1)
    balanced_tree.set_left(BinaryTreeNode(2))
    balanced_tree.set_right(BinaryTreeNode(3))

    unbalanced_tree = BinaryTreeNode(1)
    unbalanced_tree.left = BinaryTreeNode(2)
    unbalanced_tree.right = BinaryTreeNode(3)
    unbalanced_tree.left.left = BinaryTreeNode(4)
    unbalanced_tree.left.right = BinaryTreeNode(5)
    unbalanced_tree.left.left.left = BinaryTreeNode(8)

    # Act & Assert
    assert is_balanced_top_down(balanced_tree) is True
    assert is_balanced_top_down(unbalanced_tree) is False


def test_is_balanced_bottom_up():
    # Arrange: Create test cases for balanced and unbalanced trees
    balanced_tree = BinaryTreeNode(1)
    balanced_tree.set_left(BinaryTreeNode(2))
    balanced_tree.set_right(BinaryTreeNode(3))

    unbalanced_tree = BinaryTreeNode(1)
    unbalanced_tree.left = BinaryTreeNode(2)
    unbalanced_tree.right = BinaryTreeNode(3)
    unbalanced_tree.left.left = BinaryTreeNode(4)
    unbalanced_tree.left.right = BinaryTreeNode(5)
    unbalanced_tree.left.left.left = BinaryTreeNode(8)

    # Act & Assert
    assert is_balanced_bottom_up(balanced_tree) is True
    assert is_balanced_bottom_up(unbalanced_tree) is False
