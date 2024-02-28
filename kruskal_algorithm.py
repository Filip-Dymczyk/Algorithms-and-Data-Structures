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

    @abstractmethod
    def prim(self, v: Vertex):
        pass

    @abstractmethod
    def kruskal(self):
        pass


class UnionFind:
    def __init__(self) -> None:
        self.p = []
        self.size = []
        self.map = {}

    def find(self, v: Vertex) -> Vertex:
        return self.p[self.map[v]]

    def union_sets(self, s1: Vertex, s2: Vertex) -> None:
        p_s1 = self.find(s1)
        p_s2 = self.find(s2)
        if p_s1 != p_s2:
            size1 = self.size[self.map[p_s1]]
            size2 = self.size[self.map[p_s2]]
            if size1 < size2:
                self.p[self.map[p_s1]] = p_s2
                self.size[self.map[p_s2]] += 1
            else:
                self.p[self.map[p_s2]] = p_s1
                self.size[self.map[p_s1]] += 1

    def same_component(self, s1: Vertex, s2: Vertex) -> bool:
        return self.find(s1) == self.find(s2)


class GraphList(Graph):
    def __init__(self) -> None:
        self.adj_list = {}
        self.list_vertex = []
        self.map_vertex = {}
        self.in_tree = set()
        self.distance = {}
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

    def edges_with_d(self) -> List[Tuple[Vertex, Vertex, int]]:
        if not self.is_empty():
            l = []
            for current_vertex, neighs in self.adj_list.items():
                for neighbour_vertex in neighs:
                    tup = (current_vertex, neighbour_vertex, self.adj_list[current_vertex][neighbour_vertex])
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

    def __create_uf(self) -> UnionFind:
        uf = UnionFind()
        for ver in self.list_vertex:
            uf.p.append(ver)
            uf.size.append(1)
            uf.map[ver] = len(uf.p) - 1
        return uf

    def kruskal(self):
        e = self.edges_with_d()
        e.sort(key=lambda a: a[2])
        uf = self.__create_uf()
        mst = GraphList()
        i = 0
        while i < len(e) and mst.size() != self.size():
            v1, v2 = e[i][0], e[i][1]
            if not uf.same_component(v1, v2):
                uf.union_sets(v1, v2)
                mst.insert_edge(v1, v2, e[i][2])
            i += 1
        return mst

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


def printGraph(g):
    n = g.size()
    print("------GRAPH------ ", n)
    for i in range(n):
        v = g.list_vertex[i]
        print(v, end=" -> ")
        for ver, w in g.adj_list[v].items():
            print(ver, w, end="; ")
        print()
    print("-------------------")


def main():
    graph = [('A', 'B', 4), ('A', 'C', 1), ('A', 'D', 4),
            ('B', 'E', 9), ('B', 'F', 9), ('B', 'G', 7), ('B', 'C', 5),
            ('C', 'G', 9), ('C', 'D', 3),
            ('D', 'G', 10), ('D', 'J', 18),
            ('E', 'I', 6), ('E', 'H', 4), ('E', 'F', 2),
            ('F', 'H', 2), ('F', 'G', 8),
            ('G', 'H', 9), ('G', 'J', 8),
            ('H', 'I', 3), ('H', 'J', 9),
            ('I', 'J', 9)
            ]

    G = GraphList()
    for t in graph:
        G.insert_edge(Vertex(t[0]), Vertex(t[1]), t[2])

    uf = UnionFind()
    v1 = Vertex("1")
    v2 = Vertex("2")
    v3 = Vertex("3")
    v4 = Vertex("4")
    v5 = Vertex("5")
    l = [v1, v2, v3, v4, v5]
    for v in l:
        uf.p.append(v)
        uf.size.append(1)
        uf.map[v] = len(uf.p) - 1
    uf.union_sets(v1, v2)
    uf.union_sets(v4, v5)
    print(uf.same_component(v1, v2), uf.same_component(v2, v3), uf.same_component(v4, v5))
    uf.union_sets(v3, v1)
    print(uf.same_component(v1, v2), uf.same_component(v2, v3), uf.same_component(v4, v5))
    print()
    G_kruskal = G.kruskal()
    printGraph(G_kruskal)


if __name__ == '__main__':
    main()
