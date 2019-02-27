from graph import *
from graph_io import *


def CRefignment(filename):
    with open(filename) as f:
        G = load_graph(f)[0][0]
        for v in G.vertices:
            v.colournum = v.degree





def write_dot_from_graph(G):
    with open('mygraph.dot', 'w') as f:
        write_dot(G, f)