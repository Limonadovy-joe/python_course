from typing import Generic, TypeVar, List, Optional, Literal, Callable, Tuple

from collections import deque

T = TypeVar("T")


class HeapNode(Generic[T]):
    def __init__(
        self,
        value: T,
        left: Optional["HeapNode[T]"] = None,
        right: Optional["HeapNode[T]"] = None,
        parent: Optional["HeapNode[T]"] = None,
    ):
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent

        if self.left:
            self.left.parent = self
        if self.right:
            self.right.parent = self

    def __eq__(self, other):
        if not isinstance(other, HeapNode):
            return False
        return self.value == other.value

    def __repr__(self):
        return f"HeapNode({self.value}, left={self.left}, right={self.right})"

    def is_empty(self) -> bool:
        return self.value is None and not self.has_children()

    def has_left(self) -> bool:
        return self.left is not None

    def has_right(self) -> bool:
        return self.right is not None

    def has_children(self) -> bool:
        return self.has_left() or self.has_right()

    def has_parent(self) -> bool:
        return self.parent is not None


#   To ordering utils
Ordering = Literal[-1, 0, 1]
#   To function utils
CompareFunction = Callable[[T, T], Ordering]
Position = Literal["Left", "Right"]


class MaxHeap(Generic[T]):

    def __init__(self, compare: Optional[CompareFunction[T]]):
        self.compare = compare
        if compare is None:
            self.compare = lambda x, y: -1 if x < y else 1 if x > y else 0
        self.root: Optional[HeapNode[T]] = None
        self.length = 0

    def __str__(self):

        if self.root is None:
            return ""

        current_node = self.root
        result = []
        queue = deque([current_node])

        while queue:
            node = queue.popleft()
            result.append(str(node.value))

            if node.has_left():
                queue.append(node.left)

            if node.has_right():
                queue.append(node.right)

        return ",".join(result)

    def is_empty(self) -> bool:
        return self.root is None

    def add_node_by_pos(
        self, node: HeapNode[T], value: T, pos: Position = "left"
    ) -> HeapNode[T]:
        new_node = HeapNode(value)
        left_or_right: Position = "Left" if pos == "Left" else "Right"

        node[left_or_right] = new_node

        return node

    def insert(self, node: HeapNode[T], new_node: HeapNode[T]):
        queue = deque([node])

        while len(queue) > 0:
            current_node = queue.popleft()

            if current_node.has_left():
                queue.append(current_node.left)
            else:
                current_node.left = new_node
                new_node.parent = current_node
                return new_node

            if current_node.has_right():
                queue.append(current_node.right)
            else:
                current_node.right = new_node
                new_node.parent = current_node
                return new_node

        return new_node

    def is_heap_order_valid(self, parent_node: HeapNode[T], child: HeapNode[T]) -> bool:
        return self.compare(parent_node.value, child.value) >= 0

    def swap(self, fst_node: HeapNode[T], snd_node: HeapNode[T]) -> None:
        tmp_fst_value = fst_node.value
        fst_node.value = snd_node.value
        snd_node.value = tmp_fst_value

    def heapify_up(self, node: HeapNode[T]):
        current_node = node
        while current_node.has_parent() and not self.is_heap_order_valid(
            current_node.parent, current_node
        ):
            self.swap(current_node.parent, current_node)
            current_node = current_node.parent

    def add(self, value: T) -> None:
        new_node = HeapNode(value)

        if self.is_empty():
            self.root = new_node
            return None

        self.insert(self.root, new_node)
        self.heapify_up(new_node)

    def get_left_most_node(self, node: HeapNode[T]) -> Optional[HeapNode[T]]:
        left_most_node: Optional[HeapNode[T]] = None
        queue = [node]

        while len(queue) > 0:
            left_most_node = queue.pop(0)

            if left_most_node.has_left():
                queue.append(left_most_node.left)

            if left_most_node.has_right():
                queue.append(left_most_node.right)

        return left_most_node

    def heapify_down(self, node: HeapNode[T]) -> None:
        current_node = node
        while (
            current_node.has_left()
            and not self.is_heap_order_valid(current_node, current_node.left)
        ) or (
            current_node.has_right()
            and not self.is_heap_order_valid(current_node, current_node.right)
        ):
            largest_node = current_node.left
            if (
                current_node.has_right()
                and self.compare(largest_node.value, current_node.right.value) == -1
            ):
                largest_node = current_node.right

            self.swap(current_node, largest_node)
            current_node = largest_node

    def poll(self) -> T | None:
        if self.is_empty():
            return None

        root_node = self.root
        top: T = root_node.value

        if not self.root.has_children():
            self.root = None
            del root_node
            return top

        last_node = self.get_left_most_node(root_node)

        if not last_node.is_empty():
            self.swap(root_node, last_node)

            if last_node.has_parent():
                parent = last_node.parent

                if parent.has_right():
                    parent.right = None
                else:
                    parent.left = None
            del last_node

        self.heapify_down(root_node)
        return top

    #   DFS (Preorder Traversal)
    def find_node(self, node: Optional[HeapNode[T]], value: T) -> List[HeapNode[T]]:
        matching_nodes: List[HeapNode[T]] = []

        if self.compare(node.value, value) == 0:
            matching_nodes.append(node)

        if node.left is not None:
            matching_nodes.extend(self.find_node(node.left, value))

        if node.right is not None:
            matching_nodes.extend(self.find_node(node.right, value))

        return matching_nodes

    def are_nodes_equal(self, node_fst: HeapNode[T], node_snd: HeapNode[T]) -> bool:
        return self.compare(node_fst.value, node_snd.value) == 0

    def delete(self, value: T) -> Optional[T]:
        root_node = self.root

        node = None
        nodes = [node]
        while len(nodes) > 0:
            nodes = self.find_node(root_node, value)
            if len(nodes) == 0:
                return node

            node = nodes[0]
            last_node = self.get_left_most_node(root_node)

            #   remove root node
            if not node.has_parent() and (not node.has_left() and not node.has_right()):
                self.root = None
                return node

            #   Remove the last node directly, avoiding unnecessary tree traversal.
            if self.are_nodes_equal(node, last_node) and not node.has_children():
                if node.has_parent():
                    parent = node.parent

                    if parent.has_right():
                        parent.right = None
                    else:
                        parent.left = None

                return node

            self.swap(node, last_node)

            #   Remove the node after swapping,the last_node should  be deleted
            if last_node.has_parent():
                parent = last_node.parent

                if parent.has_right():
                    parent.right = None
                else:
                    parent.left = None

            new_node = node
            old_node = last_node
            if new_node.value > old_node.value:
                self.heapify_up(new_node)
            elif new_node.value < old_node.value:
                self.heapify_down(new_node)

        return node

    def find_position(self, value: T) -> List[Tuple[HeapNode[T], int]]:
        positions: List[Tuple[HeapNode[T], int]] = []
        if self.is_empty():
            return positions

        pos = 0
        node_to_find = HeapNode(value)
        queue = deque([self.root])

        while len(queue) > 0:
            node = queue.popleft()

            if self.are_nodes_equal(node, node_to_find):
                positions.append((node, pos))

            if node.has_left():
                queue.append(node.left)

            if node.has_right():
                queue.append(node.right)

            pos = pos + 1

        return positions
