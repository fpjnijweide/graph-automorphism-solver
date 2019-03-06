from week3 import *

def count_isomorphism(G: Graph, H: Graph, D,I):

    # TODO compute coarsest stable coloring..
    if not compare_partitions(G1, G2):
        return 0
    else:
        # TODO Check if it is a bijection (all sets have length 1)

    # TODO choose color class C with |C| >= 4

    # TODO choose a vertex x, which has color C and is in graph G

    num = 0

    # TODO for all y with color y and in graph H:
        num = num + count_isomorphism(G, H, D + [x], I + [y])

    return num