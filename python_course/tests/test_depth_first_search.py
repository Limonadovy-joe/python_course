import pytest

from python_course.algorithms.tree.depth_first_search import (
    depth_first_search,
    TraversalCallbacks,
)
from python_course.data_structures.binary_tree_node import (
    BinaryTreeNode,
    BinaryTreeNodeInterface,
)


def test_perform_in_order_traversal():
    node_A = BinaryTreeNode("A")
    node_B = BinaryTreeNode("B")
    node_C = BinaryTreeNode("C")
    node_D = BinaryTreeNode("D")
    node_E = BinaryTreeNode("E")
    node_F = BinaryTreeNode("F")
    node_G = BinaryTreeNode("G")

    # Building the tree
    node_A.set_left(node_B).set_right(node_C)
    node_B.set_left(node_D).set_right(node_E)
    node_C.set_left(node_F).set_right(node_G)

    node_A.traverse_in_order() == ["D", "B", "E", "A", "F", "C", "G"]

    enter_node_callback = []
    leave_node_callback = []

    # Define mock functions to track the calls
    def mock_enter_node(node):
        enter_node_callback.append(node)

    def mock_leave_node(node):
        leave_node_callback.append(node)

    callbacks = TraversalCallbacks(
        enter_node=mock_enter_node, leave_node=mock_leave_node
    )

    # Perform depth-first search (DFS) on the tree with mocked callbacks
    depth_first_search(node_A, callbacks)

    # Check if the callbacks were called 7 times (once for each node)
    assert len(enter_node_callback) == 7
    assert len(leave_node_callback) == 7

    # Check node entering order (based on depth-first search)
    assert enter_node_callback[0].value == "A"
    assert enter_node_callback[1].value == "B"
    assert enter_node_callback[2].value == "D"
    assert enter_node_callback[3].value == "E"
    assert enter_node_callback[4].value == "C"
    assert enter_node_callback[5].value == "F"
    assert enter_node_callback[6].value == "G"

    # Check leave order (after entering)
    assert leave_node_callback[0].value == "D"
    assert leave_node_callback[1].value == "E"
    assert leave_node_callback[2].value == "B"
    assert leave_node_callback[3].value == "F"
    assert leave_node_callback[4].value == "G"
    assert leave_node_callback[5].value == "C"
    assert leave_node_callback[6].value == "A"


def test_perform_in_order_traversal_only_on_right_subtree():
    # Create nodes
    node_A = BinaryTreeNode("A")
    node_B = BinaryTreeNode("B")
    node_C = BinaryTreeNode("C")
    node_D = BinaryTreeNode("D")
    node_E = BinaryTreeNode("E")
    node_F = BinaryTreeNode("F")
    node_G = BinaryTreeNode("G")

    # Build the tree
    node_A.set_left(node_B).set_right(node_C)
    node_B.set_left(node_D).set_right(node_E)
    node_C.set_left(node_F).set_right(node_G)

    # Create callback lists to track calls
    enter_node_callback = []
    leave_node_callback = []

    def mock_enter_node(node):
        enter_node_callback.append(node)

    def mock_leave_node(node):
        leave_node_callback.append(node)

    # Traverse the tree without any specific callbacks
    depth_first_search(node_A)

    callbacks = TraversalCallbacks(
        lambda node, child: child.value != "B",
        mock_enter_node,
        mock_leave_node,
    )

    # Now traverse with callbacks
    depth_first_search(node_A, callbacks)

    # Check callback call counts
    assert len(enter_node_callback) == 4
    assert len(leave_node_callback) == 4

    # Check node entering order (A, C, F, G)
    assert enter_node_callback[0].value == "A"
    assert enter_node_callback[1].value == "C"
    assert enter_node_callback[2].value == "F"
    assert enter_node_callback[3].value == "G"

    # Check node leaving order (F, G, C, A)
    assert leave_node_callback[0].value == "F"
    assert leave_node_callback[1].value == "G"
    assert leave_node_callback[2].value == "C"
    assert leave_node_callback[3].value == "A"
