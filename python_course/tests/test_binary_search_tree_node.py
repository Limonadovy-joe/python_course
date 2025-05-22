import pytest

from python_course.data_structures.binary_search_tree_node import BinarySearchTreeNode


def test_create_node():
    bst_node = BinarySearchTreeNode(2)

    assert bst_node.value == 2
    assert bst_node.left is None
    assert bst_node.right is None


def test_insert():
    bst_node = BinarySearchTreeNode(2)

    inserted_node_1 = bst_node.insert(1)

    assert inserted_node_1.value == 1
    assert bst_node.to_string() == "1,2"

    inserted_node_2 = bst_node.insert(3)

    assert inserted_node_2.value == 3
    assert bst_node.to_string() == "1,2,3"

    inserted_node_3 = bst_node.insert(7)

    assert inserted_node_3.value == 7
    assert bst_node.to_string() == "1,2,3,7"

    inserted_node_4 = bst_node.insert(4)

    assert inserted_node_4.value == 4
    assert bst_node.to_string() == "1,2,3,4,7"

    inserted_node_5 = bst_node.insert(6)

    assert inserted_node_5.value == 6
    assert bst_node.to_string() == "1,2,3,4,6,7"


def test_insert_duplicates():
    bst_node = BinarySearchTreeNode(2)

    bst_node.insert(1)
    bst_node.insert(3)
    bst_node.insert(7)
    bst_node.insert(4)
    bst_node.insert(6)

    # Try to insert duplicates
    duplicate_1 = bst_node.insert(3)
    duplicate_2 = bst_node.insert(7)
    duplicate_3 = bst_node.insert(1)

    # Should not insert duplicates, so returned nodes should be None
    assert duplicate_1 is None
    assert duplicate_2 is None
    assert duplicate_3 is None

    # Tree structure should remain unchanged
    assert bst_node.to_string() == "1,2,3,4,6,7"


def test_find_min_node():
    bst_node = BinarySearchTreeNode(10)
    bst_node.insert(20)
    bst_node.insert(30)
    bst_node.insert(5)
    bst_node.insert(40)
    bst_node.insert(1)

    min_node = bst_node.find_min()
    assert min_node is not None
    assert min_node.value == 1


def test_find_min_node_with_duplicates_and_negative_values():
    bst_node = BinarySearchTreeNode(15)
    bst_node.insert(10)
    bst_node.insert(20)
    bst_node.insert(8)
    bst_node.insert(12)
    bst_node.insert(17)
    bst_node.insert(25)
    bst_node.insert(-5)
    bst_node.insert(0)
    bst_node.insert(8)  # duplicate, should not be inserted

    min_node = bst_node.find_min()
    assert min_node is not None
    assert min_node.value == -5

    # Ensure the tree structure is correct (in-order traversal)
    assert bst_node.to_string() == "-5,0,8,10,12,15,17,20,25"


def test_attach_meta_information():
    bst_node = BinarySearchTreeNode(10)

    bst_node.insert(20)
    node1 = bst_node.insert(30)
    bst_node.insert(5)
    bst_node.insert(40)
    node2 = bst_node.insert(1)

    bst_node.meta["color"] = "red"
    node1.meta["color"] = "black"
    node2.meta["color"] = "white"

    assert bst_node.meta.get("color") == "red"

    min_node = bst_node.find_min()
    assert min_node is not None
    assert min_node.value == 1
    assert min_node.meta.get("color") == "white"


def test_find():
    bst_node = BinarySearchTreeNode(10)

    bst_node.insert(20)
    bst_node.insert(30)
    bst_node.insert(5)
    bst_node.insert(40)
    bst_node.insert(1)

    assert bst_node.find(6) is None
    found_node = bst_node.find(5)
    assert found_node is not None
    assert found_node.value == 5


def test_remove_leaf_nodes():
    bst_node = BinarySearchTreeNode(10)

    bst_node.insert(10)
    bst_node.insert(20)
    bst_node.insert(5)
    assert bst_node.to_string() == "5,10,20"

    bst_node.remove(5)
    assert bst_node.to_string() == "10,20"

    bst_node.remove(20)
    assert bst_node.to_string() == "10"


def test_remove_nodes_with_one_child():
    bst_node = BinarySearchTreeNode(10)

    bst_node.insert(10)
    bst_node.insert(20)
    bst_node.insert(5)
    bst_node.insert(30)

    assert bst_node.to_string() == "5,10,20,30"

    bst_node.remove(20)
    assert bst_node.to_string() == "5,10,30"

    bst_node.insert(1)
    assert bst_node.to_string() == "1,5,10,30"

    bst_node.remove(5)
    assert bst_node.to_string() == "1,10,30"


def test_remove_nodes_with_two_children():
    bst_node = BinarySearchTreeNode(10)

    bst_node.insert(10)
    bst_node.insert(20)
    bst_node.insert(5)
    bst_node.insert(30)
    bst_node.insert(15)
    bst_node.insert(25)

    assert bst_node.to_string() == "5,10,15,20,25,30"

    bst_node.remove(20)
    assert bst_node.to_string() == "5,10,15,25,30"

    bst_node.remove(15)
    assert bst_node.to_string() == "5,10,25,30"

    bst_node.remove(10)
    assert bst_node.to_string() == "5,25,30"

    bst_node.remove(25)
    assert bst_node.to_string() == "5,30"

    bst_node.remove(5)
    assert bst_node.to_string() == "30"

    bst_node.remove(30)
    assert bst_node.to_string() == ""
