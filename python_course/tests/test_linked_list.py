import pytest

from python_course.data_structures.linked_list import LinkedList


@pytest.fixture
def empty_linked_list():
    """Fixture that returns an empty linked list and checks its initial state."""
    ll = LinkedList()
    assert ll.head is None
    assert ll.tail is None
    return ll


@pytest.fixture
def populated_linked_list(empty_linked_list, request):
    """Fixture that populates the linked list with given values."""
    values = request.param
    for value in values:
        empty_linked_list.append(value)
    return empty_linked_list


def test_create(empty_linked_list):
    assert str(empty_linked_list) == ""


@pytest.mark.parametrize(
    "populated_linked_list, expected_structure",
    [
        ([1, 2, 3], "1,2,3"),
        (["a", "b", "c"], "a,b,c"),
    ],
    indirect=["populated_linked_list"],
)
def test_append(populated_linked_list, expected_structure):
    assert str(populated_linked_list) == expected_structure
    assert populated_linked_list.tail.next is None


@pytest.mark.parametrize(
    "values, expected_structure",
    [
        ([1, 2, 3], "3,2,1"),
    ],
)
def test_prepend(empty_linked_list, values, expected_structure):
    for value in values:
        empty_linked_list.prepend(value)
    assert str(empty_linked_list) == expected_structure


@pytest.mark.parametrize(
    "values, expected_structure",
    [
        ([(4, 3), (3, 2), (2, 1), (1, -7), (10, 9)], "1,4,2,3,10"),
    ],
)
def test_insert(empty_linked_list, values, expected_structure):
    for value, pos in values:
        empty_linked_list.insert(value, pos)
    assert str(empty_linked_list) == expected_structure


@pytest.mark.parametrize(
    "populated_linked_list, values_to_delete, expected_structure",
    [
        (
            [1, 1, 2, 3, 3, 3, 4, 5],
            [3, 3, 1, 5, 4, 2],
            ["1,1,2,4,5", "1,1,2,4,5", "2,4,5", "2,4", "2", ""],
        ),
    ],
    indirect=["populated_linked_list"],
)
def test_delete(populated_linked_list, values_to_delete, expected_structure):
    for value, exp_str in zip(values_to_delete, expected_structure):
        populated_linked_list.delete(value)
        assert str(populated_linked_list) == exp_str


@pytest.mark.parametrize(
    "populated_linked_list, deleted_tail_values, expected_structure",
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
    indirect=["populated_linked_list"],
)
def test_delete_tail(populated_linked_list, deleted_tail_values, expected_structure):
    for deleted_value, exp_str in zip(deleted_tail_values, expected_structure):
        node = populated_linked_list.delete_tail()

        assert node.value == deleted_value  # Verify the correct node was deleted
        assert (
            str(populated_linked_list) == exp_str
        )  # Verify the structure is updated correctly


@pytest.mark.parametrize(
    "populated_linked_list, deleted_head_values, expected_structure",
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
    indirect=["populated_linked_list"],
)
def test_delete_head(populated_linked_list, deleted_head_values, expected_structure):
    for deleted_value, exp_str in zip(deleted_head_values, expected_structure):
        node = populated_linked_list.delete_head()

        assert node.value == deleted_value  # Verify the correct node was deleted
        assert (
            str(populated_linked_list) == exp_str
        )  # Verify the structure is updated correctly


@pytest.mark.parametrize(
    "populated_linked_list, values_to_find, expected_values",
    [
        (
            [1, 2, 3],  # Initial linked list
            [5, 1, 2],
            [
                None,  # After finding 5
                1,
                2,
            ],
        ),
    ],
    indirect=["populated_linked_list"],
)
def test_find(populated_linked_list, values_to_find, expected_values):
    for value_to_find, exp_value in zip(values_to_find, expected_values):
        node = populated_linked_list.find(value_to_find)
        value = node.value if node is not None else None
        assert value == exp_value


@pytest.mark.parametrize(
    "populated_linked_list, callbacks, expected_values",
    [
        (
            [
                {"value": 1, "key": "key1"},
                {"value": 2, "key": "key2"},
                {"value": 3, "key": "key3"},
            ],  # Initial linked list
            [
                lambda obj: obj.get("key") == "key2",
                lambda obj: obj.get("value") == 4,
                lambda obj: obj.get("key") == "key3",
            ],
            [
                {"value": 2, "key": "key2"},
                None,
                {"value": 3, "key": "key3"},
            ],
        ),
    ],
    indirect=["populated_linked_list"],
)
def test_find_by_callback(populated_linked_list, callbacks, expected_values):
    for callback, exp_value in zip(callbacks, expected_values):
        node = populated_linked_list.find(callback)
        value = node.value if node else None
        assert value == exp_value


def test_find_by_compare_function():
    def comparator_function(a, b):
        if a["value"] == b["value"]:
            return 0
        return -1 if a["value"] < b["value"] else 1

    ll = LinkedList(comparator=comparator_function)
    for obj in [
        {"value": 1, "key": "key1"},
        {"value": 2, "key": "key2"},
        {"value": 3, "key": "key3"},
    ]:
        ll.append(obj)

    node3 = ll.find({"value": 3, "key": "key3"})

    assert node3 is not None
    assert node3.value == {"value": 3, "key": "key3"}

    node10 = ll.find({"value": 10, "key": "key10"})
    assert node10 is None


#   find preferring callback over compare function
def test_find_by_preffering_callback():
    def greater_than(current_value, value_to_find):
        return 0 if current_value > value_to_find else 1

    ll = LinkedList(comparator=greater_than)
    for i in [1, 2, 3, 4, 5]:
        ll.append(i)

    node = ll.find(3)
    assert node is not None
    assert node.value == 4

    node = ll.find(lambda x: x < 3)
    assert node is not None
    assert node.value == 1


@pytest.mark.parametrize(
    "populated_linked_list, expected_array",
    [
        (
            [1, 2, 3],  # Initial linked list
            [1, 2, 3],
        ),
    ],
    indirect=["populated_linked_list"],
)
def test_to_array(populated_linked_list, expected_array):
    assert populated_linked_list.to_array() == expected_array


@pytest.mark.parametrize(
    "populated_linked_list, expected_structure",
    [
        (
            [1, 2, 3],  # Initial linked list
            "3,2,1",
        ),
    ],
    indirect=["populated_linked_list"],
)
def test_reverse(populated_linked_list, expected_structure):
    populated_linked_list.reverse()
    assert str(populated_linked_list) == expected_structure


@pytest.mark.parametrize(
    "populated_linked_list, expected_structure",
    [
        (
            [1, 2, 3],  # Initial linked list
            [
                {"value": 1, "index": 0},
                {"value": 2, "index": 1},
                {"value": 3, "index": 2},
            ],
        ),
    ],
    indirect=["populated_linked_list"],
)
def test_traverse(populated_linked_list, expected_structure):
    assert [
        {"value": node.value, "index": node.index}
        for node in populated_linked_list.traverse()
    ] == expected_structure


@pytest.mark.parametrize(
    "populated_linked_list, expected_structure",
    [
        (
            [
                {"value": 1, "key": "key1"},
                {"value": 2, "key": "key2"},
            ],  # Initial linked list
            "{value:1,key:key1},{value:2,key:key2}",
        ),
    ],
    indirect=["populated_linked_list"],
)
def test_store_objects_and_to_string(populated_linked_list, expected_structure):
    assert populated_linked_list.to_string() == expected_structure
