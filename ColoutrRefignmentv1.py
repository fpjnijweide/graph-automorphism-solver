from graph import *
from graph_io import *

def CRefignment(filename):
    with open(filename) as f:
        G = load_graph(f)[0][0]
        for v in G.vertices:
            v.colournum = v.degree




