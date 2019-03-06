from week3 import *


def count_isomorphism(G: Graph, H: Graph, D, I):
    # todo compute coarsest stable coloring of G (with Crefinement) while giving the final element of D a unique color
    #  todo compute coarsest stable coloring of H  (with Crefinement) while giving the final element of I the same color as above


    if not compare_partitions(G1, G2):
        return 0
    else:
        pass
        # TODO Check if all sets in the dict of the graphs have length 1. If this is the case, return 1


    # TODO choose color class C with |C| >= 4 (so its length in G + length in H >=4)

    # TODO choose a vertex x, which has color C and is in graph G

    num = 0

    # TODO for all y with color y and in graph H:
    num = num + count_isomorphism(copy.deepcopy(G), copy.deepcopy(H), D + [x], I + [y])


    return num

if __name__ == "__main__":
    G1, G2 = load_graphs("graphs/colorref_smallexample_6_15.grl", 0, 1)
    G1 = initialize_colors(G1)
    G2 = initialize_colors(G2)
    count_isomorphism(G1, G2, [], [])
