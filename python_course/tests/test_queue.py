import pytest

from python_course.data_structures.queue import Queue


@pytest.fixture
def queue():
    """Fixture to create a new queue for each test."""
    return Queue()


def test_create_empty_queue(queue):
    assert queue is not None


@pytest.mark.parametrize(
    "values, expected",
    [
        ([1, 2], "1,2"),  # Enqueue integers
    ],
)
def test_enqueue_data(queue, values, expected):
    for value in values:
        queue.enqueue(value)
    assert str(queue) == expected


def test_enqueue_dequeue_objects(queue):
    queue.enqueue({"value": "test1", "key": "key1"})
    queue.enqueue({"value": "test2", "key": "key2"})

    assert queue.dequeue()["value"] == "test1"
    assert queue.dequeue()["value"] == "test2"


def test_peek_data(queue):
    assert queue.peek() is None

    queue.enqueue(1)
    queue.enqueue(2)

    assert queue.peek() == 1
    assert queue.peek() == 1  # Should still be 1


def test_check_if_queue_is_empty(queue):
    assert queue.is_empty() is True

    queue.enqueue(1)

    assert queue.is_empty() is False


def test_dequeue_fifo_order(queue):
    queue.enqueue(1)
    queue.enqueue(2)

    assert queue.dequeue() == 1
    assert queue.dequeue() == 2
    assert queue.dequeue() is None
    assert queue.is_empty() is True
