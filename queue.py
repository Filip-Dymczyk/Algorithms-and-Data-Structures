from typing import Optional


class Queue:
    def __init__(self) -> None:
        self.__size = 5
        self.tab = [None for i in range(self.__size)]
        self.__read = 0
        self.__write = self.__read

    def is_empty(self) -> bool:
        return self.__read == self.__write

    def peek(self) -> Optional[float]:
        if not self.is_empty():
            return self.tab[self.__read]
        return None

    def dequeue(self) -> Optional[float]:
        if not self.is_empty():
            read = self.tab[self.__read]
            self.tab[self.__read] = None
            self.__read += 1
            if self.__read == self.__size:
                self.__read = 0
            return read
        return None

    def __realloc(self) -> None:
        old_size = self.__size
        self.__size *= 2
        tab = [None for i in range(self.__size)]
        tab[self.__size - (old_size - self.__write):] = self.tab[self.__write:old_size]
        tab[:self.__write] = self.tab[:self.__write]
        self.tab = tab
        self.__read = self.__size - (old_size - self.__write)

    def enqueue(self, data) -> None:
        if not self.is_empty():
            self.tab[self.__write] = data
            self.__write += 1
            if self.is_empty():
                self.__realloc()
            else:
                if self.__write == self.__size:
                    self.__write = 0
                    if self.is_empty():
                        self.__realloc()
        else:
            self.tab[self.__read] = data
            self.__write += 1

    def __str__(self) -> str:
        if not self.is_empty():
            res = "["
            read = self.__read
            while read != self.__write:
                if read == self.__size:
                    read = 0
                    continue
                if read != self.__read:
                    res += ", "
                res += str(self.tab[read])
                read += 1
            res += "]"
            return res
        return "[]"

def main():
    q1 = Queue()

    for i in range(4):
        q1.enqueue(i + 1)

    print(q1.dequeue())
    print(q1.peek())
    print(q1)

    for i in range(5, 9):
        q1.enqueue(i)

    print(q1.tab)

    while q1.peek() is not None:
        print(q1.dequeue())
    print(q1)


if __name__ == "__main__":
    main()
