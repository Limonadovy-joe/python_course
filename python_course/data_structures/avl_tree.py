from typing import TypeVar, Optional


from python_course.data_structures.binary_tree_node import BinaryTreeNode
from python_course.utils.ord import CompareFunction
from python_course.data_structures.binary_search_tree_node import BinarySearchTreeNode
from python_course.data_structures.binary_search_tree import BinarySearchTree

T = TypeVar("T")


class AvlTree(BinarySearchTree[T]):
    def __init__(
        self,
        comparator: Optional[CompareFunction[T]] = None,
    ):
        super().__init__(comparator=comparator)

    def right_rotate(
        self,
        lowest_unbalanced_ancestor: "BinaryTreeNode[T]",
        left_child: "BinaryTreeNode[T]",
    ) -> None:
        parent_lowest_unbalanced_ancestor = lowest_unbalanced_ancestor.parent

        # case nodes are not consecutive in two lefts, low_un_anc -> left - > right
        if lowest_unbalanced_ancestor.right and left_child.right:
            left_child_right = left_child.right

            #   set new root or new left to its parent
            if parent_lowest_unbalanced_ancestor:
                parent_lowest_unbalanced_ancestor.set_left(left_child)
            else:
                self.root = left_child
                left_child.parent = None

            #   need to move left_child_right to right subtree
            #   move low_un_ancestor to new created parent

            #   also left_child_right has new parent lua
            lowest_unbalanced_ancestor.set_left(left_child_right)

            #   is new root or parent
            #   firstly remove left_child_right which was moved
            left_child.right = None
            #   set new right subtree
            left_child.set_right(lowest_unbalanced_ancestor)

        else:
            # case only low_un_anc -> left - > left
            lowest_unbalanced_ancestor.left = None

            left_child.set_right(lowest_unbalanced_ancestor)
            left_child.parent = parent_lowest_unbalanced_ancestor

            if parent_lowest_unbalanced_ancestor is None:
                self.root = left_child
            else:
                parent_lowest_unbalanced_ancestor.left = left_child

        return None

    def set_parent_child_on_equality_nodes(
        self,
        parent: "BinaryTreeNode[T]",
        node_to_equal: "BinaryTreeNode[T]",
        child: "BinaryTreeNode[T]",
    ) -> None:
        value_to_equal = node_to_equal.value
        if value_to_equal:
            if parent.left and parent.left.value == value_to_equal:
                parent.set_left(child)
            elif parent.right and parent.right.value == value_to_equal:
                parent.set_right(child)

    def left_right_rotate(
        self,
        lowest_unbalanced_ancestor: "BinaryTreeNode[T]",
        left_child: "BinaryTreeNode[T]",
        left_right_child: "BinaryTreeNode[T]",
    ) -> None:
        parent_lowest_unbalanced_ancestor = lowest_unbalanced_ancestor.parent

        #   case if it has parent
        if parent_lowest_unbalanced_ancestor:
            self.set_parent_child_on_equality_nodes(
                parent_lowest_unbalanced_ancestor,
                lowest_unbalanced_ancestor,
                left_right_child,
            )
        else:
            #   handle root case
            left_right_child.parent = None
            self.root = left_right_child

        #   reset lefts and right nodes
        left_child.right = None
        lowest_unbalanced_ancestor.left = None

        left_right_child.set_left(left_child)
        left_right_child.set_right(lowest_unbalanced_ancestor)

        return None

    def left_rotate(
        self,
        lowest_unbalanced_ancestor: "BinaryTreeNode[T]",
        right_child: "BinaryTreeNode[T]",
    ) -> None:
        parent_lowest_unbalanced_ancestor = lowest_unbalanced_ancestor.parent

        if lowest_unbalanced_ancestor.left and right_child.left:
            right_child_left = right_child.left

            #   case if it has parent
            if parent_lowest_unbalanced_ancestor:
                #   set new right and also remove parent from lowest_unbalanced_ancestor
                if (
                    parent_lowest_unbalanced_ancestor.left
                    and parent_lowest_unbalanced_ancestor.left.value
                    == lowest_unbalanced_ancestor.value
                ):
                    parent_lowest_unbalanced_ancestor.set_left(right_child)
                elif (
                    parent_lowest_unbalanced_ancestor.right
                    and parent_lowest_unbalanced_ancestor.right.value
                    == lowest_unbalanced_ancestor.value
                ):
                    parent_lowest_unbalanced_ancestor.set_right(right_child)
            else:
                #   handle root case
                right_child.parent = None
                self.root = right_child

            right_child.left = None

            #   create new left subtree with right_child_left
            lowest_unbalanced_ancestor.set_right(right_child_left)
            #   resets parent new subroot
            right_child.parent = parent_lowest_unbalanced_ancestor

            #       assign new left subtree to the sub-root
            right_child.set_left(lowest_unbalanced_ancestor)
        else:
            #   case if it has parent
            if parent_lowest_unbalanced_ancestor:
                #   set new right and also remove parent from lowest_unbalanced_ancestor
                if (
                    parent_lowest_unbalanced_ancestor.left
                    and parent_lowest_unbalanced_ancestor.left.value
                    == lowest_unbalanced_ancestor.value
                ):
                    parent_lowest_unbalanced_ancestor.set_left(right_child)
                elif (
                    parent_lowest_unbalanced_ancestor.right
                    and parent_lowest_unbalanced_ancestor.right.value
                    == lowest_unbalanced_ancestor.value
                ):
                    parent_lowest_unbalanced_ancestor.set_right(right_child)
            else:
                #   handle root case
                right_child.parent = None
                self.root = right_child
            lowest_unbalanced_ancestor.right = None
            right_child.set_left(lowest_unbalanced_ancestor)

        return None

    def right_left_rotate(
        self,
        lowest_unbalanced_ancestor: "BinaryTreeNode[T]",
        right_child: "BinaryTreeNode[T]",
        right_left_child: "BinaryTreeNode[T]",
    ) -> None:
        parent_lowest_unbalanced_ancestor = lowest_unbalanced_ancestor.parent

        #   case if it has parent
        if parent_lowest_unbalanced_ancestor:
            self.set_parent_child_on_equality_nodes(
                parent_lowest_unbalanced_ancestor,
                lowest_unbalanced_ancestor,
                right_left_child,
            )
        else:
            #   handle root case
            right_left_child.parent = None
            self.root = right_left_child

        #   reset lefts and right nodes
        right_child.left = None
        lowest_unbalanced_ancestor.right = None

        right_left_child.set_left(lowest_unbalanced_ancestor)
        right_left_child.set_right(right_child)

    def balance(self, node: "BinaryTreeNode[T]") -> None:

        if self._is_left_case(node):
            left_child = node.left
            if left_child is None:
                return None
            if self._is_left_left_case(left_child):
                self.right_rotate(node, left_child)
            elif self._is_left_right_case(left_child):
                left_right_child = left_child.right
                if left_right_child:
                    self.left_right_rotate(node, left_child, left_right_child)

        elif self._is_right_case(node):
            right_child = node.right
            if right_child is None:
                return None

            if self._is_right_right_case(right_child):
                self.left_rotate(node, right_child)
            elif self._is_right_left_case(right_child):
                right_left_child = right_child.left
                if right_left_child:
                    self.right_left_rotate(node, right_child, right_left_child)

        else:
            return None

    def insert(self, value: T) -> Optional[BinarySearchTreeNode[T]]:
        node = super().insert(value)
        while node is not None:
            self.balance(node)
            node = node.parent
        return node

    def _is_left_case(self, parent: "BinaryTreeNode[T]") -> bool:
        return parent.balance_factor > 1

    def _is_left_left_case(self, child: "BinaryTreeNode[T]") -> bool:
        return child.balance_factor > 0

    def _is_left_right_case(self, child: "BinaryTreeNode[T]") -> bool:
        return child.balance_factor < 0

    def _is_right_case(self, node: "BinaryTreeNode[T]") -> bool:
        return node.balance_factor < -1

    def _is_right_right_case(self, child: "BinaryTreeNode[T]") -> bool:
        return child.balance_factor < 0

    def _is_right_left_case(self, child: "BinaryTreeNode[T]") -> bool:
        return child.balance_factor > 0

    def remove(self, value: T) -> bool:
        if self.root.value is None:
            return False

        try:
            node = super().find(value)
            parent = node.parent

            super().remove(value)

            if parent is None:
                parent = self.root
            self.balance(self.root)
            return True
        except Exception as e:
            match e:
                case RuntimeError():
                    print(f"RuntimeError during removal of {value}: {e}")
                    return False
                case _:
                    print(f"Unexpected error during removal of {value}: {e}")
                    raise e
