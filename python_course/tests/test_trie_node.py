import pytest
from python_course.data_structures.trie import TrieNode


@pytest.fixture
def default_trie_node():
    return TrieNode("c", True)


@pytest.fixture
def trie_node(request):
    char, is_complete = request.param
    return TrieNode(char, is_complete)


@pytest.fixture
def trie_node_with_children():
    """Fixture that returns a TrieNode with pre-added children: a, o."""
    node = TrieNode("c")
    node.add_child("a")
    node.add_child("o")
    return node


@pytest.mark.parametrize(
    "trie_node, expected_str",
    [
        (("c", True), "c*"),
        (("x", False), "x*"),
    ],
    indirect=["trie_node"],
)
def test_create(trie_node, expected_str):
    assert str(trie_node) == expected_str


@pytest.mark.parametrize(
    "children, expected_str",
    [
        (["a"], "c:a"),
        (["a", "t"], "c:a,t"),
        (["x", "y", "z"], "c:x,y,z"),
    ],
)
def test_add_child(default_trie_node, children, expected_str):
    for char in children:
        default_trie_node.add_child(char)

    assert str(default_trie_node) == expected_str


@pytest.mark.parametrize(
    "char, expected_str",
    [
        ("a", "a*"),
        ("o", "o*"),
        ("b", None),
    ],
)
def test_get_child(trie_node_with_children, char, expected_str):
    child_node = trie_node_with_children.get_child(char)

    if expected_str:
        assert child_node is not None
        assert str(child_node) == expected_str
        assert child_node.value == char
    else:
        assert child_node is None  # For the "b" case


def test_has_children_false(
    default_trie_node,
):
    assert not default_trie_node.has_children()


def test_has_children_true(trie_node_with_children):
    assert trie_node_with_children.has_children()


@pytest.mark.parametrize(
    "char, expected_str",
    [
        ("a", True),
        ("o", True),
        ("b", False),
    ],
)
def test_has_specific_child(trie_node_with_children, char, expected_str):
    assert trie_node_with_children.has_child(char) == expected_str
