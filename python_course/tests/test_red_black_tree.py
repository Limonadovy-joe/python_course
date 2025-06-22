import pytest

from python_course.data_structures.red_black_tree import RedBlackTree


def test_insert_first_node_color():
    red_black_tree = RedBlackTree[int]()

    first_node = red_black_tree.insert(10)

    assert red_black_tree.is_node_colored(first_node) is True
    assert red_black_tree.is_node_black(first_node) is True
    assert red_black_tree.is_node_red(first_node) is False

    assert red_black_tree.to_string() == "10"
    assert red_black_tree.root.height == 0


def test_insert_leaf_nodes_color():
    red_black_tree = RedBlackTree[int]()

    first_node = red_black_tree.insert(10)
    second_node = red_black_tree.insert(15)
    third_node = red_black_tree.insert(5)

    assert red_black_tree.is_node_black(first_node) is True
    assert red_black_tree.is_node_red(second_node) is True
    assert red_black_tree.is_node_red(third_node) is True

    assert red_black_tree.to_string() == "5,10,15"
    assert red_black_tree.root.height == 1


def test_left_left_rotation():
    red_black_tree = RedBlackTree[int]()

    node1 = red_black_tree.insert(10)
    node2 = red_black_tree.insert(-10)
    node3 = red_black_tree.insert(20)
    node4 = red_black_tree.insert(7)
    node5 = red_black_tree.insert(15)

    assert red_black_tree.to_string() == "-10,7,10,15,20"
    assert red_black_tree.root.height == 2

    assert red_black_tree.is_node_black(node1) is True
    assert red_black_tree.is_node_black(node2) is True
    assert red_black_tree.is_node_black(node3) is True
    assert red_black_tree.is_node_red(node4) is True
    assert red_black_tree.is_node_red(node5) is True

    node6 = red_black_tree.insert(13)

    assert red_black_tree.to_string() == "-10,7,10,13,15,20"
    assert red_black_tree.root.height == 2

    assert red_black_tree.is_node_black(node1) is True
    assert red_black_tree.is_node_black(node2) is True
    assert red_black_tree.is_node_black(node5) is True
    assert red_black_tree.is_node_red(node4) is True
    assert red_black_tree.is_node_red(node6) is True
    assert red_black_tree.is_node_red(node3) is True


def test_left_right_rotation():
    red_black_tree = RedBlackTree[int]()

    node1 = red_black_tree.insert(10)
    node2 = red_black_tree.insert(-10)
    node3 = red_black_tree.insert(20)
    node4 = red_black_tree.insert(7)
    node5 = red_black_tree.insert(15)

    assert red_black_tree.to_string() == "-10,7,10,15,20"
    assert red_black_tree.root.height == 2

    assert red_black_tree.is_node_black(node1) is True
    assert red_black_tree.is_node_black(node2) is True
    assert red_black_tree.is_node_black(node3) is True
    assert red_black_tree.is_node_red(node4) is True
    assert red_black_tree.is_node_red(node5) is True

    node6 = red_black_tree.insert(17)

    assert red_black_tree.to_string() == "-10,7,10,15,17,20"
    assert red_black_tree.root.height == 2

    assert red_black_tree.is_node_black(node1) is True
    assert red_black_tree.is_node_black(node2) is True
    assert red_black_tree.is_node_black(node6) is True
    assert red_black_tree.is_node_red(node4) is True
    assert red_black_tree.is_node_red(node5) is True
    assert red_black_tree.is_node_red(node3) is True


def test_right_right_rotation():
    red_black_tree = RedBlackTree[int]()

    node1 = red_black_tree.insert(10)
    node2 = red_black_tree.insert(5)
    node3 = red_black_tree.insert(30)

    assert red_black_tree.to_string() == "5,10,30"
    assert red_black_tree.root.height == 1

    assert red_black_tree.is_node_black(node1) is True
    assert red_black_tree.is_node_red(node2) is True
    assert red_black_tree.is_node_red(node3) is True

    #   only uncle red case
    node4 = red_black_tree.insert(40)

    assert red_black_tree.to_string() == "5,10,30,40"
    assert red_black_tree.root.height == 2

    #   right right case
    node5 = red_black_tree.insert(50)

    assert red_black_tree.is_node_black(node1) is True
    assert red_black_tree.is_node_black(node2) is True
    assert red_black_tree.is_node_black(node4) is True
    assert red_black_tree.is_node_red(node3) is True
    assert red_black_tree.is_node_red(node5) is True

    assert red_black_tree.to_string() == "5,10,30,40,50"
    assert red_black_tree.root.height == 2


def test_right_left_rotation():
    red_black_tree = RedBlackTree[int]()

    node1 = red_black_tree.insert(10)
    node2 = red_black_tree.insert(-10)
    node3 = red_black_tree.insert(20)
    node4 = red_black_tree.insert(-20)
    node5 = red_black_tree.insert(6)
    node6 = red_black_tree.insert(30)

    assert red_black_tree.to_string() == "-20,-10,6,10,20,30"
    assert red_black_tree.root.height == 2

    assert red_black_tree.is_node_black(node1) is True
    assert red_black_tree.is_node_black(node2) is True
    assert red_black_tree.is_node_black(node3) is True
    assert red_black_tree.is_node_red(node4) is True
    assert red_black_tree.is_node_red(node5) is True
    assert red_black_tree.is_node_red(node6) is True

    node7 = red_black_tree.insert(25)

    right_node = red_black_tree.root.right
    right_left_node = right_node.left
    right_right_node = right_node.right

    assert right_node.value == node7.value
    assert right_left_node.value == node3.value
    assert right_right_node.value == node6.value

    assert red_black_tree.to_string() == "-20,-10,6,10,20,25,30"
    assert red_black_tree.root.height == 2

    assert red_black_tree.is_node_black(node1) is True
    assert red_black_tree.is_node_black(node2) is True
    assert red_black_tree.is_node_black(node7) is True
    assert red_black_tree.is_node_red(node4) is True
    assert red_black_tree.is_node_red(node5) is True
    assert red_black_tree.is_node_red(node3) is True
    assert red_black_tree.is_node_red(node6) is True


def test_left_left_rotation_with_left_grandparent():
    red_black_tree = RedBlackTree[int]()

    red_black_tree.insert(20)
    red_black_tree.insert(15)
    red_black_tree.insert(25)
    red_black_tree.insert(10)
    red_black_tree.insert(5)

    assert red_black_tree.to_string() == "5,10,15,20,25"
    assert red_black_tree.root.height == 2


def test_right_right_rotation_with_left_grandparent():
    red_black_tree = RedBlackTree[int]()

    red_black_tree.insert(20)
    red_black_tree.insert(15)
    red_black_tree.insert(25)
    red_black_tree.insert(17)
    red_black_tree.insert(19)

    assert red_black_tree.to_string() == "15,17,19,20,25"
    assert red_black_tree.root.height == 2
