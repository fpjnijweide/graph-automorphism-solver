from graph import *
from graph_io import *

def CRefignment(filename):
    with open(filename) as f:
        G = load_graph(f)[0][0]
        for v in G.vertices:
            v.colornum = v.degree

        old_graph = copy.deepcopy(G)
        equal = False
        while not equal:
            colourGraph(G)
        return G

def colourGraph(G):
    verts = dict()
    for v in G.vertices:
        if v.colornum in verts:
            verts[v.colornum] = verts.get(v.colournum).append(v)
        else:
            verts[v.colornum] = [v]
