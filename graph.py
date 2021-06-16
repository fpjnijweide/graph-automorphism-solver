# graph module
# original authors P. Bonsma (2015), P. Bos and T. Bontekoe (2017)
import copy

from typing import List, Union, Set


class GraphError(Exception):
    def __init__(self, message: str):
         super(GraphError, self).__init__(message)


class Vertex(object):
    def __init__(self, graph: "Graph", label=None):
        if label is None:
            label = graph._next_label()

        self._graph = graph
        self.label = label
        self._incidence = {}
        self._neighborset = []
        self._neighbor_colors = []
        self.colornum = 0
        self.label = 0
        self._neighbor_colors_sum = 0

    def __repr__(self):
        return 'Vertex(label={}, #incident={})'.format(self.label, len(self._incidence))

    def __str__(self) -> str:
        return str(self.label)

    def is_adjacent(self, other: "Vertex") -> bool:
        return other in self._incidence

    def _add_incidence(self, edge: "Edge"):
        other = edge.other_end(self)

        if other not in self._incidence:
            self._incidence[other] = set()

        self._incidence[other].add(edge)

    @property
    def graph(self) -> "Graph":
        return self._graph

    @property
    def incidence(self) -> List["Edge"]:
        result = set()

        for edge_set in self._incidence.values():
            result |= edge_set

        return list(result)

    @property
    def neighbors(self) -> List["Vertex"]:
         return list(self._neighborset)

    def _add_neighbor(self, vertex: "Vertex"):
        self._neighborset.append(vertex)

    def change_color(self, color):
        for neighbor in self._neighborset:
            neighbor._neighbor_colors.remove(self.colornum)
            neighbor._neighbor_colors_sum -= self.colornum
            neighbor._neighbor_colors.append(color)
            neighbor._neighbor_colors_sum += color
        self.colornum = color
        self.label = color

    @property
    def degree(self) -> int:
        """
        Returns the degree of the vertex
        """
        return sum(map(len, self._incidence.values()))


class Edge(object):

    def __init__(self, tail: Vertex, head: Vertex, weight=None):
        if tail.graph != head.graph:
            raise GraphError("Can only add edges between vertices of the same graph")

        self._tail = tail
        self._head = head
        self._weight = weight

    def __repr__(self):
        return 'Edge(head={}, tail={}, weight={})'.format(self.head.label, self.tail.label, self.weight)

    def __str__(self) -> str:
        return '({}, {})'.format(str(self.tail), str(self.head))

    @property
    def tail(self) -> "Vertex":
        return self._tail

    @property
    def head(self) -> "Vertex":
        return self._head

    @property
    def weight(self):
        return self._weight

    def other_end(self, vertex: Vertex) -> Vertex:
        if self.tail == vertex:
            return self.head
        elif self.head == vertex:
            return self.tail

        raise GraphError(
            'edge.other_end(vertex): vertex must be head or tail of edge')

    def incident(self, vertex: Vertex) -> bool:
        return self.head == vertex or self.tail == vertex


class Graph(object):
    def __init__(self, directed: bool, n: int = 0, simple: bool = False):
        self._v = list()
        self._e = list()
        self._simple = simple
        self._directed = directed
        self._next_label_value = 0

        for i in range(n):
            self.add_vertex(Vertex(self))

        self.partition = {}

    def __repr__(self):
        return 'Graph(directed={}, simple={}, #edges={n_edges}, #vertices={n_vertices})'.format(
            self._directed, self._simple, n_edges=len(self._e), n_vertices=len(self._v))

    def __str__(self) -> str:
        return 'V=[' + ", ".join(map(str, self._v)) + ']\nE=[' + ", ".join(map(str, self._e)) + ']'

    def _next_label(self) -> int:
        result = self._next_label_value
        self._next_label_value += 1
        return result

    @property
    def simple(self) -> bool:
        return self._simple

    @property
    def directed(self) -> bool:
        return self._directed

    @property
    def vertices(self) -> List["Vertex"]:
        return list(self._v)

    @property
    def edges(self) -> List["Edge"]:
        return list(self._e)

    def __iter__(self):
        return iter(self._v)

    def __len__(self) -> int:
        return len(self._v)

    def add_vertex(self, vertex: "Vertex"):
        if vertex.graph != self:
            raise GraphError("A vertex must belong to the graph it is added to")

        self._v.append(vertex)

    def del_vertex(self, vertex: "Vertex"):
        for edge in vertex.incidence:
            self.del_edge(edge)
        self._v.remove(vertex)

    def add_edge(self, edge: "Edge"):
        if self._simple:
            if edge.tail == edge.head:
                raise GraphError('No loops allowed in simple graphs')

            if self.is_adjacent(edge.tail, edge.head):
                raise GraphError('No multiedges allowed in simple graphs')

        if edge.tail not in self._v:
            self.add_vertex(edge.tail)
        if edge.head not in self._v:
            self.add_vertex(edge.head)

        self._e.append(edge)

        edge.head._add_incidence(edge)
        edge.tail._add_incidence(edge)
        if edge.tail == edge.head:
            pass
        edge.head._add_neighbor(edge.tail)
        edge.head._neighbor_colors.append(edge.tail.colornum)
        edge.head._neighbor_colors_sum += edge.tail.colornum
        edge.tail._add_neighbor(edge.head)
        edge.tail._neighbor_colors.append(edge.head.colornum)
        edge.tail._neighbor_colors_sum += edge.head.colornum

    def del_edge(self, edge: "Edge"):
        edge.tail._incidence[edge.head].remove(edge)
        edge.head._incidence[edge.tail].remove(edge)
        edge.tail._neighborset.remove(edge.head)
        edge.head._neighborset.remove(edge.tail)
        edge.tail._neighbor_colors.remove(edge.head.colornum)
        edge.head._neighbor_colors.remove(edge.tail.colornum)
        edge.tail._neighbor_colors_sum -= edge.head.colornum
        edge.head._neighbor_colors_sum -= edge.tail.colornum
        self._e.remove(edge)

    def __add__(self, other: "Graph") -> "Graph":
        G = copy.copy(self)
        d = {}
        for v in other.vertices:
            new_v = Vertex(G, v.label)
            G.add_vertex(new_v)
            d[v] = new_v
        for e in other.edges:
            new_e = Edge(d[e.tail], d[e.head])
            G.add_edge(new_e)
        return G

    def __iadd__(self, other: Union[Edge, Vertex]) -> "Graph":
        if isinstance(other, Vertex):
            self.add_vertex(other)

        if isinstance(other, Edge):
            self.add_edge(other)

        return self

    def find_edge(self, u: "Vertex", v: "Vertex") -> Set["Edge"]:
        result = u._incidence.get(v, set())

        if not self._directed:
            result |= v._incidence.get(u, set())

        return set(result)

    def is_adjacent(self, u: "Vertex", v: "Vertex") -> bool:
        return v in u.neighbors and (not self.directed or any(e.head == v for e in u.incidence))


class UnsafeGraph(Graph):
    @property
    def vertices(self) -> List["Vertex"]:
        return self._v

    @property
    def edges(self) -> List["Edge"]:
        return self._e

    def add_vertex(self, vertex: "Vertex"):
        self._v.append(vertex)

    def add_edge(self, edge: "Edge"):
        self._e.append(edge)

        edge.head._add_incidence(edge)
        edge.tail._add_incidence(edge)

    def find_edge(self, u: "Vertex", v: "Vertex") -> Set["Edge"]:
        left = u._incidence.get(v, None)
        right = None

        if not self._directed:
            right = v._incidence.get(u, None)

        if left is None and right is None:
            return set()

        if left is None:
            return right

        if right is None:
            return left

        return left | right

    def is_adjacent(self, u: "Vertex", v: "Vertex") -> bool:
        return v in u._incidence or (not self._directed and u in v._incidence)
