from typing import Optional


class Elem:
    def __init__(self, data, next) -> None:
        self.data = data
        self.next = next

    def __str__(self) -> str:
        return str(self.data)


class LinkedList:
    def __init__(self) -> None:
        self.__head = None

    def destroy(self) -> None:
        self.__head = None

    def add(self, data: Elem) -> None:
        elem = Elem(data, self.__head)
        self.__head = elem

    def append(self, data: Elem) -> None:
        if not self.is_empty():
            temp = self.__head
            while temp.next is not None:
                temp = temp.next
            else:
                elem = Elem(data, None)
                temp.next = elem
        else:
            self.__head = Elem(data, None)

    def remove(self) -> None:
        if not self.is_empty():
            next_elem = self.__head.next
            self.__head = None
            self.__head = next_elem

    def remove_end(self) -> None:
        if not self.is_empty():
            if self.length() != 1:
                temp = self.__head
                pre_temp = self.__head
                while temp.next is not None:
                    pre_temp = temp
                    temp = temp.next
                pre_temp.next = None
            else:
                self.remove()

    def is_empty(self) -> bool:
        return self.__head is None

    def length(self) -> int:
        size = 0
        temp = self.__head
        while temp is not None:
            temp = temp.next
            size += 1
        return size

    def get(self):
        if not self.is_empty():
            return self.__head.data
        return None

    def __str__(self) -> Optional[str]:
        res = ""
        if not self.is_empty():
            temp = self.__head
            while temp is not None:
                res = res + "-> " + str(temp) + "\n"
                temp = temp.next
        return res

def main():
    test_data = [('AGH', 'Cracow', 1919),
         ('UJ', 'Cracow', 1364),
         ('PW', 'Warsaw', 1915),
         ('UW', 'Warsaw', 1915),
         ('UP', 'Poznan', 1919),
         ('PG', 'Gdansk', 1945)]

    universities = LinkedList()

    for i in range(3):
        universities.append(test_data[i])

    for i in range(3, len(test_data)):
        universities.add(test_data[i])

    print(universities)
    print(universities.length())

    universities.remove()

    print(universities.get())

    universities.remove_end()

    print(universities)

    universities.destroy()

    print(universities.is_empty())

    universities.remove()
    universities.append(test_data[0])
    universities.remove_end()
    print(universities)


if __name__ == "__main__":
    main()


