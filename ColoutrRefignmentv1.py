from graph import *
from graph_io import *

def load_graphs(filename: str, nr1: int, nr2: int):
    with open(filename) as f:
        G1 = load_graph(f)[0][nr1]
        G2 = load_graph(f)[0][nr2]
        return G1,G2

def CRefignment(filename):
    with open(filename) as f:
        G = load_graph(f)[0][0]
        for v in G.vertices:
            v.colournum = v.degree



def compare_two_graphs(G1: Graph, G2: Graph):
    print("Comparing two graphs")
    #TODO implement

    return True

def write_graph_to_dot_file(G):
    with open('mygraph.dot', 'w') as f:
        write_dot(G, f)

if __name__=="__main__":
    # main method
    G1,G2 = load_graphs("graph/colorref_smallexample_4_7.grl",1,3)
    G1 = CRefignment(G1)
    G2 = CRefignment(G2)

    result = compare_two_graphs(G1,G2)
    print(result)