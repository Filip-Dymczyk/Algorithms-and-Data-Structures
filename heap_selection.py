from typing import Optional, List, Union
from random import randint
import time


class Elem:
    def __init__(self, data, priority) -> None:
        self.__data = data
        self.__priority = priority

    def __gt__(self, other) -> bool:
        return self.__priority > other.__priority

    def __lt__(self, other) -> bool:
        return self.__priority < other.__priority

    def __repr__(self) -> str:
        return f"{self.__priority}: {self.__data}"


class Heap:
    def __init__(self, tab: List[Union[Elem, float]] = None) -> None:
        self.tab = tab if tab else []
        self.heap_size = len(tab) if tab else 0

        if tab:
            par = self.__parent(self.heap_size - 1)
            for idx in range(par, -1, -1):
                self.fix_heap(idx)

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


def selection_sort_swap(data: List[Union[Elem, float]]) -> None:
    if data:
        n = len(data)
        for i in range(n):
            min_index = i
            for j in range(i + 1, n):
                if data[j] < data[min_index]:
                    min_index = j
            if min_index != i:
                data[i], data[min_index] = data[min_index], data[i]


def selection_sort_shift(data: List[Union[Elem, float]]) -> None:
    if data:
        n = len(data)
        for i in range(n):
            min_index = i
            for j in range(i + 1, n):
                if data[j] < data[min_index]:
                    min_index = j
            if min_index != i:
                data.insert(i, data[min_index])
                data.pop(min_index + 1)


def main():

    l = [(5, 'A'), (5, 'B'), (7, 'C'), (2, 'D'), (5, 'E'), (1, 'F'), (7, 'G'), (5, 'H'), (1, 'I'), (2, 'J')]
    to_sort_heap = []
    to_sort_selection_swap = []
    to_sort_selection_shift = []

    for t in l:
        to_sort_heap.append(Elem(t[1], t[0]))
        to_sort_selection_swap.append(Elem(t[1], t[0]))
        to_sort_selection_shift.append(Elem(t[1], t[0]))

    h1 = Heap(to_sort_heap)
    h1.print_tab()
    h1.print_tree(0, 0)

    for i in range(len(h1.tab)):
        h1.dequeue()
    print()

    selection_sort_swap(to_sort_selection_swap)
    selection_sort_shift(to_sort_selection_shift)

    print("Heap sort: " + str(to_sort_heap))
    print("Selection sort swap: " + str(to_sort_selection_swap))
    print("Both algorithms aren't stable.")
    print()
    print("Selection sort shift: " + str(to_sort_selection_shift))
    print("Selection sort with shift is stable")

    rand_heap = [randint(0, 100) for _ in range(10000)]
    rand_selection_swap = [randint(0, 100) for _ in range(10000)]
    rand_selection_shift = [randint(0, 100) for _ in range(10000)]

    t_start_heap = time.perf_counter()
    h2 = Heap(rand_heap)
    for i in range(len(h2.tab)):
        h2.dequeue()
    print()
    t_stop_heap = time.perf_counter()

    t_start_selection_swap = time.perf_counter()
    selection_sort_swap(rand_selection_swap)
    t_stop_selection_swap = time.perf_counter()

    t_start_selection_shift = time.perf_counter()
    selection_sort_shift(rand_selection_shift)
    t_stop_selection_shift = time.perf_counter()

    print("Calculations time for heap sort:", "{:.7f}".format(t_stop_heap - t_start_heap))
    print("Calculations time for selection sort swap:", "{:.7f}".format(t_stop_selection_swap - t_start_selection_swap))
    print("Calculations time for selection sort shift:", "{:.7f}".format(t_stop_selection_shift - t_start_selection_shift))


if __name__ == '__main__':
    main()

