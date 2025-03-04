from typing import Generic, TypeVar, Tuple, Optional, List, Dict

from itertools import chain

from python_course.data_structures.linked_list import LinkedList


K = TypeVar("K")
V = TypeVar("V")


class HashTable(Generic[K, V]):

    def __init__(self, size: int = 32):
        self.size = size
        self.buckets = [LinkedList[Tuple[K, V]]() for _ in range(0, size)]
        self.__keys = {}

    def __str__(self):
        for i in range(self.size):
            print("-----")
            print(f"node - {i}", self.buckets[i])
            print("-----")

        return str(self.__dict__)

    def hash(self, key: str) -> int:
        hashes = 0
        for i in range(len(key)):
            hashes = hashes + ord(key[i])

        return hashes % self.size

    def set(self, key: K, value: V) -> None:
        self.__keys[key] = key

        index = self.hash(key)
        bucket = self.buckets[index]
        key_value = (key, value)

        was_find = False
        current_node = bucket.head

        while current_node is not None and not was_find:
            key_value_to_find: Tuple[K, V] = current_node.value
            key_to_find = key_value_to_find[0]

            if key == key_to_find:
                del key_value_to_find
                current_node.value = key_value
                was_find = True

            current_node = current_node.next

        if not was_find:
            bucket.append(key_value)

    def delete(self, key: K) -> None:

        index = self.hash(key)
        bucket = self.buckets[index]

        if bucket.is_empty():
            return None

        current_node = bucket.head
        prev_node = None

        while current_node is not None:
            next_node = current_node.next

            key_value_to_find: Tuple[K, V] = current_node.value
            key_to_find = key_value_to_find[0]

            if key == key_to_find:
                current_node.next = None
                del current_node

                if prev_node is not None:
                    prev_node.next = None

                    if next_node is not None:
                        prev_node.next = next_node
                else:
                    # head = tail
                    if next_node is not None:
                        bucket.head = next_node

                        if next_node.next is None:
                            bucket.tail = bucket.head
                    else:
                        bucket.head = None
                        bucket.tail = bucket.head

                if bucket.length > 0:
                    bucket.length = bucket.length - 1

                return None

            prev_node = current_node
            current_node = next_node

    def get(self, key: K) -> Optional[V]:
        index = self.hash(key)
        bucket = self.buckets[index]

        if bucket.is_empty():
            return None

        current_node = bucket.head
        value: Optional[V] = None

        while current_node is not None:
            key_value_to_find: Tuple[K, V] = current_node.value
            key_to_find = key_value_to_find[0]

            if key == key_to_find:
                value = key_value_to_find[1]
                return value

            current_node = current_node.next

        return value

    def has(self, key: K) -> bool:
        return self.get(key) is not None

    def get_keys_values(self) -> Dict[K, List[V]]:
        keys_values = {}

        for index in range(0, self.size):
            ll = self.buckets[index]
            node = ll.head

            while node is not None:
                key, value = node.value

                if keys_values.get(key) is None:
                    keys_values[key] = []

                keys_values[key].append(value)
                node = node.next

        return keys_values

    def get_keys(self) -> List[K]:
        return list(chain.from_iterable(self.get_keys_values().keys()))

    def get_values(self) -> List[K]:
        return list(chain.from_iterable(self.get_keys_values().values()))
