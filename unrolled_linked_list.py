from typing import Optional

size = 6


class Node:
    def __init__(self) -> None:
        self.arr = [None for i in range(size)]
        self.fill = 0
        self.next = None

    def put_in(self, index: int, elem) -> None:
        if self.fill > 0:
            if index < size - 1:
                tab = [None for i in range(size)]
                tab[:index] = self.arr[:index]
                tab[index] = elem
                tab[index + 1:] = self.arr[index:-1]
                self.arr = tab
            elif index == size - 1:
                self.arr[index] = elem
        else:
            self.arr[index] = elem
        self.fill += 1

    def take_out(self, index: int) -> None:
        if self.fill > 0 and self.arr[index] is not None:
            if index < size - 1:
                tab = [None for i in range(size)]
                tab[:index] = self.arr[:index]
                tab[index:-1] = self.arr[index + 1:]
                self.arr = tab
            elif index == size - 1:
                self.arr[index] = None
            self.fill -= 1

    def __str__(self) -> Optional[str]:
        if self.fill > 0:
            res = "["
            for i in range(size - 1):
                res = res + f"{self.arr[i]}, "
            res = res + f"{self.arr[size - 1]}]"
            return res
        return "None"


class UnrolledLinkedList:
    def __init__(self) -> None:
        self.head = None

    def get(self, index: int) -> Optional[float]:
        if self.head is not None:
            number_node = index // size
            ind = index % size
            next = self.head
            for i in range(number_node):
                next = next.next
                if next is None:
                    return None
            return next.arr[ind]
        return None

    def insert(self, index: int, data) -> None:
        if self.head is not None:
            number_node = index // size
            ind = index % size
            next = self.head
            count = 1
            for i in range(number_node):
                if next.next is None:
                    break
                next = next.next
                count += 1
            if count * size <= index:
                new_node = Node()
                next.next = new_node
                new_node.put_in(0, data)
            else:
                if next.next is None:
                    if next.fill == size:
                        new_node = Node()
                        next.next = new_node
                        new_node.put_in(0, data)
                    else:
                        next.put_in(ind, data)
                else:
                    if next.fill == size:
                        new_node = Node()
                        mid = size // 2
                        if size % 2 != 0:
                            mid += 1
                        new_node.next = next.next
                        next.next = new_node
                        new_node.arr[:mid] = next.arr[mid:]
                        new_node.fill = mid
                        next.arr[mid:] = [None for i in range(mid)]
                        next.fill -= mid
                        if ind < mid:
                            next.put_in(ind, data)
                        else:
                            ind -= mid
                            new_node.put_in(ind, data)
                    else:
                        next.put_in(ind, data)
        else:
            node = Node()
            node.put_in(index, data)
            self.head = node

    def delete(self, index: int) -> None:
        if self.head is not None:
            number_node = index // size
            ind = index % size
            next = self.head
            for i in range(number_node):
                if next.next is None:
                    break
                next = next.next
            if next is not None and next.arr[ind] is not None:
                mid = size // 2
                if size % 2 != 0:
                    mid += 1
                if next.fill - 1 < mid:
                    next_next = next.next
                    if next_next is not None:
                        if next_next.fill - 1 < mid:
                            next.take_out(ind)
                            next.next = next_next.next
                            next_next.next = None
                            next.arr[next.fill:(next.fill + next_next.fill + 1)] = next_next.arr[:next_next.fill + 1]
                        else:
                            elem = next_next.arr[0]
                            next_next.take_out(0)
                            next.take_out(ind)
                            next.put_in(next.fill, elem)
                    else:
                        next.take_out(ind)
                else:
                    next.take_out(index)

    def __str__(self) -> str:
        if self.head is not None:
            res = "["
            next = self.head
            while next.next is not None:
                res = res + f"{next}, \n"
                next = next.next
            res = res + f"{next}]"
            return res
        return "[]"

def main():
    ull = UnrolledLinkedList()
    for i in range(9):
        ull.insert(i, i + 1)
    print(ull)
    print()
    print(ull.get(4))
    print()
    ull.insert(1, 10)
    print(ull)
    print()
    ull.insert(8, 11)
    print(ull)
    print()
    ull.delete(1)
    print(ull)
    ull.delete(2)
    print()
    print(ull)


if __name__ == "__main__":
    main()


