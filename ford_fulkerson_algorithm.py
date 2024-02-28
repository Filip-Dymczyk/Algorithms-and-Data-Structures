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
        return f"{self.key}"


class Edge:
    def __init__(self, capacity: int, isResidual: bool) -> None:
        if not isResidual:
            self.flow = 0
            self.residual = capacity
        else:
            self.flow = None
            self.residual = 0
        self.capacity = capacity
        self.isResidual = isResidual

    def __repr__(self) -> str:
        return f"{self.capacity} {self.flow} {self.residual} {self.isResidual}"


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
    def insert_edge(self, vertex1: Vertex, vertex2: Vertex, capacity: int) -> None:
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

    @abstractmethod
    def prim(self, v: Vertex):
        pass


class GraphListDirected(Graph):
    def __init__(self) -> None:
        self.adj_list = {}
        self.list_vertex = []
        self.map_vertex = {}
        self.in_tree = set()
        self.distance = {}
        self.parent = {}

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

    def insert_edge(self, vertex1: Vertex, vertex2: Vertex, capacity: int) -> None:
        if vertex1 not in self.adj_list:
            self.insert_vertex(vertex1)
        if vertex2 not in self.adj_list:
            self.insert_vertex(vertex2)
        if vertex2 not in self.adj_list[vertex1]:
            self.adj_list[vertex1][vertex2] = []
        if vertex1 not in self.adj_list[vertex2]:
            self.adj_list[vertex2][vertex1] = []
        self.adj_list[vertex1][vertex2].append(Edge(capacity, False))
        self.adj_list[vertex2][vertex1].append(Edge(capacity, True))

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

    def prim(self, v: Vertex):
        mst = GraphList()
        length = 0
        for ver in self.list_vertex:
            self.distance[ver] = float('inf')
            self.parent[ver] = -1
        while v not in self.in_tree:
            self.in_tree.add(v)
            for neigh in self.adj_list[v]:
                if neigh not in self.in_tree and \
                        self.adj_list[v][neigh] < self.distance[neigh]:
                    self.distance[neigh] = self.adj_list[v][neigh]
                    self.parent[neigh] = v
            min_dist = float('inf')
            min_ver = v
            for to_ver, dist in self.distance.items():
                if to_ver not in self.in_tree and dist < min_dist:
                    min_ver = to_ver
                    min_dist = dist
            mst.insert_edge(self.parent[min_ver], min_ver, self.distance[min_ver])
            v = min_ver
        return mst, length

    def bfs_ff(self, v: Vertex) -> List[Vertex]:
        visited = set()
        parent = [0 for _ in range(self.size())]
        queue = [v]
        parent[self.map_vertex[v]] = v
        visited.add(v)
        while queue:
            popped = queue.pop(0)
            for neigh in self.adj_list[popped]:
                for edge in self.adj_list[popped][neigh]:
                    if neigh not in visited and edge.residual > 0:
                        visited.add(neigh)
                        parent[self.map_vertex[neigh]] = popped
                        queue.append(neigh)
        return parent

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


def lowest_capacity(G: Graph, v_start: Vertex, v_end: Vertex, parent: List[Vertex]) -> int:
    current_idx = G.map_vertex[v_end]
    lowest_cap = float('inf')
    if not isinstance(parent[current_idx], Vertex):
        return 0
    while current_idx > G.map_vertex[v_start]:
        par = parent[current_idx]
        for edge in G.adj_list[par][v_end]:
            if not edge.isResidual:
                lowest_cap = edge.residual if edge.residual < lowest_cap else lowest_cap
        current_idx = G.map_vertex[par]
        v_end = par
    return lowest_cap


def path_augment(G: Graph, v_start: Vertex, v_end: Vertex, parent: List[Vertex], lowest_cap: int) -> None:
    current_idx = G.map_vertex[v_end]
    if isinstance(parent[current_idx], Vertex):
        while current_idx > G.map_vertex[v_start]:
            par = parent[current_idx]
            for edge in G.adj_list[par][v_end]:
                if not edge.isResidual:
                    edge.flow += lowest_cap
                    edge.residual -= lowest_cap
            for edge in G.adj_list[v_end][par]:
                if edge.isResidual:
                    edge.residual += lowest_cap
            current_idx = G.map_vertex[par]
            v_end = par


def ff_algorithm(G: Graph, v_start: Vertex, v_end: Vertex) -> int:
    parent = G.bfs_ff(v_start)
    lowest_cap = lowest_capacity(G, v_start, v_end, parent)
    res = lowest_cap
    while lowest_cap:
        path_augment(G, v_start, v_end, parent, lowest_cap)
        parent = G.bfs_ff(v_start)
        lowest_cap = lowest_capacity(G, v_start, v_end, parent)
        res += lowest_cap
    return res


def printGraph(g):
    n = g.size()
    print("------GRAPH------ ", n)
    for i in range(n):
        v = g.list_vertex[i]
        print(v, end=" -> ")
        for ver, w in g.adj_list[v].items():
            for edge in w:
                print(ver, edge, end="; ")
        print()
    print("-------------------")


def test(g, i):
    G = GraphListDirected()
    for t in g:
        G.insert_edge(Vertex(t[0]), Vertex(t[1]), t[2])
    print(f"Graph{i}:")
    print(f"The highest flow: {ff_algorithm(G, Vertex('s'), Vertex('t'))}")
    printGraph(G)


def main():
    graf_0 = [('s', 'u', 2), ('u', 't', 1), ('u', 'v', 3), ('s', 'v', 1), ('v', 't', 2)]
    graf_1 = [('s', 'a', 16), ('s', 'c', 13), ('a', 'c', 10), ('c', 'a', 4), ('a', 'b', 12), ('b', 'c', 9),
              ('b', 't', 20), ('c', 'd', 14), ('d', 'b', 7), ('d', 't', 4)]
    graf_2 = [('s', 'a', 3), ('s', 'c', 3), ('a', 'b', 4), ('b', 's', 3), ('b', 'c', 1), ('b', 'd', 2), ('c', 'e', 6),
              ('c', 'd', 2), ('d', 't', 1), ('e', 't', 9)]
    graf_3 = [('s', 'a', 8), ('s', 'd', 3), ('a', 'b', 9), ('b', 'd', 7), ('b', 't', 2), ('c', 't', 5), ('d', 'b', 7),
              ('d', 'c', 4)]
    graphs = [graf_0, graf_1, graf_2, graf_3]
    i = 0
    for g in graphs:
        test(g, i)
        i += 1


if __name__ == '__main__':
    main()
