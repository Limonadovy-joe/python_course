import pytest

from python_course.data_structures.doubly_linked_list import DoublyLinkedList


@pytest.fixture
def empty_doubly_linked_list():
    """Fixture that returns an empty doubly linked list and checks its initial state."""
    ll = DoublyLinkedList()
    assert ll.head is None
    assert ll.tail is None
    return ll


@pytest.fixture
def populated_doubly_linked_list(empty_doubly_linked_list, request):
    """Fixture that populates the linked list with given values."""
    values = request.param
    for value in values:
        empty_doubly_linked_list.append(value)
    return empty_doubly_linked_list


def test_create(empty_doubly_linked_list):
    assert str(empty_doubly_linked_list) == ""


@pytest.mark.parametrize(
    "populated_doubly_linked_list, expected_structure",
    [
        ([1, 2, 3], "1,2,3"),
    ],
    indirect=["populated_doubly_linked_list"],
)
def test_append(populated_doubly_linked_list, expected_structure):
    assert str(populated_doubly_linked_list) == expected_structure

    assert populated_doubly_linked_list.tail.next is None
    assert populated_doubly_linked_list.tail.previous.value == 2


@pytest.mark.parametrize(
    "values, expected_structure",
    [
        ([1, 2, 3], "3,2,1"),
    ],
)
def test_prepend(empty_doubly_linked_list, values, expected_structure):
    for value in values:
        empty_doubly_linked_list.prepend(value)
    assert str(empty_doubly_linked_list) == expected_structure

    assert (
        empty_doubly_linked_list.head.next.next.previous.value
        == empty_doubly_linked_list.head.next.value
    )
    assert (
        empty_doubly_linked_list.tail.previous.next.value
        == empty_doubly_linked_list.tail.value
    )


@pytest.mark.parametrize(
    "populated_doubly_linked_list, values_to_delete, expected_structure",
    [
        (
            [1, 1, 2, 3, 3, 3, 4, 5],
            [3, 3, 1, 5, 4, 2],
            ["1,1,2,4,5", "1,1,2,4,5", "2,4,5", "2,4", "2", ""],
        ),
    ],
    indirect=["populated_doubly_linked_list"],
)
def test_delete(populated_doubly_linked_list, values_to_delete, expected_structure):
    for value, exp_str in zip(values_to_delete, expected_structure):
        populated_doubly_linked_list.delete(value)
        assert str(populated_doubly_linked_list) == exp_str


@pytest.mark.parametrize(
    "populated_doubly_linked_list, deleted_tail_values, expected_structure",
    [
        (
            [1, 2, 3],  # Initial linked list
            [3, 2, 1],  # Expected deleted values
            [
                "1,2",  # After deleting 3
                "1",  # After deleting 2
                "",  # After deleting 1 (empty list)
            ],
        ),
    ],
    indirect=["populated_doubly_linked_list"],
)
def test_delete_tail(
    populated_doubly_linked_list, deleted_tail_values, expected_structure
):
    for deleted_value, exp_str in zip(deleted_tail_values, expected_structure):
        node = populated_doubly_linked_list.delete_tail()

        assert node.value == deleted_value  # Verify the correct node was deleted
        assert (
            str(populated_doubly_linked_list) == exp_str
        )  # Verify the structure is updated correctly


@pytest.mark.parametrize(
    "populated_doubly_linked_list, deleted_head_values, expected_structure",
    [
        (
            [1, 2, 3],  # Initial linked list
            [1, 2, 3],  # Expected deleted values
            [
                "2,3",  # After deleting 3
                "3",  # After deleting 2
                "",  # After deleting 1 (empty list)
            ],
        ),
    ],
    indirect=["populated_doubly_linked_list"],
)
def test_delete_head(
    populated_doubly_linked_list, deleted_head_values, expected_structure
):
    for deleted_value, exp_str in zip(deleted_head_values, expected_structure):
        node = populated_doubly_linked_list.delete_head()

        assert node.value == deleted_value  # Verify the correct node was deleted
        assert (
            str(populated_doubly_linked_list) == exp_str
        )  # Verify the structure is updated correctly


@pytest.mark.parametrize(
    "populated_doubly_linked_list, expected_structure",
    [
        (
            [1, 2, 3],  # Initial linked list
            "3,2,1",
        ),
    ],
    indirect=["populated_doubly_linked_list"],
)
def test_reverse(populated_doubly_linked_list, expected_structure):
    populated_doubly_linked_list.reverse()
    assert str(populated_doubly_linked_list) == expected_structure
