from enum import Enum

from typing import Tuple, List

import pytest

from python_course.data_structures.min_heap import MinHeap


class Operations(Enum):
    PEEK = "PEEK"
    POLL = "POLL"


@pytest.fixture
def empty_min_heap():
    return MinHeap()


@pytest.fixture
def populated_min_heap(empty_min_heap, request):
    items = request.param
    for item in items:
        empty_min_heap.add(item)
    return empty_min_heap


@pytest.fixture
def populated_min_heap_with_history(empty_min_heap, request) -> Tuple[MinHeap, List]:
    """Fixture that populates MinHeap, tracks its state, and applies an operation ('peek' or 'poll')."""
    operation: Operations
    items, operation = request.param
    history = []

    if operation == Operations.PEEK:
        for item in items:
            empty_min_heap.add(item)
            result_operation = empty_min_heap.peek()
            history.append((result_operation, str(empty_min_heap.container)))
    elif operation == Operations.POLL:
        for item in items:
            empty_min_heap.add(item)

        while len(empty_min_heap.container) > 0:
            result_operation = empty_min_heap.poll()
            history.append((result_operation, str(empty_min_heap.container)))

    else:
        raise ValueError("Invalid operation: choose 'peek' or 'poll'.")

    return empty_min_heap, history


def test_create(empty_min_heap):
    assert empty_min_heap is not None
    assert empty_min_heap.is_empty()
    assert empty_min_heap.peek() is None


@pytest.mark.parametrize(
    "populated_min_heap_with_history,  expected_peek_and_heap_structure",
    [
        (
            ([5, 3, 10, 1, 1], Operations.PEEK),
            [
                (5, "[5]"),
                (3, "[3, 5]"),
                (3, "[3, 5, 10]"),
                (1, "[1, 3, 10, 5]"),
                (1, "[1, 1, 10, 5, 3]"),
            ],  # Expected results
        ),
    ],
    indirect=[
        "populated_min_heap_with_history"
    ],  # Use the fixture for parameterization
)
def test_add_and_heapify_up(
    populated_min_heap_with_history, expected_peek_and_heap_structure
):
    _, results = populated_min_heap_with_history
    assert results == expected_peek_and_heap_structure


@pytest.mark.parametrize(
    "populated_min_heap_with_history,  expected_peek_and_heap_structure",
    [
        (
            ([5, 3, 10, 11, 1], Operations.POLL),
            [
                (1, "[3, 5, 10, 11]"),
                (3, "[5, 11, 10]"),
                (5, "[10, 11]"),
                (10, "[11]"),
                (11, "[]"),
            ],  # Expected results
        ),
    ],
    indirect=[
        "populated_min_heap_with_history"
    ],  # Use the fixture for parameterization
)
def test_poll_and_heapify_down(
    populated_min_heap_with_history, expected_peek_and_heap_structure
):
    _, results = populated_min_heap_with_history
    assert results == expected_peek_and_heap_structure


@pytest.mark.parametrize(
    "populated_min_heap",
    [
        ([3, 12, 10]),
    ],
    indirect=["populated_min_heap"],  # Use the fixture for parameterization
)
def test_heapify_down_right_branch(populated_min_heap):
    assert str(populated_min_heap.container) == "[3, 12, 10]"

    populated_min_heap.add(11)
    assert str(populated_min_heap.container) == "[3, 11, 10, 12]"

    assert populated_min_heap.poll() == 3
    assert str(populated_min_heap.container) == "[10, 11, 12]"


@pytest.mark.parametrize(
    "populated_min_heap, expected_indicies",
    [
        ([3, 12, 10, 11, 11], [(5, []), (3, [0]), (11, [1, 4])]),
    ],
    indirect=["populated_min_heap"],  # Use the fixture for parameterization
)
def test_find_indicies(populated_min_heap, expected_indicies):
    assert str(populated_min_heap.container) == "[3, 11, 10, 12, 11]"

    assert [
        (value, populated_min_heap.find(value)) for value, expected in expected_indicies
    ] == expected_indicies


@pytest.mark.parametrize(
    "populated_min_heap, values_to_remove , expected_structure",
    [
        (
            [3, 12, 10, 11, 11],
            [3, 3, 11, 3],
            [
                "[10, 11, 11, 12]",
                "[10, 11, 11, 12]",
                "[10, 12]",
                "[10, 12]",
            ],
        ),
    ],
    indirect=["populated_min_heap"],  # Use the fixture for parameterization
)
def test_remove_heapify_down(populated_min_heap, values_to_remove, expected_structure):
    assert str(populated_min_heap.container) == "[3, 11, 10, 12, 11]"

    for value_to_remove, structure in zip(values_to_remove, expected_structure):
        populated_min_heap.remove(value_to_remove)
        assert str(populated_min_heap.container) == structure


@pytest.mark.parametrize(
    "populated_min_heap, values_to_remove , expected_structure",
    [
        (
            [3, 10, 5, 6, 7, 4, 6, 8, 2, 1],
            [8, 7, 1, 2, 6, 10, 5, 3, 4],
            [
                "[1, 2, 4, 6, 3, 5, 6, 10, 7]",
                "[1, 2, 4, 6, 3, 5, 6, 10]",
                "[2, 3, 4, 6, 10, 5, 6]",
                "[3, 6, 4, 6, 10, 5]",
                "[3, 5, 4, 10]",
                "[3, 5, 4]",
                "[3, 4]",
                "[4]",
                "[]",
            ],
        ),
    ],
    indirect=["populated_min_heap"],  # Use the fixture for parameterization
)
def test_remove_heapify_up(populated_min_heap, values_to_remove, expected_structure):
    assert str(populated_min_heap.container) == "[1, 2, 4, 6, 3, 5, 6, 10, 8, 7]"

    for value_to_remove, structure in zip(values_to_remove, expected_structure):
        populated_min_heap.remove(value_to_remove)

        assert str(populated_min_heap.container) == structure


@pytest.mark.parametrize(
    "populated_min_heap, values_to_remove , expected_structure",
    [
        (
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [2, 4],
            [
                "[1, 4, 3, 8, 5, 6, 7, 9]",
                "[1, 5, 3, 8, 9, 6, 7]",
            ],
        ),
    ],
    indirect=["populated_min_heap"],  # Use the fixture for parameterization
)
def test_remove_and_reorder_tree(
    populated_min_heap, values_to_remove, expected_structure
):
    assert str(populated_min_heap.container) == "[1, 2, 3, 4, 5, 6, 7, 8, 9]"

    for index, value_to_remove in enumerate(values_to_remove):
        populated_min_heap.remove(value_to_remove)

        assert str(populated_min_heap.container) == expected_structure[index]
