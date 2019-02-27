from graph import *
from graph_io import *
import collections

def load_graphs(filename: str, nr1: int, nr2: int):
    with open(filename) as f:
        G1 = load_graph(f)[0][nr1]
        G2 = load_graph(f)[0][nr2]
        return G1,G2

def CRefignment(G: Graph):
    for v in G.vertices:
        v.colornum = v.degree
    equal = False
    while not equal:
        colorGraph(G)
        old_graph=copy.deepcopy(G)
        equal=compare_graph_colors(G, old_graph)
    return G


def compare_graph_colors(g1: Graph, g2: Graph):
    print("Comparing two graphs")
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
        #if the degree is not found in verts, add empty lists to it
        if v.colornum > len(verts)-1:
            diff=v.colornum - (len(verts)-1)
            for i in range(diff):
                verts.append([])
        #add the vertex to its respective index in verts
        verts[v.colornum].append(v)
    for i in verts:
        l = verts[i]
        for i in range (1, len(l)):
            v0 = colorNeighbours(l[0])
            vi = colorNeighbours(l[i])
            compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
            if not compare(v0, vi):



def write_graph_to_dot_file(G: Graph):
    with open('mygraph.dot', 'w') as f:
        write_dot(G, f)

if __name__=="__main__":
    # main method
    G1,G2 = load_graphs("graph/colorref_smallexample_4_7.grl",1,3)
    G1 = CRefignment(G1)
    G2 = CRefignment(G2)

    result = compare_two_graphs(G1,G2)
    print(result)



def colorNeighbours(v: Vertex):
    colors = []
    for n in v.neighbours:
        colors.append(n.colornum)
    return sorted(colors)
