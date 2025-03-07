from typing import Generic, TypeVar, List, Optional, Generator, Tuple


T = TypeVar("T", bound=str)

ALPHABET_SIZE = 26


class TrieNode(Generic[T]):

    def __init__(self, value: T, is_complete: bool = False):
        self.value = value
        self.is_complete = is_complete
        self.children: List[Optional[TrieNode[T]]] = [None] * ALPHABET_SIZE

    def __eq__(self, other):
        if not isinstance(other, TrieNode):
            return False
        return self.value == other.value

    def __repr__(self):
        return f"TrieNode({self.value}, children={self.children})"

    def has_child(self, child: T) -> bool:
        return self.children[self.char_to_index(child)] is not None

    def get_nodes(self) -> List["TrieNode[T]"]:
        return [node for node in self.children if node is not None]

    def has_children(self) -> bool:
        return len(self.get_nodes()) > 0

    def char_to_index(self, char: T) -> int:
        if not char:
            raise ValueError("Input character cannot be empty.")

        char_lowercased = char.lower()
        FST_CHAR_POS = 97
        return ord(char_lowercased) - FST_CHAR_POS

    def add_child(self, char: T, is_complete: bool = False) -> None:
        lower_case_char = char.lower()
        position = self.char_to_index(lower_case_char)

        if self.children[position] is None:
            self.children[position] = TrieNode(lower_case_char, is_complete)

    def get_child(self, char: T) -> Optional["TrieNode[T]"]:
        index = self.char_to_index(char)
        return self.children[index]

    def __str__(self):
        string = f"{self.value}"
        nodes = self.get_nodes()
        length = len(nodes)

        if length > 0:
            string = string + ":"
            nodes_names = [
                (f"{node.value}," if i != length - 1 else f"{node.value}")
                for i, node in enumerate(nodes)
            ]
            string = "".join([string] + nodes_names)
        else:
            if not string.startswith("*"):
                string = string + "*"

        print()
        return string


class CharInfo:
    def __init__(
        self, index: int, char: str, position: int, is_last_char: bool = False
    ):
        self.index = index
        self.char = char
        self.position = position
        self.is_last_char = is_last_char

    def __repr__(self):
        return f"CharInfo(index={self.index}, char={self.char}, position={self.position}, ,is_last_char={self.is_last_char})"


class Trie(Generic[T]):

    def __init__(self, head_character: str = "*"):
        self.root: Optional[TrieNode[T]] = TrieNode(head_character)

    def __str__(self):
        return str(self.root)

    def char_to_index(self, char: str) -> int:
        if not char:
            raise ValueError("Input character cannot be empty.")

        char_lowercased = char.lower()
        FST_CHAR_POS = 97
        return ord(char_lowercased) - FST_CHAR_POS

    def index_to_char(self, index: int) -> str:
        FST_CHAR_POS = 97
        return chr(FST_CHAR_POS + index)

    def to_lower_case(self, word: str) -> str:
        return word.lower()

    def yield_chars(self, word: str) -> Generator[CharInfo, None, None]:
        lower_case_word = self.to_lower_case(word)
        last_index = len(lower_case_word) - 1
        for index, char in enumerate(lower_case_word):
            is_last_char = index == last_index
            position = self.char_to_index(char)
            yield CharInfo(index, char, position, is_last_char)

    #   TODO
    #   make recursive call
    def add_word(self, word: T) -> None:
        if not word:
            return None

        current_node = self.root
        for char_info in self.yield_chars(word):
            position = char_info.position

            if current_node.children[position] is None:
                current_node.children[position] = TrieNode(
                    char_info.char, char_info.is_last_char
                )
            elif char_info.is_last_char:
                node = current_node.children[position]
                if node is not None:
                    node.is_complete = True

            current_node = current_node.children[position]

    def is_empty(self) -> bool:
        return not any(self.root.children)

    def does_word_exist(self, word: str) -> bool:
        if self.is_empty() or not word:
            return False

        node = self.root
        for char_info in self.yield_chars(word):
            position = char_info.position
            node = node.children[position]

            if node is None or (char_info.is_last_char and not node.is_complete):
                return False

        return True

    def __delete_word(
        self, word: str, prev_node: Optional[TrieNode[T]] = None
    ) -> Optional[Tuple[TrieNode[T], int]]:
        if self.is_empty() or not word:
            return None

        if prev_node is None:
            tuple = self.__delete_word(word, self.root)

            if tuple is not None:
                _, pos = tuple
                self.root.children[pos] = None
                return None

        char = word[0]
        rest = word[1:]
        position = self.char_to_index(char)
        current_node = prev_node.children[position] if prev_node is not None else None

        if current_node is None:
            return None

        if rest == "":

            return (current_node, position)

        tuple = self.__delete_word(rest, current_node)

        # Early exit
        if tuple is not None:
            node, pos = tuple

            if node.has_children():
                node.is_complete = False
                #   just remove flag
                #   do not have to traverse to next nodes
                return None

            if len(current_node.get_nodes()) > 1 or current_node.is_complete:
                current_node.children[pos] = None
                return None

            current_node.children[pos] = None

            return (current_node, position)

    def delete_word(self, word: str) -> bool:
        return self.__delete_word(word)

    def suggest_next_characters(self, chars: str) -> List[str]:
        if self.is_empty() or not chars:
            return []

        node = self.root
        for char_info in self.yield_chars(chars):
            node = node.children[char_info.position]

            if node is None:
                return []

            if char_info.is_last_char:
                return [node.value for node in node.get_nodes()]
