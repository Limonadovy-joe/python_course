import pytest

from python_course.data_structures.avl_tree import AvlTree


def test_simple_left_left_rotation():
    avl_tree = AvlTree[int]()

    avl_tree.insert(4)
    avl_tree.insert(3)
    avl_tree.insert(2)

    assert avl_tree.to_string() == "2,3,4"
    assert avl_tree.root.value == 3
    assert avl_tree.root.height == 1

    avl_tree.insert(1)

    assert avl_tree.to_string() == "1,2,3,4"
    assert avl_tree.root.value == 3
    assert avl_tree.root.height == 2

    avl_tree.insert(0)

    assert avl_tree.to_string() == "0,1,2,3,4"
    assert avl_tree.root.value == 3
    assert avl_tree.root.left.value == 1
    assert avl_tree.root.height == 2


def test_complex_left_left_rotation():
    avl_tree = AvlTree[int]()

    avl_tree.insert(30)
    avl_tree.insert(20)
    avl_tree.insert(40)
    avl_tree.insert(10)

    assert avl_tree.to_string() == "10,20,30,40"
    assert avl_tree.root.value == 30
    assert avl_tree.root.height == 2

    avl_tree.insert(25)
    assert avl_tree.to_string() == "10,20,25,30,40"
    assert avl_tree.root.value == 30
    assert avl_tree.root.height == 2

    avl_tree.insert(5)
    assert avl_tree.to_string() == "5,10,20,25,30,40"
    assert avl_tree.root.value == 20
    assert avl_tree.root.left.value == 10
    assert avl_tree.root.right.value == 30
    assert avl_tree.root.height == 2


def test_simple_right_right_rotation():
    avl_tree = AvlTree[int]()

    avl_tree.insert(2)
    avl_tree.insert(3)
    avl_tree.insert(4)

    assert avl_tree.to_string() == "2,3,4"
    assert avl_tree.root.value == 3
    assert avl_tree.root.height == 1

    avl_tree.insert(5)

    assert avl_tree.to_string() == "2,3,4,5"
    assert avl_tree.root.value == 3
    assert avl_tree.root.height == 2

    avl_tree.insert(6)

    assert avl_tree.to_string() == "2,3,4,5,6"
    assert avl_tree.root.value == 3
    assert avl_tree.root.right is not None and avl_tree.root.right.value == 5
    assert avl_tree.root.height == 2


def test_complex_right_right_rotation():
    avl_tree = AvlTree[int]()

    avl_tree.insert(30)
    avl_tree.insert(20)
    avl_tree.insert(40)
    avl_tree.insert(50)

    assert avl_tree.to_string() == "20,30,40,50"
    assert avl_tree.root.value == 30
    assert avl_tree.root.height == 2

    avl_tree.insert(35)

    assert avl_tree.to_string() == "20,30,35,40,50"
    assert avl_tree.root.value == 30
    assert avl_tree.root.height == 2

    avl_tree.insert(55)

    assert avl_tree.to_string() == "20,30,35,40,50,55"
    assert avl_tree.root.value == 40
    assert avl_tree.root.left is not None and avl_tree.root.left.value == 30
    assert avl_tree.root.right is not None and avl_tree.root.right.value == 50
    assert avl_tree.root.height == 2


def test_left_right_rotation():
    avl_tree = AvlTree[int]()

    avl_tree.insert(30)
    avl_tree.insert(20)
    avl_tree.insert(25)

    assert avl_tree.to_string() == "20,25,30"
    assert avl_tree.root.value == 25
    assert avl_tree.root.height == 1


def test_right_left_rotation():
    avl_tree = AvlTree[int]()

    avl_tree.insert(30)
    avl_tree.insert(40)
    avl_tree.insert(35)

    assert avl_tree.to_string() == "30,35,40"
    assert avl_tree.root.value == 35
    assert avl_tree.root.height == 1


def test_remove_value_left_left_rotation():
    avl_tree = AvlTree[int]()

    avl_tree.insert(10)
    avl_tree.insert(20)
    avl_tree.insert(5)
    avl_tree.insert(30)

    assert avl_tree.to_string() == "5,10,20,30"
    assert avl_tree.root.value == 10

    avl_tree.remove(5)

    assert avl_tree.to_string() == "10,20,30"
    assert avl_tree.root.value == 20
    assert avl_tree.root.left is not None and avl_tree.root.left.value == 10
    assert avl_tree.root.right is not None and avl_tree.root.right.value == 30


def test_balance_after_remove():
    avl_tree = AvlTree[int]()

    avl_tree.insert(1)
    avl_tree.insert(2)
    avl_tree.insert(3)
    avl_tree.insert(4)
    avl_tree.insert(5)

    assert avl_tree.to_string() == "1,2,3,4,5"
    assert avl_tree.root.value == 2
    assert avl_tree.root.left is not None and avl_tree.root.left.value == 1
    assert avl_tree.root.right is not None and avl_tree.root.right.value == 4

    avl_tree.insert(6)
    #   complex left rotate

    assert avl_tree.to_string() == "1,2,3,4,5,6"
    assert avl_tree.root.value == 4
    assert avl_tree.root.left is not None and avl_tree.root.left.value == 2
    assert avl_tree.root.right is not None and avl_tree.root.right.value == 5

    avl_tree.insert(7)
    #   left rotate on node with value 5

    assert avl_tree.to_string() == "1,2,3,4,5,6,7"
    assert avl_tree.root.value == 4
    assert avl_tree.root.left is not None and avl_tree.root.left.value == 2
    assert avl_tree.root.right is not None and avl_tree.root.right.value == 6

    avl_tree.insert(8)
    #   balanced on all nodes
    assert avl_tree.to_string() == "1,2,3,4,5,6,7,8"

    avl_tree.insert(9)
    #   left rotate on node with value 7
    assert avl_tree.to_string() == "1,2,3,4,5,6,7,8,9"
    assert avl_tree.root.value == 4
    assert avl_tree.root.left is not None and avl_tree.root.left.value == 2
    assert avl_tree.root.right is not None and avl_tree.root.right.value == 6
    assert (
        avl_tree.root.right is not None
        and avl_tree.root.right.right is not None
        and avl_tree.root.right.right.value == 8
    )

    avl_tree.remove(8)
    assert avl_tree.to_string() == "1,2,3,4,5,6,7,9"

    avl_tree.remove(9)
    assert avl_tree.to_string() == "1,2,3,4,5,6,7"
    assert avl_tree.root.value == 4
    assert avl_tree.root.height == 2
    assert avl_tree.root.balance_factor == 0
