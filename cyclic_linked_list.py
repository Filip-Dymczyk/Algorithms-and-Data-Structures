from typing import Optional


class Elem:
    def __init__(self, data, next, prev) -> None:
        self.data = data
        self.next = next
        self.prev = prev

    def __str__(self) -> str:
        return str(self.data)


class LinkedList:
    def __init__(self) -> None:
        self.__head = None
        self.__tail = None

    def destroy(self) -> None:
        self.__head = None
        self.__tail = None

    def add(self, data: Elem) -> None:
        if not self.is_empty():
            elem = Elem(data, self.__head, None)
            self.__head.prev = elem
            self.__head = elem
        else:
            self.__head = Elem(data, None, None)
            self.__tail = self.__head

    def append(self, data: Elem) -> None:
        if not self.is_empty():
            elem = Elem(data, None, self.__tail)
            self.__tail.next = elem
            self.__tail = elem
        else:
            self.add(data)

    def remove(self) -> None:
        if not self.is_empty() and self.length() > 1:
            next = self.__head.next
            next.prev = None
            self.__head = next
        elif self.length() == 1:
            self.__head = None
            self.__tail = self.__head

    def remove_end(self) -> None:
        if not self.is_empty() and self.length() > 1:
            prev = self.__tail.prev
            prev.next = None
            self.__tail = prev
        elif self.length() == 1:
            self.remove()

    def is_empty(self) -> bool:
        return self.__head is None and self.__tail is None

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
    test_data = [('AGH', 'Kraków', 1919),
         ('UJ', 'Kraków', 1364),
         ('PW', 'Warszawa', 1915),
         ('UW', 'Warszawa', 1915),
         ('UP', 'Poznań', 1919),
         ('PG', 'Gdańsk', 1945)]
    
    universities = LinkedList()
    for e in test_data:
        universities.append(e)
    print(universities)
    universities.destroy()
    print(universities.is_empty())
    universities.append(test_data[0])
    print(universities)
    universities.add(test_data[1])
    print(universities)


if __name__ == "__main__":
    main()




