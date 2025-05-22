from typing import TypeVar, Optional, Generic, Union, Tuple, Literal, TypeGuard


T = TypeVar("T")
Direction = Literal["left", "right"]


def is_tuple(value: T) -> bool:
    return value is not None


class BinarySearchTreeNode(Generic[T]):

    def __init__(
        self,
        value: Optional[T] = None,
        left: Optional["BinarySearchTreeNode[T]"] = None,
        right: Optional["BinarySearchTreeNode[T]"] = None,
    ):
        self.value = value
        self.left = left
        self.right = right
        self.meta: dict[str, str] = dict()

    def __str__(self) -> str:
        def in_order(node):
            if node is None:
                return []
            return (
                in_order(node.left)
                + [str(node.value) if node.value is not None else ""]
                + in_order(node.right)
            )

        return ",".join(in_order(self))

    def to_string(self) -> str:
        return self.__str__()

    def comparator(
        self, x: "BinarySearchTreeNode[T]", y: "BinarySearchTreeNode[T]"
    ) -> int:
        """Default comparator assuming T supports comparison operators."""
        return (
            -1 if x.value < y.value else 1 if x.value > y.value else 0
        )  # Returns -1, 0, or 1

    def insert(self, value: T) -> Union["BinarySearchTreeNode[T]", None]:

        if self.value is None:
            self.value = value
            return self

        root_to_traverse = self
        new_node = BinarySearchTreeNode(value)

        while root_to_traverse is not None:
            root_value = root_to_traverse.value

            if value == root_value:
                return None

            if value < root_value:
                if root_to_traverse.left is None:
                    root_to_traverse.left = new_node
                    return new_node
                root_to_traverse = root_to_traverse.left
            elif value > root_value:
                if root_to_traverse.right is None:
                    root_to_traverse.right = new_node
                    return new_node
                root_to_traverse = root_to_traverse.right

    def find_min(self) -> Union["BinarySearchTreeNode[T]", None]:
        if self.value is None:
            return None

        min_value_node = self
        node_to_traverse = min_value_node

        while node_to_traverse is not None:
            if (
                node_to_traverse.left is not None
                and node_to_traverse.left.value < min_value_node.value
            ):
                min_value_node = node_to_traverse.left
                node_to_traverse = min_value_node
            else:
                node_to_traverse = None

        return min_value_node

    def find_max(self) -> "BinarySearchTreeNode[T]":

        max_value_node = self
        node_to_traverse = max_value_node

        while node_to_traverse is not None:
            if (
                node_to_traverse.right is not None
                and node_to_traverse.right.value > max_value_node.value
            ):
                max_value_node = node_to_traverse.right
                node_to_traverse = max_value_node
            else:
                node_to_traverse = None

        return max_value_node

    def find(self, value: T) -> Union["BinarySearchTreeNode[T]", None]:
        if self.value is None:
            return None

        node_to_traverse = self
        node_to_find = None

        while node_to_traverse is not None:
            value_to_find = node_to_traverse.value

            if node_to_traverse.value == value:
                node_to_find = node_to_traverse
                return node_to_find

            if node_to_traverse.left is not None and value < value_to_find:
                node_to_traverse = node_to_traverse.left
            elif node_to_traverse.right is not None and value > value_to_find:
                node_to_traverse = node_to_traverse.right
            else:
                node_to_traverse = None

        return node_to_find

    def has_left(self) -> TypeError:
        return self.left is not None and self.left.value is not None

    def has_right(self) -> bool:
        return self.right is not None and self.right.value is not None

    @staticmethod
    def get_parent(
        root: "BinarySearchTreeNode[T]",
        node: "BinarySearchTreeNode[T]",
    ) -> Union[Tuple["BinarySearchTreeNode[T]", Direction], None]:
        node_to_traverse = root
        direction: Direction = "left"
        parent: Optional["BinarySearchTreeNode[T]"] = None

        while node_to_traverse is not None:
            node_value = node_to_traverse.value
            node_to_find_value = node.value

            if node_value == node_to_find_value:
                if parent is not None:
                    return (parent, direction)

            if node_to_traverse.left is not None and node_to_find_value < node_value:
                parent = node_to_traverse
                direction = "left"
                node_to_traverse = node_to_traverse.left
            elif node_to_traverse.right is not None and node_to_find_value > node_value:
                parent = node_to_traverse
                direction = "right"
                node_to_traverse = node_to_traverse.right
            else:
                node_to_traverse = None

    @staticmethod
    def is_defined(
        node: Optional["BinarySearchTreeNode[T]"],
    ) -> TypeGuard["BinarySearchTreeNode[T]"]:
        return isinstance(node, BinarySearchTreeNode) and node.value is not None

    def remove(self, value: T) -> Union["BinarySearchTreeNode[T]", None]:
        if self.value is None:
            return None

        root = self
        node_to_traverse = self
        node_to_remove = None

        while node_to_traverse is not None:

            node_value = node_to_traverse.value
            if node_value == value:
                node_to_remove = node_to_traverse
                parent_node_to_remove_info = BinarySearchTreeNode.get_parent(
                    root, node_to_remove
                )

                #   if it has parent
                if isinstance(parent_node_to_remove_info, tuple):
                    parent_node_to_remove = parent_node_to_remove_info[0]
                    parent_node_to_remove_direction = parent_node_to_remove_info[1]

                    #   check left-subtree
                    if node_to_remove.has_left():
                        left_child = node_to_remove.left

                        largest_node = left_child.find_max()
                        parent_largest_node_info = BinarySearchTreeNode.get_parent(
                            root, largest_node
                        )

                        if largest_node is not None and isinstance(
                            parent_largest_node_info, tuple
                        ):
                            parent_largest_node = parent_largest_node_info[0]
                            parent_largest_node_direction = parent_largest_node_info[1]

                            #   check whether the parent is node to remove
                            if parent_largest_node.value == node_to_remove.value:
                                #   copy only right nodes from node to remove
                                setattr(largest_node, "right", node_to_remove.right)

                                setattr(
                                    parent_node_to_remove,
                                    parent_node_to_remove_direction,
                                    largest_node,
                                )
                            else:
                                if largest_node.has_left():
                                    #   set left child node from largest node to its parent
                                    setattr(
                                        parent_largest_node,
                                        parent_largest_node_direction,
                                        largest_node.left,
                                    )

                                    #   copy nodes from node to remove
                                    setattr(largest_node, "left", node_to_remove.left)
                                    setattr(largest_node, "right", node_to_remove.right)

                                    #   set largest node to parent
                                    setattr(
                                        parent_node_to_remove,
                                        parent_node_to_remove_direction,
                                        largest_node,
                                    )
                                else:
                                    #   remove largest node from its parent
                                    setattr(
                                        parent_largest_node,
                                        parent_largest_node_direction,
                                        None,
                                    )

                                    #   copy nodes from node to remove
                                    setattr(largest_node, "left", node_to_remove.left)
                                    setattr(largest_node, "right", node_to_remove.right)

                                    #   set largest node to parent
                                    setattr(
                                        parent_node_to_remove,
                                        parent_node_to_remove_direction,
                                        largest_node,
                                    )
                    elif node_to_remove.has_right():
                        right_node = node_to_remove.right
                        #   only set parent node to remove right nodes
                        setattr(
                            parent_node_to_remove,
                            parent_node_to_remove_direction,
                            right_node,
                        )
                    else:
                        #   in case it is leaf node, only remove from its parent
                        setattr(
                            parent_node_to_remove,
                            parent_node_to_remove_direction,
                            None,
                        )

                    node_to_remove.left = None
                    node_to_remove.right = None
                    return node_to_remove

                else:
                    #   removing root value

                    #   if left subtree is defined find largest node
                    if BinarySearchTreeNode.is_defined(node_to_remove.left):

                        #   get largest node
                        largest_node: BinarySearchTreeNode[T] = node_to_remove.left
                        node_to_traverse: Optional[BinarySearchTreeNode[T]] = (
                            largest_node
                        )
                        while BinarySearchTreeNode.is_defined(node_to_traverse):
                            if BinarySearchTreeNode.is_defined(node_to_traverse.right):
                                node_to_traverse = node_to_traverse.right
                                largest_node = node_to_traverse
                            else:
                                node_to_traverse = None

                        parent_largest_node_tuple = BinarySearchTreeNode.get_parent(
                            root, largest_node
                        )
                        if isinstance(parent_largest_node_tuple, tuple):
                            parent_largest_node = parent_largest_node_tuple[0]

                            tmp_root_value = root.value
                            if parent_largest_node.value == tmp_root_value:
                                root.value = largest_node.value

                                largest_node.value = tmp_root_value

                                if BinarySearchTreeNode.is_defined(largest_node.left):
                                    root.left = largest_node.left
                                else:
                                    root.left = None

                            else:
                                if BinarySearchTreeNode.is_defined(largest_node.left):
                                    root.value = largest_node.value

                                    largest_node.value = tmp_root_value
                                    parent_largest_node.right = largest_node.left
                                else:
                                    root.value = largest_node.value

                                    largest_node.value = tmp_root_value
                                    parent_largest_node.right = None
                        node_to_remove = largest_node
                    #   if not left subtree is defined get right nodes
                    elif BinarySearchTreeNode.is_defined(node_to_remove.right):

                        right_node = node_to_remove.right
                        tmp_node_to_remove_value = node_to_remove.value

                        node_to_remove.value = right_node.value
                        node_to_remove.left = right_node.left
                        node_to_remove.right = right_node.right

                        right_node.value = tmp_node_to_remove_value
                        node_to_remove = right_node
                    else:
                        node_to_remove.value = None

                    node_to_remove.left = None
                    node_to_remove.right = None
                    return node_to_remove

            elif node_to_traverse.left is not None and value < node_value:
                node_to_traverse = node_to_traverse.left
            elif node_to_traverse.right is not None and value > node_value:
                node_to_traverse = node_to_traverse.right
            else:
                node_to_traverse = None

        return node_to_remove
