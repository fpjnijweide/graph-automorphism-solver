from graph import *
from graph_io import *

def CRefignment(filename):
    with open(filename) as f:
        G = load_graph(f)[0][0]
        for v in G.vertices:
            v.colornum = v.degree
        equal = False
        while not equal:
            colorGraph(G)
        return G

def colorGraph(G):
    old_graph = copy.deepcopy(G)
    verts = dict()
    for v in G.vertices:
        if v.colornum in verts:
            verts[v.colornum] = verts.get(v.colornum).append(v)
        else:
            verts[v.colornum] = [v]




def colorNeighbours(v):
    colors = []
    for n in v.neighbours:
        colors.append(n.colornum)
    return sorted(colors)
