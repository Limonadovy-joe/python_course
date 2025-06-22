from typing import Generic, TypeVar, Optional, Dict, List


T = TypeVar("T")


class Array(Generic[T]):
    def __init__(self, items: Optional[List[T]] = None):
        self.items: Dict[int, T] = (
            {index: value for index, value in enumerate(items)} if items else {}
        )
        self.length = len(self.items)

    def __str__(self):
        print(list(self.items.values()))
        return str(self.__dict__.values())

    def __increment(self, count: int = 1) -> None:
        self.length = self.length + count

    def __decrement(self, count) -> None:
        if self.length > 0:
            self.length = self.length - count

    # TODO
    # make standalone helper
    def __normalize_index(self, index: int) -> int:
        return int(abs(index))

    def push(self, item: T):
        self.items[self.length] = item
        self.__increment()
        return self

    def insert(self, index: int, item: T):
        new_index = self.__normalize_index(index)

        if new_index >= self.length:
            self.push(item)
        else:
            updated_items = {}
            updated_items[new_index] = item

            for index, value in self.items.items():
                if index < new_index:
                    updated_items[index] = value
                elif index >= new_index:
                    updated_items[index + 1] = value

            self.items = updated_items
            self.__increment()
        return self

    #   TODO
    #   Refactor
    #   Filter insert
    def __remove_item(self, index: int) -> None:
        filtered_entries = list(
            filter(lambda pair: pair[0] != index, list(self.items.items()))
        )

        entries = list(
            map(
                lambda pair: (
                    (pair[0] - 1, pair[1])
                    if pair[0] != index and pair[0] != 0
                    else pair
                ),
                filtered_entries,
            )
        )
        copy_items = dict(entries)
        self.items = copy_items

        self.__decrement(1)

    def pop(self):
        if self.length == 0:
            return None
        index = self.length - 1
        item = self.get(index)
        self.__remove_item(index)
        return item

    def delete(self, index: int):
        norm_index = self.__normalize_index(index)
        self.__remove_item(norm_index)
        return self

    def get(self, index: int):
        norm_index = self.__normalize_index(index)
        if norm_index > self.length - 1:
            return None
        return self.items[norm_index]


array = Array([1, 2, 3, 4]).pop()
print("array", array)
