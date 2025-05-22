import pytest

from typing import List, TypeVar

from python_course.data_structures.binary_search_tree import BinarySearchTree

T = TypeVar("T")


def get_string(values: List[T]):
    return ",".join(str(x) for x in values)


@pytest.fixture
def empty_bst():
    return BinarySearchTree()


@pytest.fixture
def bst_with_values(request):
    bst = BinarySearchTree()
    for v in request.param:
        bst.insert(v)
    return bst


def test_create(empty_bst):
    bst = empty_bst

    assert bst is not None
    assert bst.root is not None
    assert bst.root.value is None
    assert bst.root.left is None
    assert bst.root.right is None


@pytest.mark.parametrize(
    "bst_with_values, values_to_insert, expected_str, expected_inserted_values",
    [
        ([], [10, 20, 5], "5,10,20", [10, 20]),
        ([7], [3, 9], "3,7,9", [3, 9]),
        ([15, 10], [5], "5,10,15", [5]),
    ],
    indirect=["bst_with_values"],
)
def test_insert(
    bst_with_values, values_to_insert, expected_str, expected_inserted_values
):
    bst = bst_with_values

    inserted_nodes = []
    for v in values_to_insert:
        inserted_nodes.append(bst.insert(v))

    assert bst.to_string() == expected_str
    for node, value in zip(inserted_nodes, expected_inserted_values):
        assert node.value == value


def test_insert_raises_error_when_duplicate_value_inserted(empty_bst):

    bst = empty_bst
    bst.insert(10)

    with pytest.raises(
        RuntimeError,
        match=f"Value '{10}' already exists in the binary search tree and cannot be inserted again.",
    ):
        bst.insert(10)


@pytest.mark.parametrize(
    "bst_with_values, expected_str, values_to_find, expected_values",
    [
        ([10, 20, 5], "5,10,20", [10, 20], [10, 20]),
        ([7, 3, 9, 1], "1,3,7,9", [7, 9], [7, 9]),
        ([15, 10], "10,15", [15, 10], [15, 10]),
    ],
    indirect=["bst_with_values"],
)
def test_find(bst_with_values, expected_str, values_to_find, expected_values):
    bst = bst_with_values

    assert bst.to_string() == expected_str

    found_values = []
    for v in values_to_find:
        node = bst.find(v)
        assert node is not None
        found_values.append(node.value)

    assert found_values == expected_values


def test_find_raises_error_when_value_not_found(empty_bst):
    empty_bst.insert(10)

    with pytest.raises(
        RuntimeError, match="Value '100' was not found in the binary search tree."
    ):
        empty_bst.find(100)


@pytest.mark.parametrize(
    "bst_with_values, value_to_remove, expected_str, expected_return",
    [
        ([10, 20, 5], 10, "5,20", True),
        ([7, 3, 9, 1], 3, "1,7,9", True),
        ([15, 10], 10, "15", True),
        ([15], 100, "15", False),
    ],
    indirect=["bst_with_values"],
)
def test_remove(bst_with_values, value_to_remove, expected_str, expected_return):
    bst = bst_with_values
    result = bst.remove(value_to_remove)
    assert result == expected_return
    assert bst.to_string() == expected_str


def test_traversed_to_sorted_array():
    bst = BinarySearchTree()

    bst.insert(10)
    bst.insert(-10)
    bst.insert(20)
    bst.insert(-20)
    bst.insert(25)
    bst.insert(6)

    result = ",".join(str(x) for x in bst.in_order_traversal())
    assert result == "-20,-10,6,10,20,25"


def test_traversed_to_sorted_array_reversed():
    bst = BinarySearchTree()

    bst.insert(10)
    bst.insert(-10)
    bst.insert(20)
    bst.insert(-20)
    bst.insert(25)
    bst.insert(6)

    result = get_string(bst.in_order_traversal(reverse=True))
    assert result == "25,20,10,6,-10,-20"


def test_inorder_traversal_using_stack():
    bst = BinarySearchTree()

    bst.insert(1)
    bst.insert(-2)
    bst.insert(3)
    bst.insert(-4)
    bst.insert(5)

    result = get_string(bst.in_order_traversal_using_stack())
    assert result == "-4,-2,1,3,5"
