from typing import Optional


class Elem:
    def __init__(self, data, priority) -> None:
        self.__data = data
        self.__priority = priority

    def __gt__(self, other) -> bool:
        return self.__priority > other.__priority

    def __lt__(self, other) -> bool:
        return self.__priority < other.__priority

    def __str__(self) -> str:
        return f"{self.__priority}: {self.__data}"


class Heap:
    def __init__(self) -> None:
        self.tab = []
        self.heap_size = 0

    def is_empty(self) -> bool:
        return self.heap_size == 0

    def __parent(self, ind: int) -> int:
        if ind > 0:
            return (ind - 1) // 2
        return ind

    def __left(self, ind: int) -> int:
        return 2 * ind + 1

    def __right(self, ind: int) -> int:
        return 2 * ind + 2

    def fix_heap(self, ind: int) -> None:
        while self.__left(ind) < self.heap_size:
            left_i = self.__left(ind)
            right_i = self.__right(ind)
            left_ch = self.tab[left_i]
            right_ch = left_ch
            if right_i < self.heap_size:
                right_ch = self.tab[right_i]
            par = self.tab[ind]
            if right_ch > left_ch:
                if par < right_ch:
                    self.tab[ind], self.tab[right_i] = self.tab[right_i], self.tab[ind]
                    ind = right_i
                else:
                    break
            else:
                if par < left_ch:
                    self.tab[ind], self.tab[left_i] = self.tab[left_i], self.tab[ind]
                    ind = left_i
                else:
                    break

    def peek(self) -> Optional[Elem]:
        if not self.is_empty():
            return self.tab[0]
        return None

    def dequeue(self) -> Optional[Elem]:
        if not self.is_empty():
            first = self.tab[0]
            self.tab[0], self.tab[self.heap_size - 1] = self.tab[self.heap_size - 1], self.tab[0]
            self.heap_size -= 1
            ind = 0
            self.fix_heap(ind)
            return first
        return None

    def enqueue(self, elem: Elem) -> None:
        if self.heap_size == len(self.tab):
            self.tab.append(elem)
        else:
            self.tab[self.heap_size] = elem
        self.heap_size += 1
        ind = self.heap_size - 1
        while self.tab[ind] > self.tab[self.__parent(ind)]:
            self.tab[ind], self.tab[self.__parent(ind)] = self.tab[self.__parent(ind)], self.tab[ind]
            ind = self.__parent(ind)

    def print_tab(self):
        print('{', end='')
        print(*self.tab[:self.heap_size], sep=', ', end='')
        print('}')

    def print_tree(self, idx, lvl):
        if idx < len(self.tab):
            self.print_tree(self.__right(idx), lvl + 1)
            print(2 * lvl * '  ', self.tab[idx] if self.tab[idx] else None)
            self.print_tree(self.__left(idx), lvl + 1)

def main():
    heap = Heap()

    l = [7, 5, 1, 2, 5, 3, 4, 8, 9]
    values = "GRYMOTYLA"

    for i in range(len(l)):
        heap.enqueue(Elem(values[i], l[i]))

    heap.print_tree(0, 0)
    print()
    heap.print_tab()
    rem = heap.dequeue()
    print(heap.peek())
    heap.print_tab()
    print(rem)
    print()
    while heap.heap_size > 0:
        print(heap.dequeue())
    heap.print_tab()


if __name__ == "__main__":
    main()

