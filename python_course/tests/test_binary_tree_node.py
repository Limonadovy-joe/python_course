import pytest

from python_course.data_structures.binary_tree_node import BinaryTreeNode


@pytest.fixture
def empty_binary_tree_node():
    bt = BinaryTreeNode()
    assert bt.value is None
    assert bt.parent is None
    assert bt.left is None
    assert bt.right is None
    return bt


# Fixture for creating left and right children
@pytest.fixture
def populated_binary_tree_node(empty_binary_tree_node, request):
    """Fixture that populates a BinaryTreeNode with given left and right child values."""
    root_value, left_value, right_value = request.param  # Extract values

    # Set root value
    empty_binary_tree_node.set_value(root_value)

    # Create and set left child if provided
    if left_value is not None:
        left_node = BinaryTreeNode(left_value)
        empty_binary_tree_node.set_left(left_node)

    # Create and set right child if provided
    if right_value is not None:
        right_node = BinaryTreeNode(right_value)
        empty_binary_tree_node.set_right(right_node)

    return empty_binary_tree_node


def test_create(empty_binary_tree_node):
    assert str(empty_binary_tree_node) == ""


@pytest.mark.parametrize(
    "populated_binary_tree_node, expected_root, expected_left, expected_right",
    [
        ((10, 5, 15), 10, 5, 15),  # Root 10, left 5, right 15
        ((20, 10, None), 20, 10, None),  # Root 20, only left child 10
        ((30, None, 40), 30, None, 40),  # Root 30, only right child 40
        ((50, None, None), 50, None, None),  # Root 50, no children
    ],
    indirect=["populated_binary_tree_node"],  # Use fixture indirectly
)
def test_set_children(
    populated_binary_tree_node, expected_root, expected_left, expected_right
):
    assert populated_binary_tree_node.value == expected_root
    assert (
        populated_binary_tree_node.left.value
        if populated_binary_tree_node.left
        else None
    ) == expected_left
    assert (
        populated_binary_tree_node.right.value
        if populated_binary_tree_node.right
        else None
    ) == expected_right


@pytest.mark.parametrize(
    "populated_binary_tree_node, expected",
    [
        (
            (10, 5, 15),
            (10, 10, 10),
        ),  # Root 10, left node parent value 10, right node parent value 10
        ((20, 10, None), (20, 20, None)),
        ((30, None, 40), (30, None, 30)),
        ((50, None, None), (50, None, None)),  # Root 50, no children, no parent
    ],
    indirect=["populated_binary_tree_node"],
)
def test_set_parent(populated_binary_tree_node, expected):
    parent_value, left__parent_value, right_parent_value = expected
    assert populated_binary_tree_node.value == parent_value

    assert (
        populated_binary_tree_node.left.parent.value
        if populated_binary_tree_node.left and populated_binary_tree_node.left.parent
        else None
    ) == left__parent_value
    assert (
        populated_binary_tree_node.right.parent.value
        if populated_binary_tree_node.right and populated_binary_tree_node.right.parent
        else None
    ) == right_parent_value


def test_traverse_in_order():
    left_node = BinaryTreeNode(2)

    right_node = BinaryTreeNode(3)
    root_node = BinaryTreeNode(1)

    root_node.set_left(left_node)
    root_node.set_right(right_node)

    left_node.set_left(BinaryTreeNode(4))
    left_node.set_right(BinaryTreeNode(5))

    right_node.set_right(BinaryTreeNode(6))

    assert [4, 2, 5, 1, 3, 6] == root_node.traverse_in_order()


@pytest.mark.parametrize(
    "populated_binary_tree_node, child_to_remove, expected_left, expected_right",
    [
        ((10, 5, 15), "left", None, 15),  # Remove left child
        ((10, 5, 15), "right", 5, None),  # Remove right child
        ((20, 10, None), "left", None, None),  # Remove only left child
        ((30, None, 40), "right", None, None),  # Remove only right child
        (
            (50, None, None),
            "left",
            None,
            None,
        ),  # Remove nonexistent left child (no change)
    ],
    indirect=["populated_binary_tree_node"],
)
def test_remove_child(
    populated_binary_tree_node, child_to_remove, expected_left, expected_right
):

    # Get reference to the child before removing
    child_node = (
        populated_binary_tree_node.left
        if child_to_remove == "left"
        else populated_binary_tree_node.right
    )

    # Perform removal
    was_removed = populated_binary_tree_node.remove_child(child_node)

    # Verify expected removal
    assert was_removed == (
        child_node is not None
    )  # Should return True if the child existed
    assert (
        populated_binary_tree_node.left.value
        if populated_binary_tree_node.left
        else None
    ) == expected_left
    assert (
        populated_binary_tree_node.right.value
        if populated_binary_tree_node.right
        else None
    ) == expected_right


def test_replace_child():
    left_node = BinaryTreeNode(1)
    right_node = BinaryTreeNode(3)
    root_node = BinaryTreeNode(2)

    root_node.set_left(left_node)
    root_node.set_right(right_node)

    assert [1, 2, 3] == root_node.traverse_in_order()

    replacement_node = BinaryTreeNode(5)
    right_node.set_right(replacement_node)

    assert [1, 2, 3, 5] == root_node.traverse_in_order()
    assert root_node.replace_child(root_node.right, replacement_node) is True
    assert root_node.right.value == 5
    assert root_node.right.right is None
    assert [1, 2, 5] == root_node.traverse_in_order()

    #   test non-existing node in the tree to replace
    assert root_node.replace_child(right_node, replacement_node) is False
    assert [1, 2, 5] == root_node.traverse_in_order()


def test_node_height():
    root = BinaryTreeNode(1)
    left = BinaryTreeNode(3)
    right = BinaryTreeNode(2)

    grand_left = BinaryTreeNode(5)
    grand_right = BinaryTreeNode(6)
    grand_grand_left = BinaryTreeNode(7)

    root.set_left(left)
    root.set_right(right)

    assert root.height == 1
    assert left.height == 0
    assert right.height == 0
    assert root.balance_factor == 0

    left.set_left(grand_left)
    right.set_right(grand_right)

    assert root.height == 2
    assert left.height == 1
    assert right.height == 1
    assert root.balance_factor == 0

    grand_left.set_left(grand_grand_left)

    assert root.height == 3
    assert left.height == 2
    assert right.height == 1
    assert root.balance_factor == 1


def test_detect_right_uncle():
    grand_parent = BinaryTreeNode("grand-parent")
    parent = BinaryTreeNode("parent")
    uncle = BinaryTreeNode("uncle")
    child = BinaryTreeNode("child")

    assert grand_parent.uncle is None
    assert parent.uncle is None

    grand_parent.set_left(parent)

    assert parent.uncle is None
    assert child.uncle is None

    parent.set_left(child)

    assert child.uncle is None

    grand_parent.set_right(uncle)

    assert parent.uncle is None
    assert child.uncle is not None and child.uncle.value == "uncle"


def test_detect_left_uncle():
    grand_parent = BinaryTreeNode("grand-parent")
    parent = BinaryTreeNode("parent")
    uncle = BinaryTreeNode("uncle")
    child = BinaryTreeNode("child")

    assert grand_parent.uncle is None
    assert parent.uncle is None

    grand_parent.set_right(parent)

    assert parent.uncle is None
    assert child.uncle is None

    parent.set_right(child)

    assert child.uncle is None

    grand_parent.set_left(uncle)

    assert parent.uncle is None
    assert child.uncle is not None and child.uncle.value == "uncle"


def test_copy_node():
    root = BinaryTreeNode("root")
    left = BinaryTreeNode("left")
    right = BinaryTreeNode("right")

    root.set_left(left)
    root.set_right(right)

    assert root.traverse_in_order() == ["left", "root", "right"]

    new_root = BinaryTreeNode("new_root")
    new_left = BinaryTreeNode("new_left")
    new_right = BinaryTreeNode("new_right")

    new_root.set_left(new_left)
    new_root.set_right(new_right)

    assert new_root.traverse_in_order() == ["new_left", "new_root", "new_right"]
    assert root.traverse_in_order() == ["left", "root", "right"]

    copied_root = BinaryTreeNode.copy_node(new_root)
    assert copied_root.traverse_in_order() == ["new_left", "new_root", "new_right"]
