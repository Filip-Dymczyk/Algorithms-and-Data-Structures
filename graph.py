import polska
from typing import List, Tuple
from abc import ABC, abstractmethod


class Vertex:
    def __init__(self, key: str, data: str = None) -> None:
        self.key = key
        self.data = data

    def __eq__(self, other) -> bool:
        return self.key == other.key

    def __hash__(self) -> int:
        return hash(self.key)


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

    def insert_edge(self, vertex1: Vertex, vertex2: Vertex, edge: int=1) -> None:
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


class GraphList(Graph):
    def __init__(self) -> None:
        self.adj_list = {}
        self.list_vertex = []
        self.map_vertex = {}

    def is_empty(self) -> bool:
        return not self.list_vertex

    def size(self) -> int:
        if self.is_empty():
            return 0
        return len(self.list_vertex)

    def insert_vertex(self, vertex: Vertex) -> None:
        if vertex not in self.adj_list:
            self.adj_list[vertex] = {}
            self.list_vertex.append(vertex)
            self.map_vertex[vertex] = self.size() - 1

    def insert_edge(self, vertex1: Vertex, vertex2: Vertex, edge: int = 1) -> None:
        if vertex1 not in self.adj_list:
            self.insert_vertex(vertex1)
        if vertex2 not in self.adj_list:
            self.insert_vertex(vertex2)

        self.adj_list[vertex1][vertex2] = edge
        self.adj_list[vertex2][vertex1] = edge

    def delete_vertex(self, vertex: Vertex) -> None:
        if vertex in self.adj_list:
            ind = self.map_vertex[vertex]
            del self.adj_list[vertex]
            del self.map_vertex[vertex]
            del self.list_vertex[ind]
            for v, i in self.map_vertex.items():
                if i > ind:
                    self.map_vertex[v] -= 1
            for current_vertex, neighs in self.adj_list.items():
                if vertex in neighs:
                    del self.adj_list[current_vertex][vertex]

    def delete_edge(self, vertex1: Vertex, vertex2: Vertex) -> None:
        if vertex1 in self.adj_list and vertex2 in self.adj_list:
            if vertex1 in self.adj_list[vertex2] and vertex2 in self.adj_list[vertex1]:
                del self.adj_list[vertex1][vertex2]
                del self.adj_list[vertex2][vertex1]

    def edges(self) -> List[Tuple[Vertex, Vertex]]:
        if not self.is_empty():
            l = []
            for current_vertex, neighs in self.adj_list.items():
                for neighbour_vertex in neighs:
                    tup = (current_vertex.key, neighbour_vertex.key)
                    l.append(tup)
            return l


def main():
    graph_matrix = GraphMatrix()
    graph_list = GraphList()

    for tup in polska.graf:
        vertex1 = Vertex(tup[0])
        vertex2 = Vertex(tup[1])
        graph_matrix.insert_edge(vertex1, vertex2)
        graph_list.insert_edge(vertex1, vertex2)

    graph_matrix.delete_vertex(Vertex('K'))
    graph_list.delete_vertex(Vertex('K'))

    graph_matrix.delete_edge(Vertex('W'), Vertex('E'))
    graph_list.delete_edge(Vertex('W'), Vertex('E'))

    polska.draw_map(graph_list.edges())
    polska.draw_map(graph_matrix.edges())


if __name__ == '__main__':
    main()
