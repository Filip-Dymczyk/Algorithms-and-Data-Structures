from typing import Optional
from copy import deepcopy
from timeit import timeit

class Matrix:
    def __init__(self, data: Optional[tuple], const: float = 0) -> None:
        if isinstance(data, tuple):
            r = data[0]
            c = data[1]
            self.__matrix = [[const] * c for i in range(r)]
        else:
            self.__matrix = data

    def size(self) -> tuple:
        r = len(self.__matrix)
        c = len(self.__matrix[0])
        return r, c

    def __getitem__(self, item: int) -> float:
        return self.__matrix[item]

    def __add__(self, other):
        if other is not None and self.size() == other.size():
            r, c = self.size()
            res = Matrix(data=(r, c))
            for i in range(r):
                for j in range(c):
                    res[i][j] = self.__matrix[i][j] + other[i][j]
            return res
        return None

    def __mul__(self, other):
        if other is not None:
            r1, c1 = self.size()
            r2, c2 = other.size()
            if c1 == r2:
                res = Matrix(data=(r1, c2))
                for i in range(r1):
                    for j in range(c2):
                        for k in range(c1):
                            res[i][j] += self.__matrix[i][k] * other[k][j]
                return res
        return None

    def __str__(self) -> str:
        res = ""
        r, c = self.size()
        for i in range(r):
            res += "|"
            for j in range(c):
                res += str(self.__matrix[i][j])
                if not j == c - 1:
                    res += " "
            res += "|\n"
        return res


def transpose(m: Matrix) -> Optional[Matrix]:
    if m is not None:
        r, c = m.size()
        res = Matrix((c, r))
        for i in range(r):
            for j in range(c):
                res[j][i] = m[i][j]
        return res
    return m


def chio_det(m: Matrix) -> Optional[float]:
    if m is not None and m.size()[0] == m.size()[1]:
        counter_r, _ = m.size()
        copy = deepcopy(m)
        det = 1
        while counter_r > 2:
            if copy[0][0] == 0:
                for m in range(1, counter_r):
                    if copy[m][0] != 0:
                        copy[0][:], copy[m][:] = copy[m][:], copy[0][:]
                        det *= -1
                        break
            a11 = copy[0][0]
            temp_matrix = deepcopy(copy)
            for j in range(1, counter_r):
                for k in range(1, counter_r):
                    det_jk = a11 * temp_matrix[j][k] - temp_matrix[j][0] * temp_matrix[0][k]
                    copy[j - 1][k - 1] = det_jk
            det *= 1/(a11**(counter_r - 2))
            counter_r -= 1
        det *= copy[0][0] * copy[1][1] - copy[1][0] * copy[0][1]
        return det
    return None

def main():
    m2 = Matrix(data=(2, 3))
    m4 = Matrix(data=[[5, 1, 1, 2, 3], [4, 2, 1, 7, 3], [2, 1, 2, 4, 7], [9, 1, 0, 7, 0], [1, 4, 7, 2, 2]])
    m5 = Matrix(data=[[0, 1, 1, 2, 3], [4, 2, 1, 7, 3], [2, 1, 2, 4, 7], [9, 1, 0, 7, 0], [1, 4, 7, 2, 2]])
    m6 = Matrix(data=[[0, 2, 3, 4], [0, 2, 1, 7], [5, 43, 32, 2], [67, 2, 2, 3]])
    print(m2)
    print(m4)
    print(chio_det(m4))
    print(chio_det(m5))
    print(chio_det(m6))

if __name__ == "__main__":
    main()

