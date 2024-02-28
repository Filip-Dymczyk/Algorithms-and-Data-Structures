from typing import Optional


class ChildNode:
    def __init__(self, key: int, value: Optional[str]) -> None:
        self.key = key
        self.value = value
        self.height = 1
        self.left = None
        self.right = None

    def __str__(self) -> str:
        return f"{self.key}:{self.value}"


class AVLBinaryTree:
    def __init__(self) -> None:
        self.root = None

    def search(self, key: int) -> Optional[str]:
        if self.root is not None:
            def in_search(node: ChildNode, key: int) -> Optional[str]:
                if node is None:
                    return None
                if key < node.key:
                    return in_search(node.left, key)
                elif key > node.key:
                    return in_search(node.right, key)
                else:
                    return node.value

            return in_search(self.root, key)
        return None

    def __balance_factor(self, node: ChildNode) -> int:
        if node.left is not None and node.right is not None:
            return node.left.height - node.right.height
        elif node.left is not None and node.right is None:
            return node.left.height
        elif node.left is None and node.right is not None:
            return -node.right.height
        return 0

    def __ll_rotation(self, node: ChildNode) -> ChildNode:
        left = node.left
        node.left = left.right
        left.right = node
        node.height = self.height(node)
        left.height = self.height(left)
        if node == self.root:
            self.root = left
        return left

    def __rr_rotation(self, node: ChildNode) -> ChildNode:
        right = node.right
        node.right = right.left
        right.left = node
        node.height = self.height(node)
        right.height = self.height(right)
        if node == self.root:
            self.root = right
        return right

    def __solve_imbalance(self, node: ChildNode) -> ChildNode:
        if self.__balance_factor(node) > 0:
            if self.__balance_factor(node.left) > 0:
                return self.__ll_rotation(node)
            else:
                node.left = self.__rr_rotation(node.left)
                return self.__ll_rotation(node)
        else:
            if self.__balance_factor(node.right) < 0:
                return self.__rr_rotation(node)
            else:
                node.right = self.__ll_rotation(node.right)
                return self.__rr_rotation(node)

    def insert(self, key: int, value: Optional[str]) -> None:
        if self.root is not None:
            def in_insert(node: ChildNode, key: int, value: Optional[str]) -> ChildNode:
                if node is None:
                    return ChildNode(key, value)
                if key < node.key:
                    node.left = in_insert(node.left, key, value)
                elif key > node.key:
                    node.right = in_insert(node.right, key, value)
                else:
                    node.value = value
                    return node
                node.height = self.height(node)
                if abs(self.__balance_factor(node)) >= 2:
                    return self.__solve_imbalance(node)
                return node

            in_insert(self.root, key, value)
        else:
            self.root = ChildNode(key, value)

    def delete(self, key: int) -> None:
        if self.root is not None:
            def in_delete(node: ChildNode, key: int) -> Optional[ChildNode]:
                if node is not None:
                    if node.key == key:
                        if node.right is None and node.left is None:
                            return None
                        elif node.right is not None and node.left is None:
                            return node.right
                        elif node.right is None and node.left is not None:
                            return node.left
                        else:
                            right = node.right
                            left = node.left
                            new = node.right
                            pred = new
                            while new.left is not None:
                                pred = new
                                new = new.left
                            if new.key != pred.key:
                                pred.left = new.right
                                new.left = left
                                new.right = right
                            else:
                                new.left = left
                            if node.key == self.root.key:
                                self.root = new

                            new.height = self.height(new)
                            if abs(self.__balance_factor(new)) >= 2:
                                return self.__solve_imbalance(new)
                            return new
                    else:
                        if key < node.key:
                            node.left = in_delete(node.left, key)
                        elif key > node.key:
                            node.right = in_delete(node.right, key)

                        node.height = self.height(node)
                        if abs(self.__balance_factor(node)) >= 2:
                            return self.__solve_imbalance(node)
                        return node
                return None

            in_delete(self.root, key)

    def __print_tree(self, node: ChildNode, lvl: int) -> None:
        if node is not None:
            self.__print_tree(node.right, lvl + 5)

            print()
            print(lvl * " ", node.key, node.value)

            self.__print_tree(node.left, lvl + 5)

    def print_tree(self) -> None:
        print("==============")
        self.__print_tree(self.root, 0)
        print("==============")

    def height(self, node: ChildNode) -> int:
        if self.root is not None:
            def in_height(node: ChildNode) -> int:
                if node is None:
                    return 0
                left_height = in_height(node.left)
                right_height = in_height(node.right)
                return 1 + max(left_height, right_height)

            return in_height(node)
        return 0

    def print_list(self) -> None:
        if self.root is not None:
            def in_print_list(node: ChildNode) -> None:
                if node is None:
                    return
                in_print_list(node.left)
                print(node, end="")
                print(", ", end="")
                in_print_list(node.right)

            in_print_list(self.root)

def main():
    tree = AVLBinaryTree()
    d = {50: 'A', 15: 'B', 62: 'C', 5: 'D', 2: 'E', 1: 'F', 11: 'G', 100: 'H', 7: 'I', 6: 'J',
         55: 'K', 52: 'L', 51: 'M', 57: 'N', 8: 'O', 9: 'P', 10: 'R', 99: 'S', 12: 'T'}
    for key, value in d.items():
        tree.insert(key, value)
    tree.print_tree()
    tree.print_list()
    print()
    print(tree.search(10))
    tree.delete(50)
    tree.delete(52)
    tree.delete(11)
    tree.delete(57)
    tree.delete(1)
    tree.delete(12)
    tree.insert(3, 'AA')
    tree.insert(4, 'BB')
    tree.delete(7)
    tree.delete(8)
    tree.print_tree()
    tree.print_list()


if __name__ == "__main__":
    main()


