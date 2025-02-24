from typing import Generic, TypeVar, List, Optional

from python_course.utils.ord import Ordering, CompareFunction

V = TypeVar("V")


class MinHeap(Generic[V]):

    def __init__(self, compare: Optional[CompareFunction[V]] = None):
        self.container: List[V] = []
        self.compare: CompareFunction[V] = (
            compare
            if compare is not None
            else lambda x, y: (-1 if x < y else 1 if x > y else 0)
        )

    def __str__(self):
        return str(self.__dict__)

    @property
    def length(self) -> int:
        return len(self.container)

    def is_empty(self) -> bool:
        return len(self.container) == 0

    def get_left_child_index(self, parent_index: int) -> int:
        return 2 * parent_index + 1

    def get_right_child_index(self, parent_index: int) -> int:
        return 2 * parent_index + 2

    def get_parent_index(self, child_index: int) -> int:
        if child_index == 0:
            return child_index
        return (child_index - 1) // 2

    def has_parent(self, child_index: int) -> int:
        return self.get_parent_index(child_index) >= 0

    def has_left_child(self, parent_index: int) -> int:
        return self.get_left_child_index(parent_index) < self.length

    def has_right_child(self, parent_index: int) -> int:
        return self.get_right_child_index(parent_index) < self.length

    def get_left_child(self, parent_index: int) -> int:
        index = self.get_left_child_index(parent_index)
        return self.container[index]

    def get_right_child(self, parent_index: int) -> int:
        index = self.get_right_child_index(parent_index)
        return self.container[index]

    def get_parent(self, child_index: int) -> int:
        index = self.get_parent_index(child_index)
        return self.container[index]

    def swap(self, index_fst: int, index_snd: int) -> None:
        tmp_fst = self.container[index_fst]
        self.container[index_fst] = self.container[index_snd]
        self.container[index_snd] = tmp_fst

    def peek(self) -> V | None:
        if self.length == 0:
            return None
        return self.container[0]

    def should_swap_left(self, parent_index: int) -> bool:
        left_child_index = self.get_left_child_index(parent_index)
        return self.should_swap(parent_index, left_child_index)

    def should_swap_right(self, parent_index: int) -> bool:
        right_child_index = self.get_right_child_index(parent_index)
        return self.should_swap(parent_index, right_child_index)

    def should_swap(self, parent_index: int, child_index: int) -> bool:
        parent = self.container[parent_index]
        child = self.container[child_index]
        return self.compare(parent, child) == 1

    def add(self, value: V):
        self.container.append(value)
        return self.heapify_up()

    def heapify_up(self, custom_index=0) -> None:
        length = self.length
        if length == 0 and length == 1:
            return None

        current_index = (
            custom_index if custom_index > 0 and custom_index < length else length - 1
        )
        parent_index = self.get_parent_index(current_index)

        while self.has_parent(current_index) and self.should_swap(
            parent_index, current_index
        ):
            self.swap(parent_index, current_index)

            current_index = parent_index
            parent_index = self.get_parent_index(current_index)

    def are_pairs_correct(self, parent: V, child: V) -> bool:
        return self.compare(parent, child) == -1

    def heapify_down(self, custom_index=0) -> None:

        current_index = custom_index
        next_index = None
        while self.has_left_child(current_index):

            if self.has_right_child(current_index) and self.are_pairs_correct(
                self.get_right_child(current_index), self.get_left_child(current_index)
            ):
                next_index = self.get_right_child_index(current_index)
            else:
                next_index = self.get_left_child_index(current_index)

            if self.container[current_index] < self.container[next_index]:
                break

            self.swap(current_index, next_index)
            current_index = next_index

    def compare_int(self, x: int, y: int) -> Ordering:
        return -1 if x < y else 1 if x > y else 0

    def poll(self) -> V | None:
        length = self.length

        if length == 0:
            return None
        elif length == 1:
            return self.container.pop()

        last_child_index = length - 1

        #   swap and remove
        parent_index = 0
        self.swap(parent_index, last_child_index)
        value = self.container.pop()
        self.heapify_down()

        return value

    def find(self, value: V) -> List[int]:
        indicies = []
        for index, value_to_find in enumerate(self.container):
            if self.compare(value_to_find, value) == 0:
                indicies.append(index)
        return indicies

    def remove(self, value: V, first_occurrence: bool = False) -> None:
        indicies = self.find(value)
        remove_count = len(indicies)
        first_child_index = 0

        if remove_count > 0 and first_occurrence:
            remove_count = 1

        for i in range(0, remove_count):
            index_to_remove = self.find(value).pop()
            last_child_index = self.length - 1

            if index_to_remove == last_child_index:
                self.container.pop()
            elif index_to_remove == first_child_index:
                self.poll()
            else:
                #   Swap this element with the last element.
                #   Remove the last element after the swap.
                self.swap(index_to_remove, last_child_index)
                self.container.pop()

                current_value = self.container[index_to_remove]

                if current_value < value:
                    self.heapify_up(index_to_remove)
                elif current_value > value:
                    self.heapify_down(index_to_remove)
