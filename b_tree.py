from typing import Optional, Tuple


class Node:
    def __init__(self) -> None:
        self.keys = []
        self.children = None


class BTree:
    def __init__(self, max_keys: int) -> None:
        self.root = None
        self.max = max_keys

    def __loop_add(self, key: int, node: Node) -> None:
        temp_keys = []
        index = 0
        flag = True

        while index < len(node.keys):
            if node.keys[index] > key and flag:
                temp_keys.append(key)
                flag = False
            else:
                temp_keys.append(node.keys[index])
                index += 1
        node.keys = temp_keys
        if key > node.keys[-1]:
            node.keys.append(key)

    def __add_key(self, key: int, node: Node) -> Optional[Tuple[int, Node]]:
        if len(node.keys) < self.max:
            self.__loop_add(key, node)
            return None

        mid = self.max // 2
        mid_key = node.keys[mid]
        mid = mid + 1 if mid_key > key else mid

        self.__loop_add(key, node)
        new_node = Node()
        new_node.keys = node.keys[mid + 1:]
        node.keys = node.keys[:mid]

        if node.children:
            new_node.children = node.children[mid + 1:]
            node.children = node.children[:mid + 1]
        return mid_key, new_node

    def __unpack_tuple(self, tup: Optional[Tuple[int, Node]], node: Node) -> Optional[Node]:
        if isinstance(tup, Tuple):
            mid_key, new_node = tup
            parent_node = Node()
            parent_node.keys.append(mid_key)
            parent_node.children = [node, new_node]
            return parent_node
        return None

    def __insert_helper(self, key: int, node: Node) -> Optional[Node]:
        f = node
        for i in range(len(node.keys)):
            if key < f.keys[i]:
                if f.children is None:
                    tup = self.__add_key(key, f)
                    return self.__unpack_tuple(tup, f)
                else:
                    created = self.__insert_helper(key, f.children[i])
                    if isinstance(created, Node):
                        to_add_child = created.children[1]
                        temp_children = f.children[:i + 1]
                        temp_children.append(to_add_child)
                        temp_children += f.children[i + 1:]
                        f.children = temp_children
                        tup = self.__add_key(created.keys[0], f)
                        return self.__unpack_tuple(tup, f)
                    return None
        if f.children:
            child = f.children[len(f.keys)]
            parent_node = self.__insert_helper(key, child)
            if isinstance(parent_node, Node):
                child_from_par = parent_node.children[1]
                f.children.append(child_from_par)
                tup = self.__add_key(parent_node.keys[0], f)
                return self.__unpack_tuple(tup, f)
            return None
        else:
            tup = self.__add_key(key, f)
            return self.__unpack_tuple(tup, f)

    def insert(self, key: int) -> None:
        if not self.root:
            node = Node()
            node.keys.append(key)
            self.root = node
        else:
            new_node = self.__insert_helper(key, self.root)
            if isinstance(new_node, Node):
                self.root = new_node

    def print_tree(self):
        print("==============")
        self._print_tree(self.root, 0)
        print("==============")

    def _print_tree(self, node, lvl):
        if node:
            for i in range(len(node.keys) + 1):
                if node.children:
                    self._print_tree(node.children[i], lvl + 1)
                if i < len(node.keys):
                    print(lvl * '  ', node.keys[i])

def main():
    l1 = [5, 17, 2, 14, 7, 4, 12, 1, 16, 8, 11, 9, 6, 13, 0, 3, 18, 15, 10, 19]
    l2 = [i for i in range(20)]

    b_tree1 = BTree(3)
    for nr in l1:
        b_tree1.insert(nr)
    b_tree1.print_tree()

    b_tree2 = BTree(3)
    for nr in l2:
        b_tree2.insert(nr)
    b_tree2.print_tree()

    b_tree3 = BTree(5)
    for nr in l2:
        b_tree3.insert(nr)
    b_tree3.print_tree()


if __name__ == "__main__":
    main()

