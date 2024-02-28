from typing import Optional


class Elem:
    def __init__(self, key, value) -> None:
        self.key = key
        self.value = value


class HashList:
    def __init__(self, size: int, c1=1, c2=0) -> None:
        self.__arr = [None for i in range(size)]
        self.__c1 = c1
        self.__c2 = c2

    def length(self) -> int:
        return len(self.__arr)

    def __hash(self, key) -> int:
        if isinstance(key, str):
            new_key = 0
            for letter in key:
                new_key += ord(letter)
            key = new_key
        return key % self.length()

    def search(self, key) -> Optional[float]:
        hash_key = self.__hash(key)
        if self.__arr[hash_key] == 'TS':
            i = 1
            f_key = self.__hash(hash_key + self.__c1 * i + self.__c2 * i ** 2)
            if self.__arr[f_key] is None:
                return None
            elif self.__arr[f_key].key == key:
                return self.__arr[f_key].value
            while True:
                i += 1
                new_key = self.__hash(hash_key + self.__c1 * i + self.__c2 * i ** 2)
                if new_key == f_key:
                    break
                if self.__arr[new_key] is None:
                    break
                elif self.__arr[new_key].key == key:
                    return self.__arr[new_key].value
        elif self.__arr[hash_key] is not None and self.__arr[hash_key].key == key:
            return self.__arr[hash_key].value
        return None

    def __solve_collision(self, key, value) -> bool:
        i = 1
        hash_key = self.__hash(key)
        f_key = self.__hash(hash_key + self.__c1 * i + self.__c2 * i ** 2)
        flag = True
        if self.__arr[f_key] is None or self.__arr == 'TS':
            self.__arr[f_key] = Elem(key, value)
            return flag
        else:
            if self.__arr[f_key].key == key:
                self.__arr[f_key].value = value
                return flag
        while True:
            i += 1
            new_key = self.__hash(hash_key + self.__c1 * i + self.__c2 * i ** 2)
            if new_key == f_key:
                flag = False
                break
            if self.__arr[new_key] is None or self.__arr[new_key] == 'TS':
                self.__arr[new_key] = Elem(key, value)
                break
            else:
                if self.__arr[new_key].key == key:
                    self.__arr[new_key].value = value
                    break
        return flag

    def insert(self, key, value) -> None:
        hash_key = self.__hash(key)
        flag = True
        if self.__arr[hash_key] is not None and self.__arr[hash_key] != 'TS':
            if self.__arr[hash_key].key != key:
                flag = self.__solve_collision(key, value)
            else:
                self.__arr[hash_key].value = value
        else:
            self.__arr[hash_key] = Elem(key, value)
        if not flag:
            print("No space for elem of key: " + str(key))

    def remove(self, key) -> None:
        hash_key = self.__hash(key)
        flag = False
        if self.__arr[hash_key] is not None:
            if self.__arr[hash_key] == 'TS' or self.__arr[hash_key].key != key:
                i = 1
                f_key = self.__hash(hash_key + self.__c1 * i + self.__c2 * i ** 2)
                if self.__arr[f_key] is not None and self.__arr[f_key].key == key:
                    self.__arr[f_key] = 'TS'
                    flag = True
                while not flag:
                    i += 1
                    new_key = self.__hash(hash_key + self.__c1 * i + self.__c2 * i ** 2)
                    if new_key == f_key:
                        break
                    if self.__arr[new_key].key == key:
                        self.__arr[new_key] = 'TS'
                        flag = True
            else:
                self.__arr[hash_key] = 'TS'
                flag = True
        if not flag:
            print("No elem of key: " + str(key))

    def __str__(self) -> str:
        res = "{"
        for i in range(self.length()):
            elem = self.__arr[i]
            if elem is not None and elem != 'TS':
                res += f"{elem.key}: {elem.value}"
            else:
                res += "None"
            if i != self.length() - 1:
                res += ", "
        res += "}"
        return res


def test1(size: int = 13, c1=1, c2=0) -> None:
    hash_list = HashList(size, c1, c2)
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
    for i in range(15):
        if i + 1 == 6:
            hash_list.insert(18, letters[i])
        elif i + 1 == 7:
            hash_list.insert(31, letters[i])
        else:
            hash_list.insert(i + 1, letters[i])
    print(hash_list)
    print(hash_list.search(5))
    print(hash_list.search(14))
    hash_list.insert(5, 'Z')
    print(hash_list.search(5))
    hash_list.remove(5)
    print(hash_list)
    print(hash_list.search(31))
    hash_list.insert('test', 'W')
    print(hash_list)


def test2(size: int = 13, c1=1, c2=0) -> None:
    hash_list = HashList(size, c1, c2)
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
    for i in range(15):
        hash_list.insert((i + 1) * 13, letters[i])
    print(hash_list)

def main():
    test1()
    print()
    test2()
    print()
    test2(c1=0, c2=1)
    print()
    test1(c1=0, c2=1)


if __name__ == "__main__":
    main()

