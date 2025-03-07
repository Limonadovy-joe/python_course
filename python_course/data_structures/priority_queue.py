from typing import (
    Generic,
    Optional,
    TypeVar,
    List,
    Dict,
)

from python_course.utils.ord import CompareFunction, Ordering

from python_course.data_structures.min_heap import MinHeap

V = TypeVar("V")


class PriorityQueue(MinHeap[V], Generic[V]):

    def __init__(self, compare: Optional[CompareFunction[V]] = None):
        super().__init__(compare or (lambda x, y: (-1 if x < y else 1 if x > y else 0)))
        self.priorities: Dict[int, List[V]] = {}

    def __str__(self):
        return str(self.__dict__)

    def has_value(self, value):
        values = [item for sublist in self.priorities.values() for item in sublist]

        return any(self.compare(value, value_to_find) == 0 for value_to_find in values)

    def has_priority(self, priority: int) -> bool:
        return priority in self.priorities

    def add(self, value: V, priority: int) -> None:
        if not self.has_priority(priority):
            self.priorities[priority] = []

        self.priorities[priority].append(value)

        return super().add(priority)

    def get_priorities_list(self, priority: int):
        return self.priorities[priority]

    def peek(self) -> V | None:
        if len(self.priorities) == 0:
            return None

        priority = self.get_peek_priority()
        priorities = self.get_priorities_list(priority)
        return priorities[0]

    def get_peek_priority(self) -> V | None:
        return super().peek()

    def get_pool_priority(self) -> V | None:
        return super().poll()

    def remove_from_priority_list(self, priority: int, index: int = 0) -> V | None:
        priority_list = self.get_priorities_list(priority)
        value = priority_list.pop(index)
        if len(priority_list) == 0:
            del self.priorities[priority]
        return value

    def poll(self):
        if self.__are_priorities_empty():
            return None

        priority = self.get_pool_priority()
        value = self.remove_from_priority_list(priority, 0)

        return value

    def find_priority_by_value(self, value) -> int | None:
        for priority, values in self.priorities.items():
            for value_to_find in values:
                if super().compare(value, value_to_find) == 0:
                    return priority

    def __are_priorities_empty(self):
        return len(self.priorities) == 0

    def get_value_index(self, priority: int, value: V):
        values = self.get_priorities_list(priority)

        for index, value_to_find in enumerate(values):
            if super().compare(value_to_find, value) == 0:
                return index
        return -1

    def change_priority(self, value: V, new_priority: int) -> None:
        if self.__are_priorities_empty():
            return None

        priority = self.find_priority_by_value(value)
        if priority is None:
            return None

        index = self.get_value_index(priority, value)
        self.remove_from_priority_list(priority, index)
        should_remove_first_occurence = True
        super().remove(priority, should_remove_first_occurence)

        self.add(value, new_priority)

        return index
