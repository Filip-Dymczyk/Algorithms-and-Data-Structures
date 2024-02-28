import polska
from typing import List, Tuple, Set
from abc import ABC, abstractmethod


class Vertex:
    def __init__(self, key: str, data: str = None) -> None:
        self.key = key
        self.data = data
        self.col = -1

    def __eq__(self, other) -> bool:
        return self.key == other.key

    def __hash__(self) -> int:
        return hash(self.key)

    def __repr__(self) -> str:
        return f"{self.key}: {self.data} " + f"col: {self.col}" if self.col > 0 else ""

    def __str__(self) -> str:
        return f"{self.key}: {self.data} " + f"col: {self.col}" if self.col > 0 else ""


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

    @abstractmethod
    def color(self, vertex: Vertex, t: str) -> None:
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

    def __check_color_availability(self, idx: int, visited: Set[Vertex], cols: List[int]) -> int:
        cols_temp = set()
        for neigh_ind in range(self.size()):
            if idx != neigh_ind and self.matrix[idx][neigh_ind] > 0:
                neigh_ver = self.list_vertex[neigh_ind]
                if neigh_ver in visited:
                    cols_temp.add(neigh_ver.col)
        for c in cols:
            if c not in cols_temp:
                return c
        cols.append(cols[-1] + 1)
        return cols[-1]

    def __dfs_color(self, vertex: Vertex) -> None:
        if not self.is_empty() and vertex in self.map_vertex:
            cols = [1]
            visited = set()

            def dfs_color_in(v: Vertex) -> None:
                if v not in visited:
                    v_ind = self.map_vertex[v]
                    v.col = self.__check_color_availability(v_ind, visited, cols)
                    visited.add(v)
                    for idx in range(self.size()):
                        if idx != v_ind and self.matrix[v_ind][idx] > 0:
                            neigh = self.list_vertex[idx]
                            if neigh not in visited:
                                dfs_color_in(neigh)

            dfs_color_in(vertex)

    def __bfs_color(self, vertex: Vertex) -> None:
        if not self.is_empty() and vertex in self.map_vertex:
            cols = [1]
            visited = set()
            vertex.col = self.__check_color_availability(self.map_vertex[vertex], visited, cols)
            visited.add(vertex)
            queue = [vertex]
            while queue:
                popped = queue.pop(0)
                popped_ind = self.map_vertex[popped]
                for idx in range(self.size()):
                    if idx != popped_ind and self.matrix[popped_ind][idx] > 0:
                        neigh = self.list_vertex[idx]
                        if neigh not in visited:
                            neigh.col = self.__check_color_availability(self.map_vertex[neigh], visited, cols)
                            visited.add(neigh)
                            queue.append(neigh)

    def color(self, vertex: Vertex, t: str) -> None:
        if t == 'dfs':
            self.__dfs_color(vertex)
        elif t == 'bfs':
            self.__bfs_color(vertex)


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

    def __check_color_availability(self, v: Vertex, visited: Set[Vertex], cols: List[int]) -> int:
        cols_temp = set()
        for vertex in self.list_vertex:
            if vertex in self.adj_list[v] and vertex in visited:
                cols_temp.add(vertex.col)
        for c in cols:
            if c not in cols_temp:
                return c
        cols.append(cols[-1] + 1)
        return cols[-1]

    def __dfs_color(self, vertex: Vertex) -> None:
        if not self.is_empty() and vertex in self.adj_list:
            cols = [1]
            visited = set()

            def dfs_color_in(v: Vertex) -> None:
                if v not in visited:
                    v.col = self.__check_color_availability(v, visited, cols)
                    visited.add(v)
                    for neigh in self.list_vertex:
                        if neigh not in visited and neigh in self.adj_list[v]:
                            dfs_color_in(neigh)
            dfs_color_in(vertex)

    def __bfs_color(self, vertex: Vertex) -> None:
        if not self.is_empty() and vertex in self.adj_list:
            cols = [1]
            visited = set()
            vertex.col = self.__check_color_availability(vertex, visited, cols)
            visited.add(vertex)
            queue = [vertex]
            while queue:
                popped = queue.pop(0)
                for neigh in self.list_vertex:
                    if neigh not in visited and neigh in self.adj_list[popped]:
                        neigh.col = self.__check_color_availability(neigh, visited, cols)
                        visited.add(neigh)
                        queue.append(neigh)

    def color(self, vertex: Vertex, t: str) -> None:
        if t == 'dfs':
            self.__dfs_color(vertex)
        elif t == 'bfs':
            self.__bfs_color(vertex)


def color_graph(G: Graph, vertex: Vertex, t: str) -> None:
    G.color(vertex, t)


def main():
    graph_matrix = GraphMatrix()
    graph_list = GraphList()

    for tup in polska.graf:
        vertex1 = Vertex(tup[0])
        vertex2 = Vertex(tup[1])
        graph_matrix.insert_edge(vertex1, vertex2)
        graph_list.insert_edge(vertex1, vertex2)

    first = graph_matrix.list_vertex[0]
    color_graph(G=graph_matrix, vertex=first, t='dfs')
    polska.draw_map(graph_matrix.edges(), [(elem.key, elem.col) for elem in graph_matrix.list_vertex])
    color_graph(G=graph_list, vertex=first, t='dfs')
    polska.draw_map(graph_list.edges(), [(elem.key, elem.col) for elem in graph_list.adj_list])


if __name__ == '__main__':
    main()
