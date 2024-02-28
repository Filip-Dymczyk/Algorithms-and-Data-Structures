import string
from random import random
from typing import Optional, Union

def random_level(p: float = 0.5, max_level: int = 4) -> int:
    lvl = 1
    while random() < p and lvl < max_level:
        lvl = lvl + 1
    return lvl


class Node:
    def __init__(self, key: Optional[int], value: Optional[Union[float, str]], lvl: int) -> None:
        self.key = key
        self.value = value
        self.lvl = lvl
        self.next = [None for i in range(lvl)]

    def __str__(self) -> str:
        return f"{self.key}: {self.value}"


class SkipList:
    def __init__(self, max_lvl: int) -> None:
        self.head = Node(None, None, max_lvl)
        self.max_lvl = max_lvl

    def search(self, key: int) -> Optional[Union[float, str]]:
        if self.head.next != [None] * self.max_lvl:
            node = self.head
            lvl = self.max_lvl
            while lvl >= 1:
                next = node.next[lvl - 1]
                if next is not None:
                    if next.key < key:
                        lvl = next.lvl
                        node = next
                    elif next.key > key:
                        lvl -= 1
                    else:
                        return next.value
                else:
                    lvl -= 1
        return None

    def insert(self, key: int, value: Union[float, str]) -> None:
        node = self.head
        lvl = self.max_lvl
        pred = []
        while lvl >= 1:
            next = node.next[lvl - 1]
            if next is not None:
                if next.key < key:
                    node = next
                elif next.key > key:
                    pred.append(node)
                    lvl -= 1
                else:
                    next.value = value
                    return
            else:
                pred.append(node)
                lvl -= 1
        pred.reverse()
        new_node = Node(key, value, random_level(max_level=self.max_lvl))
        for i in range(new_node.lvl):
            before = pred[i]
            new_node.next[i] = before.next[i % before.lvl]
            before.next[i % before.lvl] = new_node

    def remove(self, key: int) -> None:
        if self.head.next != [None] * self.max_lvl:
            node = self.head
            lvl = self.max_lvl
            pred = []
            if key >= node.next[0].key:
                while lvl >= 1:
                    next = node.next[lvl - 1]
                    if next is not None:
                        if next.key < key:
                            node = next
                        else:
                            pred.append(node)
                            lvl -= 1
                    else:
                        pred.append(node)
                        lvl -= 1
                next = node.next[0]
                pred.reverse()
                if next is not None:
                    after = next.next
                    for i in range(next.lvl):
                        before = pred[i]
                        before.next[i % before.lvl] = after[i]

    def __str__(self) -> str:
        res = ""
        f = self.head.next[0]
        if f is not None:
            res += "["
            while f.next[0] is not None:
                res += f"{f.key}: {f.value}, "
                f = f.next[0]
            res += f"{f.key}: {f.value}]"
        return res

    def display_list(self):
        node = self.head.next[0]
        keys = []
        while node is not None:
            keys.append(node.key)
            node = node.next[0]

        for lvl in range(self.max_lvl - 1, -1, -1):
            print("{}: ".format(lvl), end=" ")
            node = self.head.next[lvl]
            idx = 0
            while node is not None:
                while node.key > keys[idx]:
                    print("  ", end=" ")
                    idx += 1
                idx += 1
                print("{:2d}".format(node.key), end=" ")
                node = node.next[lvl]
            print("")

def main():
    s = SkipList(6)
    letters = list(string.ascii_uppercase)

    for i in range(15):
        s.insert(i + 1, letters[i])
    s.display_list()
    print()
    print(s.search(2))
    s.insert(2, 'Z')
    print(s.search(2))

    for i in range(5, 8):
        s.remove(i)
    print()
    print(s)
    s.insert(6, 'W')
    print(s)


if __name__ == "__main__":
    main()
