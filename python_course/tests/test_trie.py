import pytest
from python_course.data_structures.trie import Trie


@pytest.fixture
def empty_trie():
    return Trie("*")


@pytest.fixture
def populated_trie(empty_trie, request):
    """Fixture to populate the trie with words before each test."""
    words = request.param
    for word in words:
        empty_trie.add_word(word)
    return empty_trie


def test_create(empty_trie):
    assert empty_trie is not None
    assert empty_trie.root.value == "*"
    assert empty_trie.is_empty()
    assert str(empty_trie) == "*"


def test_add_words(empty_trie):
    empty_trie.add_word("cat")

    assert not empty_trie.is_empty()
    assert str(empty_trie.root) == "*:c"
    assert str(empty_trie.root.get_child("c")) == "c:a"

    empty_trie.add_word("car")
    assert str(empty_trie.root) == "*:c"
    assert str(empty_trie.root.get_child("c")) == "c:a"
    assert str(empty_trie.root.get_child("c").get_child("a")) == "a:r,t"
    assert str(empty_trie.root.get_child("c").get_child("a").get_child("r")) == "r*"


@pytest.mark.parametrize(
    "words, search_words, expected_results",
    [
        (
            ["cat", "cats", "carpet", "caption"],
            ["cat", "cats", "dog"],
            [True, True, False],
        ),
        (
            ["apple", "applesauce"],
            ["apple", "apples", "applesauce"],
            [True, False, True],
        ),
    ],
)
def test_does_word_exist(empty_trie, words, search_words, expected_results):
    for word in words:
        empty_trie.add_word(word)

    assert [
        empty_trie.does_word_exist(word) for word in search_words
    ] == expected_results


@pytest.mark.parametrize(
    "populated_trie, search_chars, expected_results",
    [
        (
            ["cat", "cats", "carpet", "caption"],  # Words inserted via fixture
            ["ca", "cat", "cab"],  # Prefixes to search
            [
                ["p", "r", "t"],  # Expected suggestions for "ca"
                ["s"],  # Expected suggestions for "cat"
                [],  # Expected suggestions for "cab"
            ],
        )
    ],
    indirect=["populated_trie"],  # Tells pytest to use the fixture
)
def test_suggest_next_characters(populated_trie, search_chars, expected_results):
    assert [
        populated_trie.suggest_next_characters(chars) for chars in search_chars
    ] == expected_results


@pytest.mark.parametrize(
    "populated_trie, words_to_delete, expected_results",
    [
        (
            ["cat", "car", "carpet", "cart"],  # Words to insert initially
            ["carpool", "carpet", "cat", "car", "cart"],  # Words deleted one by one
            [
                {
                    "carpool": False,
                    "cat": True,
                    "car": True,
                    "carpet": True,
                    "cart": True,
                },  # After trying to delete "carpool" (not in Trie)
                {
                    "carpool": False,
                    "cat": True,
                    "car": True,
                    "carpet": False,
                    "cart": True,
                },  # After deleting "carpet"
                {
                    "carpool": False,
                    "cat": False,
                    "car": True,
                    "carpet": False,
                    "cart": True,
                },  # After deleting "cat"
                {
                    "carpool": False,
                    "cat": False,
                    "car": False,
                    "carpet": False,
                    "cart": True,
                },  # After deleting "car"
                {
                    "carpool": False,
                    "cat": False,
                    "car": False,
                    "carpet": False,
                    "cart": False,
                },  # After deleting "cart"
            ],
        )
    ],
    indirect=["populated_trie"],  # Tells pytest to use the fixture
)
def test_delete_word(populated_trie, words_to_delete, expected_results):
    """Delete words one at a time and check remaining words in Trie without order dependency."""
    print("populated_trie", populated_trie)

    # Step-by-step deletion
    for i, word_to_delete in enumerate(words_to_delete):

        populated_trie.delete_word(word_to_delete)

        assert {
            word: populated_trie.does_word_exist(word) for word in words_to_delete
        } == expected_results[i]
