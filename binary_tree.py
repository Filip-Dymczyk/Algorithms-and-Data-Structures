from typing import Optional, Union


class ChildNode:
    def __init__(self, key: int, value: Optional[str]) -> None:
        self.key = key
        self.value = value
        self.left = None
        self.right = None

    def __str__(self) -> str:
        return f"{self.key}:{self.value}"


class BinaryTree:
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

    def insert(self, key: int, value: Union[str, float]) -> None:
        if self.root is not None:
            def in_insert(node: ChildNode, key: int, value: Union[str, float]) -> ChildNode:
                if node is None:
                    return ChildNode(key, value)
                if key < node.key:
                    node.left = in_insert(node.left, key, value)
                elif key > node.key:
                    node.right = in_insert(node.right, key, value)
                else:
                    node.value = value
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
                            if node.key == self.root.key:
                                self.root.key = new.key
                                self.root.value = new.value
                            if new.key != pred.key:
                                pred.left = new.right
                                new.left = left
                                new.right = right
                            else:
                                new.left = left
                            return new
                    else:
                        if key < node.key:
                            node.left = in_delete(node.left, key)
                        elif key > node.key:
                            node.right = in_delete(node.right, key)
                        return node

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
        if node is not None:
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
    tree = BinaryTree()
    d = {50: 'A', 15: 'B', 62: 'C', 5: 'D', 20: 'E', 58: 'F', 91: 'G', 3: 'H', 8: 'I', 37: 'J', 60: 'K', 24: 'L'}
    for key, value in d.items():
        tree.insert(key, value)

    tree.print_tree()
    tree.print_list()
    print()
    print(tree.search(24))
    tree.insert(20, "AA")
    tree.insert(6, 'M')
    tree.delete(62)
    tree.insert(59, 'N')
    tree.insert(100, 'P')
    tree.delete(8)
    tree.delete(15)
    tree.insert(55, 'R')
    tree.delete(50)
    tree.delete(5)
    tree.delete(24)
    print(tree.height(tree.root))
    tree.print_list()
    print()
    tree.print_tree()


if __name__ == "__main__":
    main()
