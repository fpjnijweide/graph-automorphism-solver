from graph import *
from graph_io import *
import collections

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

    verts=[]
    for v in G.vertices:
        # if the degree is not found in verts, add empty lists to it
        if v.colornum > len(verts) - 1:
            diff = v.colornum - (len(verts) - 1)
            for i in range(diff):
                verts.append([])
        # add the vertex to its respective index in verts
        verts[v.colornum].append(v)

    G.verts=verts
    return G

def CRefignment(G: Graph):

    equal = False
    while not equal:
        old_graph = copy.deepcopy(G)
        colorGraph(G)
        equal = compare_graph_colors(G, old_graph)
    return G


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


def colorGraph(G: Graph):
    old_graph = copy.deepcopy(G)
    verts = []

    for v in G.vertices:
        # if the degree is not found in verts, add empty lists to it
        if v.colornum > len(verts) - 1:
            diff = v.colornum - (len(verts) - 1)
            for i in range(diff):
                verts.append([])
        # add the vertex to its respective index in verts
        verts[v.colornum].append(v)

    # go through vertices with same color
    for i in range(len(verts)):
        l = verts[i][:]  # list with vertices of same color
        newcolor = len(verts)
        # to create new color for vertices that are not the same as v0
        for i in range(1, len(l)):
            v0 = colorNeighbours(l[0])
            current_vertex = l[i]
            vi = colorNeighbours(current_vertex)
            if not compare(v0, vi):
                if newcolor == len(verts):
                    verts.append([])
                verts[newcolor].append(current_vertex)
                verts[current_vertex.colornum].remove(current_vertex)
                current_vertex.colornum = newcolor
                current_vertex.label = current_vertex.colornum
    G.verts=verts


def write_graph_to_dot_file(G: Graph, title: str):
    with open('graph' + title + '.dot', 'w') as f:
        write_dot(G, f)


def PRefinement(g: Graph):
    partitions = {}
    for v in g.vertices:
        i = v.colornum
        if i not in partitions.keys():
            partitions[i] = []
        partitions[i].append(v)
    return partitions


def compare_partitions(g1: Graph, g2: Graph):
    partition1 = PRefinement(g1)
    partition2 = PRefinement(g2)
    for i in partition1.keys():
        if len(partition1[i]) != len(partition2[i]):
            return False
    return True


if __name__ == "__main__":
    # main method
    G1, G2 = load_graphs("graphs/cubes5.grl", 0, 1)
    G1 = initialize_colors(G1)
    G2 = initialize_colors(G2)
    G1 = CRefignment(G1)
    G2 = CRefignment(G2)
    write_graph_to_dot_file(G1, "G1")
    write_graph_to_dot_file(G2, "G2")
    result = compare_partitions(G1, G2)
    print(result)
