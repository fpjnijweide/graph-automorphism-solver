from graph import *


def create_graph_with_cycle(n):
    G = Graph(False, n)

    for i in range(len(G.vertices)):
        if i != len(G.vertices) - 1:
            e = Edge(G.vertices[i], G.vertices[i + 1])

        else:
            e = Edge(G.vertices[i], G.vertices[0])

        G.add_edge(e)
    return G


def create_complete_graph(n):
    G = Graph(False, n)

    for i in range(len(G.vertices) - 1):
        for j in range(i + 1, len(G.vertices)):
            e = Edge(G.vertices[i], G.vertices[j])
            G.add_edge(e)
    return G
