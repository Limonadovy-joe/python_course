import pytest

from python_course.data_structures.stack import Stack


@pytest.fixture
def stack():
    return Stack()


def test_create_empty_stack(stack):
    assert stack is not None


@pytest.mark.parametrize(
    "values, expected_string",
    [
        ([1, 2], "2,1"),
        # ([5, 10, 15], "15,10,5"),
    ],
)
def test_stack_data(stack, values, expected_string):
    for value in values:
        stack.push(value)
    assert str(stack) == expected_string


def test_peek_data(stack):
    assert stack.peek() is None

    stack.push(1)
    stack.push(2)

    assert stack.peek() == 2
    assert stack.peek() == 2  # Ensure it remains the same


def test_check_if_stack_is_empty(stack):
    assert stack.is_empty() is True

    stack.push(1)

    assert stack.is_empty() is False


@pytest.mark.parametrize(
    "values, expected_popped, expected_empty",
    [
        ([1, 2], [2, 1, None], True),
        ([5, 10, 15], [15, 10, 5, None], True),
    ],
)
def test_pop_data(stack, values, expected_popped, expected_empty):
    for value in values:
        stack.push(value)

    for expected in expected_popped:
        assert stack.pop() == expected

    assert stack.is_empty() == expected_empty


@pytest.mark.parametrize(
    "values, expected_array",
    [
        ([1, 2, 3], [3, 2, 1]),
        ([10, 20, 30, 40], [40, 30, 20, 10]),
    ],
)
def test_stack_to_array(stack, values, expected_array):
    assert stack.peek() is None

    for value in values:
        stack.push(value)

    assert stack.to_array() == expected_array
