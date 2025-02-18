import pytest
from python_course.data_structures.max_heap import MaxHeap, HeapNode


custom_comparator = lambda x, y: -1 if x < y else 1 if x > y else 0


@pytest.fixture
def max_heap():
    """Fixture to create a max_heap instance with a custom comparator."""
    return MaxHeap[int](custom_comparator)


def test_initialization_with_custom_comparator(max_heap: MaxHeap[int]):
    """Test that a max_heap initializes correctly with a custom comparator."""
    assert max_heap.is_empty()
    assert max_heap.root is None
    assert max_heap.compare is custom_comparator


def test_add_and_heapify_up(max_heap: MaxHeap[int]):
    """Test that inserting elements and maintains heap order by heapifying up."""
    max_heap.add(5)

    assert max_heap.root.value == 5
    assert max_heap.root.parent is None
    assert max_heap.root.left is None
    assert max_heap.root.right is None
    assert not max_heap.is_empty()

    max_heap.add(3)
    assert max_heap.root.value == 5
    assert max_heap.root.left.value == 3
    assert max_heap.root.left.parent.value == 5
    assert max_heap.root.right is None

    max_heap.add(10)
    assert max_heap.root.value == 10
    max_heap.add(1)
    assert max_heap.root.value == 10
    max_heap.add(1)
    assert max_heap.root.value == 10

    assert str(max_heap) == "10,3,5,1,1"


def test_poll_and_heapify_down(max_heap: MaxHeap[int]):
    """Test that polling elements and maintains heap order by heapifying down."""
    max_heap.add(5)
    max_heap.add(3)
    max_heap.add(10)
    max_heap.add(11)
    max_heap.add(1)

    assert str(max_heap) == "11,10,5,3,1"

    assert max_heap.poll() == 11
    assert str(max_heap) == "10,3,5,1"

    assert max_heap.poll() == 10
    assert str(max_heap) == "5,3,1"

    assert max_heap.poll() == 5
    assert str(max_heap) == "3,1"

    assert max_heap.poll() == 3
    assert str(max_heap) == "1"

    assert max_heap.poll() == 1
    assert str(max_heap) == ""

    assert max_heap.poll() is None
    assert str(max_heap) == ""


def test_delete_and_heapify_down(max_heap: MaxHeap[int]):
    """Test that delete elements and maintains heap order by heapifying down."""
    max_heap.add(3)
    max_heap.add(12)
    max_heap.add(10)
    max_heap.add(11)
    max_heap.add(11)

    assert str(max_heap) == "12,11,10,3,11"

    max_heap.delete(12)
    assert str(max_heap) == "11,11,10,3"

    max_heap.delete(11)
    assert str(max_heap) == "10,3"

    max_heap.delete(11)
    assert str(max_heap) == "10,3"

    max_heap.delete(10)
    assert str(max_heap) == "3"
    assert max_heap.root.left is None
    assert max_heap.root.right is None


def test_delete_and_heapify_up(max_heap: MaxHeap[int]):
    """Test that delete elements and maintains heap order by heapifying up."""
    max_heap.add(3)
    max_heap.add(10)
    max_heap.add(5)
    max_heap.add(6)
    max_heap.add(7)
    max_heap.add(4)
    max_heap.add(6)
    max_heap.add(8)
    max_heap.add(2)
    max_heap.add(1)

    assert str(max_heap) == "10,8,6,7,6,4,5,3,2,1"

    max_heap.delete(4)
    assert str(max_heap) == "10,8,6,7,6,1,5,3,2"

    # delete element 3
    max_heap.delete(3)
    assert str(max_heap) == "10,8,6,7,6,1,5,2"

    # delete element 5
    max_heap.delete(5)
    assert str(max_heap) == "10,8,6,7,6,1,2"

    # delete element 10
    max_heap.delete(10)
    assert str(max_heap) == "8,7,6,2,6,1"

    # delete element 6
    max_heap.delete(6)
    assert str(max_heap) == "8,7,1,2"

    # delete element 2
    max_heap.delete(2)
    assert str(max_heap) == "8,7,1"

    # delete element 1
    max_heap.delete(1)
    assert str(max_heap) == "8,7"

    # delete element 7
    max_heap.delete(7)
    assert str(max_heap) == "8"

    # delete element 8 (last element)
    max_heap.delete(8)
    assert str(max_heap) == ""


def test_find_item_position(max_heap: MaxHeap[int]):
    """Verify that elements are positioned correctly, following an array-based heap structure."""
    max_heap.add(3)
    max_heap.add(12)
    max_heap.add(10)
    max_heap.add(11)
    max_heap.add(11)

    assert max_heap.find_position(3) == [(HeapNode(3), 3)]
    assert max_heap.find_position(33) == []
    assert max_heap.find_position(12) == [(HeapNode(12), 0)]
    assert max_heap.find_position(11) == [(HeapNode(11), 1), (HeapNode(11), 4)]
