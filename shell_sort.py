import time
from random import randint
from typing import List, Union, Optional


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


def insertion_sort(data: List[Union[Elem, float]]) -> None:
    for i in range(1, len(data)):
        to_check = data[i]
        set_ind = i
        for j in range(i - 1, -1, -1):
            if data[j] > to_check:
                data[j + 1] = data[j]
                set_ind = j
        data[set_ind] = to_check


def shell_sort_first(data: List[Union[Elem, float]]) -> None:
    h = len(data) // 2
    while h:
        for i in range(h, len(data)):
            set_ind = i
            to_check = data[i]
            for j in range(i - h, -1, -h):
                if data[j] > to_check:
                    data[j + h] = data[j]
                    set_ind = j
            data[set_ind] = to_check
        h //= 2


def shell_sort_second(data: List[Union[Elem, float]]) -> None:
    h = 0
    k = 1
    while h < len(data) // 3:
        h = (3**k - 1) // 2
        k += 1
    while h:
        for i in range(h, len(data)):
            set_ind = i
            to_check = data[i]
            for j in range(i - h, -1, -h):
                if data[j] > to_check:
                    data[j + h] = data[j]
                    set_ind = j
            data[set_ind] = to_check
        h //= 3


def main():

    l = [(5, 'A'), (5, 'B'), (7, 'C'), (2, 'D'), (5, 'E'), (1, 'F'), (7, 'G'), (5, 'H'), (1, 'I'), (2, 'J')]
    to_sort_insertion = []
    to_sort_shell_first = []
    to_sort_shell_second = []
    to_sort_heap = []
    for t in l:
        to_sort_insertion.append(Elem(t[1], t[0]))
        to_sort_shell_first.append(Elem(t[1], t[0]))
        to_sort_shell_second.append((Elem(t[1], t[0])))
        to_sort_heap.append(Elem(t[1], t[0]))

    print("Pre sorting:" + str(to_sort_shell_first))
    print()

    shell_sort_first(to_sort_shell_first)
    shell_sort_second(to_sort_shell_second)
    insertion_sort(to_sort_insertion)

    print("Insertion sort: " + str(to_sort_insertion))
    print("Shell sort first: " + str(to_sort_shell_first))
    print("Shell sort second: " + str(to_sort_shell_second))
    print("Jak widać, stabilny jest tylko algorytm insertion sort")

    rand_insertion = [randint(0, 100) for _ in range(10000)]
    rand_shell_first = [randint(0, 100) for _ in range(10000)]
    rand_shell_second = [randint(0, 100) for _ in range(10000)]
    rand_heap = [randint(0, 100) for _ in range(10000)]

    t_start_insertion = time.perf_counter()
    insertion_sort(rand_insertion)
    t_stop_insertion = time.perf_counter()

    t_start_shell_first = time.perf_counter()
    shell_sort_first(rand_shell_first)
    t_stop_shell_first = time.perf_counter()

    t_start_shell_second = time.perf_counter()
    shell_sort_second(rand_shell_second)
    t_stop_shell_second = time.perf_counter()

    t_start_heap = time.perf_counter()
    h = Heap(rand_heap)
    for i in range(len(h.tab)):
        h.dequeue()
    print()
    t_stop_heap = time.perf_counter()

    print("Czas obliczeń dla insertion sort:", "{:.7f}".format(t_stop_insertion - t_start_insertion))
    print("Czas obliczeń dla shell sort first:", "{:.7f}".format(t_stop_shell_first - t_start_shell_first))
    print("Czas obliczeń dla shell sort second:", "{:.7f}".format(t_stop_shell_second - t_start_shell_second))
    print("Czas obliczeń dla heap sort:", "{:.7f}".format(t_stop_heap - t_start_heap))


if __name__ == '__main__':
    main()
