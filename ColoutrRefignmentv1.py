from graph import *
from graph_io import *

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
    return G


def compare_two_graphs(G1: Graph, G2: Graph):
    print("Comparing two graphs")
    #TODO implement
    if len(G1.vertices)==len(G2.vertices):
        pass
        #if G1 vertices all have same degree as G2 vertices
            #if they are all the same color?
                #return true else false?

    return True

def colorGraph(G: Graph):
    old_graph = copy.deepcopy(G)
    verts = dict()
    for v in G.vertices:
        if v.colornum in verts:
            verts[v.colornum] = verts.get(v.colornum).append(v)
        else:
            verts[v.colornum] = [v]

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
