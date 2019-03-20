from graph import *
from graph_io import *
import collections
from graphviz import render

compare = lambda x, y: collections.Counter(x) == collections.Counter(y)


def load_graphs(filename: str, nr1: int, nr2: int):
    with open(filename) as f:
        L = load_graph(f, read_list=True)
        G1 = L[0][nr1]
        G2 = L[0][nr2]
        return G1, G2


def colorNeighbours(v: Vertex):
    colors = []
    for n in v.neighbours:
        colors.append(n.colornum)
    return sorted(colors)


def initialize_colors(G: Graph):
    for v in G.vertices:
        v.colornum = v.degree
        v.label = v.colornum
    G.verts = create_verts(G.vertices)
    return G

def CRefignment(G: Graph, H: Graph):

    equal = False
    while not equal:
        amount_colors_G = len(G.verts)
        amount_colors_H = len(H.verts)
        colorGraph(G, H)
        new_amount_colors_G = len(G.verts)
        new_amount_colors_H = len(H.verts)
        equal = amount_colors_G == new_amount_colors_G and amount_colors_H == new_amount_colors_H
    return G, H


def compare_graph_colors(g1: Graph, g2: Graph):
    # Compare two iterations of the same graph to see if the colours have changed between the two iterations.
    for i in range(0, len(g1.vertices)):
        if (hasattr(g1.vertices[i], "colornum") and hasattr(g2.vertices[i], "colornum")) and \
                (g1.vertices[i].colornum != g2.vertices[i].colornum):
            return False
        if (hasattr(g1.vertices[i], "colornum") and not hasattr(g2.vertices[i], "colornum")) or \
                (not hasattr(g1.vertices[i], "colornum") and hasattr(g2.vertices[i], "colornum")):
            return False
    return True


def create_verts(vertices: list):
    # a list of lists, where the index equals the color and the list at that index is a list of vertices with that color
    verts = []

    for v in vertices:
        # if the degree is not found in verts, add empty lists to it
        if v.colornum > len(verts) - 1:
            diff = v.colornum - (len(verts) - 1)
            for i in range(diff):
                verts.append([])
        # add the vertex to its respective index in verts
        verts[v.colornum].append(v)

    return verts


def colorGraph(G: Graph, H: Graph):

    vertices = G.vertices + H.vertices
    verts = create_verts(vertices)

    # go through vertices with same color
    for i in range(len(verts)):
        l = verts[i][:]  # list with vertices of same color
        newcolor = len(verts)
        # to create new color for vertices that are not the same as v0

        # now look only at color group of multiple vertices
        if len(l) > 1:
            # v0 is vertex with smallest sum of colors of neighbours
            v0 = l[0]
            for v in l:
                if sum(colorNeighbours(v)) < sum(colorNeighbours(v0)):
                    v0 = v
            v0colors = colorNeighbours(v0)

            need_change = []

            for j in range(0, len(l)):
                current_vertex = l[j]
                if v0 != current_vertex:
                    vicolors = colorNeighbours(current_vertex)
                    if not compare(v0colors, vicolors):
                        need_change.append(current_vertex)

            for x in need_change:
                if newcolor == len(verts):
                    verts.append([])
                verts[newcolor].append(x)
                verts[x.colornum].remove(x)
                x.colornum = newcolor
                x.label = x.colornum

    G.verts = create_verts(G.vertices)
    H.verts = create_verts(H.vertices)




def write_graph_to_dot_file(G: Graph, title: str):
    with open('graph' + title + '.dot', 'w') as f:
        write_dot(G, f)


def PRefinement(g: Graph):
    partitions = create_verts(g)
    return partitions


def compare_partitions(g1: Graph, g2: Graph):
    partition1 = PRefinement(g1)
    partition2 = PRefinement(g2)
    for i in range(len(partition1)):
        if len(partition1[i]) != len(partition2[i]):
            return False
    return True


if __name__ == "__main__":
    # main method
    G1, G2 = load_graphs("graphs/bigtrees1.grl", 0, 2)
    G1 = initialize_colors(G1)
    G2 = initialize_colors(G2)
    G1, G2 = CRefignment(G1, G2)
    write_graph_to_dot_file(G1, "G1")
    write_graph_to_dot_file(G2, "G2")
    render('dot', 'png', 'graphG1.dot')
    render('dot', 'png', 'graphG2.dot')
    result = compare_partitions(G1, G2)
    print(result)
