from typing import List, Tuple, TypeVar
from collections import Counter

import pytest

from python_course.data_structures.hash_table import HashTable
from python_course.data_structures.linked_list import LinkedList

DEFAULT_HASH_TABLE_SIZE = 32

K = TypeVar("K", str, int)
V = K = TypeVar("V")


def format_bucket(ll: LinkedList[Tuple[K, V]]) -> str:
    current_node = ll.head
    string = ""

    while current_node is not None:
        key, value = current_node.value

        if len(string) > 0:
            string = string + f",{key}:{value}"
        else:
            string = string + f"{key}:{value}"
        current_node = current_node.next

    return string


@pytest.fixture
def hash_table(request):
    size = request.param

    if isinstance(size, int):
        return HashTable(size)
    elif isinstance(size, list):
        value = size[0][0] if isinstance(size[0], tuple) else size[0]

        return HashTable(value)
    elif isinstance(size, tuple):
        return HashTable(size[0])  # Example usage

    print("size", size)
    return HashTable(size)


@pytest.fixture
def default_hash_table():
    return HashTable(DEFAULT_HASH_TABLE_SIZE)


@pytest.fixture
def populated_hash_table(hash_table, values: List[Tuple[K, V]]):
    for key, value in values:
        hash_table.set(key, value)
    return hash_table


@pytest.mark.parametrize(
    "hash_table, expected_buckets_length",
    [
        (64, 64),  # Test case 1
        (128, 128),  # Test case 2
    ],
    indirect=["hash_table"],
)
def test_create_by_size(hash_table, expected_buckets_length):
    assert len(hash_table.buckets) == expected_buckets_length


@pytest.mark.parametrize(
    "keys, expected_hashes",
    [
        (["a", "b", "abc"], [1, 2, 6]),  # Expected results
    ],
)
def test_generate_hash_by_key(default_hash_table, keys, expected_hashes):
    hashes = [default_hash_table.hash(key) for key in keys]
    assert hashes == expected_hashes


@pytest.mark.parametrize(
    "hash_table, values, expected_values",
    [
        (
            [(3)],  # Initial Buckets size
            [
                # Values to include in populated_hash_table
                ("a", "sky-old"),
                ("a", "sky"),
                ("b", "sea"),
                ("c", "earth"),
                ("d", "ocean"),
            ],
            # Expected results
            [("a", "sky"), ("b", "sea"), ("c", "earth"), ("d", "ocean"), ("z", None)],
        ),
    ],
    indirect=["hash_table"],
)
def test_set_and_retrieve_values(populated_hash_table, expected_values):
    values = [(key, populated_hash_table.get(key)) for key, _ in expected_values]
    assert values == expected_values


@pytest.mark.parametrize(
    "hash_table, values, expected_values",
    [
        (
            [(3)],  # Initial Buckets size
            [
                # Values to include in populated_hash_table
                ("a", "sky"),
                ("b", "sea"),
            ],
            # Expected results
            [("a", True), ("b", True), ("x", False)],
        ),
    ],
    indirect=["hash_table"],
)
def test_has_value(populated_hash_table, expected_values):
    values = [(key, populated_hash_table.has(key)) for key, _ in expected_values]
    assert values == expected_values


@pytest.mark.parametrize(
    "hash_table, values, expected_buckets_values",
    [
        (
            [(3)],  # Initial Buckets size
            [
                # Values to include in populated_hash_table
                # Values to include in populated_hash_table
                ("a", "sky-old"),
                ("a", "sky"),
                ("b", "sea"),
                ("c", "earth"),
                ("d", "ocean"),
            ],
            # Expected results
            [(0, "c:earth"), (1, "a:sky,d:ocean"), (2, "b:sea")],
        ),
    ],
    indirect=["hash_table"],
)
def test_store_values_with_collisions(populated_hash_table, expected_buckets_values):
    values = [
        (index, format_bucket(populated_hash_table.buckets[index]))
        for index, _ in expected_buckets_values
    ]
    assert values == expected_buckets_values


@pytest.mark.parametrize(
    "hash_table, values, keys_to_delete, expected_buckets_values",
    [
        (
            [(3)],  # Initial Buckets size
            [
                # Values to include in populated_hash_table
                ("a", "sky"),
                ("d", "ocean"),
            ],
            # Keys to delete
            ["a", "not-existing"],
            # Expected results
            [("a", None), ("d", "ocean"), ("not-existing", None)],
        ),
    ],
    indirect=["hash_table"],
)
def test_delete_values(populated_hash_table, keys_to_delete, expected_buckets_values):
    for key in keys_to_delete:
        populated_hash_table.delete(key)

    values = [
        (key, populated_hash_table.get(key)) for key, _ in expected_buckets_values
    ]
    assert values == expected_buckets_values


@pytest.mark.parametrize(
    "hash_table, values, expected_keys",
    [
        (
            [(3)],  # Initial Buckets size
            [
                # Values to include in populated_hash_table
                ("a", "sky-old"),
                ("a", "sky"),
                ("b", "sea"),
                ("c", "earth"),
                ("d", "ocean"),
            ],
            # Expected results
            ["a", "b", "c", "d"],
        ),
    ],
    indirect=["hash_table"],
)
def test_get_keys(populated_hash_table, expected_keys):
    assert Counter(populated_hash_table.get_keys()) == Counter(expected_keys)


@pytest.mark.parametrize(
    "hash_table, values, expected_values",
    [
        (
            [(3)],  # Initial Buckets size
            [
                # Values to include in populated_hash_table
                ("a", "sky-old"),
                ("a", "sky"),
                ("b", "sea"),
                ("c", "earth"),
                ("d", "ocean"),
            ],
            # Expected results
            ["sky", "sea", "earth", "ocean"],
        ),
    ],
    indirect=["hash_table"],
)
def test_get_values(populated_hash_table, expected_values):
    assert Counter(populated_hash_table.get_values()) == Counter(expected_values)
