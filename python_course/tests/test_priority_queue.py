import pytest

from python_course.data_structures.priority_queue import PriorityQueue


@pytest.fixture
def empty_priority_queue():
    return PriorityQueue()


@pytest.fixture
def populated_priority_queue(empty_priority_queue, request):
    items = request.param
    for value, priority in items:
        empty_priority_queue.add(value, priority)
    return empty_priority_queue


@pytest.fixture
def priority_queue_with_changes(populated_priority_queue, priority_changes):
    for value, priority in priority_changes:
        populated_priority_queue.change_priority(value, priority)
    return populated_priority_queue


def test_create(empty_priority_queue):
    assert empty_priority_queue is not None
    assert empty_priority_queue.is_empty()
    assert empty_priority_queue.peek() is None


@pytest.mark.parametrize(
    "items,  expected_peek",
    [
        ([(10, 1), (5, 2), (100, 0)], [10, 10, 100]),  # Expected results
    ],
)
def test_add_and_peak(empty_priority_queue, items, expected_peek):
    for index, (value, priority) in enumerate(items):
        empty_priority_queue.add(value, priority)
        assert empty_priority_queue.peek() == expected_peek[index]


@pytest.mark.parametrize(
    "populated_priority_queue, expected_poll",
    [
        ([(10, 1), (5, 2), (100, 0), (200, 0)], [100, 200, 10, 5]),  # Expected results
    ],
    indirect=["populated_priority_queue"],
)
def test_poll(populated_priority_queue, expected_poll):
    assert [populated_priority_queue.poll() for _ in expected_poll] == expected_poll


@pytest.mark.parametrize(
    "populated_priority_queue, priority_changes, expected_poll_order",
    [
        (
            [(10, 1), (5, 2), (100, 0), (200, 0)],  # Initial heap state
            [(100, 10), (10, 20)],  # Change priorities (affecting head node first)
            [200, 5, 100, 10],  # Expected poll order after changes
        ),  # Expected results
    ],
    indirect=["populated_priority_queue"],
)
def test_change_priority_head_nodes_and_poll(
    priority_queue_with_changes, expected_poll_order
):
    """Test changing priorities of head nodes first"""
    assert [
        priority_queue_with_changes.poll() for _ in expected_poll_order
    ] == expected_poll_order


@pytest.mark.parametrize(
    "populated_priority_queue, priority_changes, expected_poll_order",
    [
        (
            [(10, 1), (5, 2), (100, 0), (200, 0)],  # Initial heap state
            [(200, 10), (10, 20)],  # Change priorities (affecting internal nodes)
            [100, 5, 200, 10],  # Expected poll order after changes
        ),  # Expected results
    ],
    indirect=["populated_priority_queue"],
)
def test_change_priority_internal_nodes_and_poll(
    priority_queue_with_changes, expected_poll_order
):
    """Test changing priorities of internal nodes"""
    assert [
        priority_queue_with_changes.poll() for _ in expected_poll_order
    ] == expected_poll_order


@pytest.mark.parametrize(
    "populated_priority_queue, priority_changes, values_to_add, expected_poll_order",
    [
        (
            [(10, 1), (5, 2), (100, 0), (200, 0)],  # Initial heap state
            [(200, 10), (10, 20)],  # Change priorities (affecting internal nodes)
            [(15, 15)],
            [100, 5, 200, 15, 10],  # Expected poll order after changes
        ),  # Expected results
    ],
    indirect=["populated_priority_queue"],
)
def test_change_priority_with_add(
    priority_queue_with_changes, values_to_add, expected_poll_order
):
    for value, priority in values_to_add:
        priority_queue_with_changes.add(value, priority)

    assert [
        priority_queue_with_changes.poll() for _ in expected_poll_order
    ] == expected_poll_order


@pytest.mark.parametrize(
    "populated_priority_queue, search_cases",
    [
        (
            [(10, 1), (5, 2), (100, 0), (200, 0), (15, 15)],  # Initial heap state
            [(70, False), (15, True)],
        ),  # Expected results
    ],
    indirect=["populated_priority_queue"],
)
def test_search(populated_priority_queue, search_cases):
    for value_to_find, expected_found in search_cases:
        assert populated_priority_queue.has_value(value_to_find) == expected_found
