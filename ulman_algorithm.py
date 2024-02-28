from typing import List, Tuple
from abc import ABC, abstractmethod
import numpy as np
from copy import deepcopy


class Vertex:
    def __init__(self, key: str, data: str = None) -> None:
        self.key = key
        self.data = data

    def __eq__(self, other) -> bool:
        return self.key == other.key

    def __hash__(self) -> int:
        return hash(self.key)

    def __repr__(self) -> str:
        return f"{self.key}"


class Graph(ABC):
    @abstractmethod
    def is_empty(self) -> bool:
        pass

    @abstractmethod
    def size(self) -> int:
        pass

    @abstractmethod
    def insert_vertex(self, vertex: Vertex) -> None:
        pass

    @abstractmethod
    def insert_edge(self, vertex1: Vertex, vertex2: Vertex, edge: int = 1) -> None:
        pass

    @abstractmethod
    def delete_vertex(self, vertex: Vertex) -> None:
        pass

    @abstractmethod
    def delete_edge(self, vertex1: Vertex, vertex2: Vertex) -> None:
        pass

    @abstractmethod
    def edges(self) -> List[Tuple[Vertex, Vertex]]:
        pass


class GraphMatrix(Graph):
    def __init__(self) -> None:
        self.matrix = None
        self.list_vertex = None
        self.map_vertex = {}

    def is_empty(self) -> bool:
        return not self.matrix

    def size(self) -> int:
        if self.is_empty():
            return 0
        return len(self.list_vertex)

    def insert_vertex(self, vertex: Vertex) -> None:
        if self.is_empty():
            self.list_vertex = [vertex]
            self.matrix = [[0]]
            self.map_vertex[vertex] = 0
        else:
            if vertex not in self.map_vertex:
                size = self.size()
                for vec in self.matrix:
                    vec.append(0)
                self.list_vertex.append(vertex)
                self.map_vertex[vertex] = size
                new_vec = [[0 for _ in range(size + 1)]]
                self.matrix += new_vec

    def insert_edge(self, vertex1: Vertex, vertex2: Vertex, edge: int = 1) -> None:
        if vertex1 not in self.map_vertex:
            self.insert_vertex(vertex1)
        if vertex2 not in self.map_vertex:
            self.insert_vertex(vertex2)

        ind1 = self.map_vertex[vertex1]
        ind2 = self.map_vertex[vertex2]
        self.matrix[ind1][ind2] = edge
        self.matrix[ind2][ind1] = edge

    def delete_vertex(self, vertex: Vertex) -> None:
        if vertex in self.map_vertex:
            ind = self.map_vertex[vertex]
            del self.list_vertex[ind]
            del self.map_vertex[vertex]
            for ver, i in self.map_vertex.items():
                if ind < i:
                    self.map_vertex[ver] -= 1
            del self.matrix[ind]
            for vec in self.matrix:
                del vec[ind]

    def delete_edge(self, vertex1: Vertex, vertex2: Vertex) -> None:
        if vertex1 in self.map_vertex and vertex2 in self.map_vertex:
            ind1 = self.map_vertex[vertex1]
            ind2 = self.map_vertex[vertex2]
            if self.matrix[ind1][ind2] > 0:
                self.matrix[ind1][ind2] -= 1
                self.matrix[ind2][ind1] -= 1

    def edges(self) -> List[Tuple[Vertex, Vertex]]:
        if not self.is_empty():
            l = []
            for i in range(self.size()):
                for j in range(self.size()):
                    if i != j and self.matrix[i][j] > 0:
                        tup = self.list_vertex[i].key, self.list_vertex[j].key
                        l.append(tup)
            return l


def ulman1(G: Graph, P: Graph) -> None:
    G_matrix = np.array(G.matrix)
    P_matrix = np.array(P.matrix)
    M = np.zeros((P.size(), G.size()))
    used_columns = np.array([False for _ in range(M.shape[1])])
    res = []
    global rec_count
    rec_count = 0

    def in_ulman(curr_row: int, M_in: np.ndarray) -> None:
        global rec_count
        if curr_row == M_in.shape[0]:
            if (P_matrix == M_in @ (M_in @ G_matrix).T).all():
                res.append(deepcopy(M_in))
            return
        for c_idx, c in enumerate(M_in[curr_row]):
            if not used_columns[c_idx]:
                used_columns[c_idx] = True
                M_in[curr_row] = np.zeros((1, M_in.shape[1]))
                M_in[curr_row, c_idx] = 1
                rec_count += 1
                in_ulman(curr_row + 1, M_in)
                used_columns[c_idx] = False

    in_ulman(0, M)
    print("Recursion calls: " + str(rec_count), end=', ')
    print("Isomorphisms count: " + str(len(res)))


def ulman2(G: Graph, P: Graph) -> None:
    G_matrix = np.array(G.matrix)
    P_matrix = np.array(P.matrix)
    M = np.zeros((P.size(), G.size()))
    M0 = np.zeros((P.size(), G.size()))
    for i in range(P.size()):
        for j in range(G.size()):
            if np.sum(P_matrix[i]) <= np.sum(G_matrix[j]):
                M0[i, j] = 1

    used_columns = np.array([False for _ in range(M0.shape[1])])
    res = []
    global rec_count
    rec_count = 0

    def in_ulman(curr_row: int, M_in: np.ndarray) -> None:
        global rec_count
        if curr_row == M_in.shape[0]:
            if (P_matrix == M_in @ (M_in @ G_matrix).T).all():
                res.append(deepcopy(M_in))
            return
        for c_idx, c in enumerate(M_in[curr_row]):
            if M0[curr_row, c_idx] == 1 and not used_columns[c_idx]:
                used_columns[c_idx] = True
                M_in[curr_row] = np.zeros((1, M_in.shape[1]))
                M_in[curr_row, c_idx] = 1
                rec_count += 1
                in_ulman(curr_row + 1, M_in)
                used_columns[c_idx] = False

    in_ulman(0, M)
    print("Recursion calls: " + str(rec_count), end=', ')
    print("Isomorphisms count: " + str(len(res)))


def ulman3(G: Graph, P: Graph) -> None:
    G_matrix = np.array(G.matrix)
    P_matrix = np.array(P.matrix)
    M = np.zeros((P.size(), G.size()))
    M0 = np.zeros((P.size(), G.size()))
    for i in range(P.size()):
        for j in range(G.size()):
            if np.sum(P_matrix[i]) <= np.sum(G_matrix[j]):
                M0[i, j] = 1

    used_columns = np.array([False for _ in range(M.shape[1])])
    res = []
    global rec_count
    rec_count = 0

    def prune(M_p: np.ndarray) -> bool:
        for i in range(M_p.shape[0]):
            for j in range(M_p.shape[1]):
                if M_p[i, j] == 1:
                    cant_be_iso = True
                    for x_idx in range(P_matrix.shape[0]):
                        if x_idx != i and P_matrix[i, x_idx] > 0:
                            for y_idx in range(G_matrix.shape[0]):
                                if y_idx != j and G_matrix[j, y_idx] > 0 and M_p[x_idx, y_idx] == 1:
                                    cant_be_iso = False
                                    break
                    if cant_be_iso:
                        M_p[i, j] = 0
                        return cant_be_iso
        return False

    def in_ulman(curr_row: int, M_in: np.ndarray) -> None:
        global rec_count
        if curr_row == M_in.shape[0]:
            if (P_matrix == M_in @ (M_in @ G_matrix).T).all():
                res.append(deepcopy(M_in))
            return
        M_copy = deepcopy(M_in)
        cant_be_iso = False
        if curr_row == len(M_in) - 1:
            cant_be_iso = prune(M_copy)
        for c_idx, c in enumerate(M_copy[curr_row]):
            if cant_be_iso:
                break
            if M0[curr_row, c_idx] == 1 and not used_columns[c_idx]:
                used_columns[c_idx] = True
                M_copy[curr_row] = np.zeros((1, M_copy.shape[1]))
                M_copy[curr_row, c_idx] = 1
                rec_count += 1
                in_ulman(curr_row + 1, M_copy)
                used_columns[c_idx] = False

    in_ulman(0, M)
    print("Recursion calls: " + str(rec_count), end=', ')
    print("Isomorphisms count: " + str(len(res)))


def main():
    graph_G = [('A', 'B', 1), ('B', 'F', 1), ('B', 'C', 1), ('C', 'D', 1), ('C', 'E', 1), ('D', 'E', 1)]
    graph_P = [('A', 'B', 1), ('B', 'C', 1), ('A', 'C', 1)]
    G = GraphMatrix()
    P = GraphMatrix()
    for t in graph_G:
        G.insert_edge(Vertex(t[0]), Vertex(t[1]), t[2])
    for t in graph_P:
        P.insert_edge(Vertex(t[0]), Vertex(t[1]), t[2])
    ulman1(G, P)
    ulman2(G, P)
    ulman3(G, P)


if __name__ == '__main__':
    main()
