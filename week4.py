from week3 import *


def count_isomorphism(G: Graph, H: Graph, D, I):
    # todo compute coarsest stable coloring of G (with Crefinement) while giving the final element of D a unique color
    #  todo compute coarsest stable coloring of H  (with Crefinement) while giving the final element of I the same color as above

    if not compare_partitions(G1, G2):
        return 0
    else:
        all_colors_are_unique=True
        for i in range(len(G.verts)):
            if len( G.verts[i])!=1 or len (H.verts[i])!=1:
                all_colors_are_unique=False
        if all_colors_are_unique:
            return True

    C=-1
    for i in range(len(G.verts)):
        Gcolor = G.verts[i][:]  # list with vertices of same color
        Hcolor = H.verts[i][:]
        if len(Gcolor)+len(Hcolor)>=4:
            C=i
            break

    if C==-1:
        return 0

    x=G.verts[C][0]


    num = 0

    for y in H.verts[C]:
        num = num + count_isomorphism(copy.deepcopy(G), copy.deepcopy(H), D + [x], I + [y])


    return num

if __name__ == "__main__":
    G1, G2 = load_graphs("graphs/colorref_smallexample_6_15.grl", 0, 1)
    G1 = initialize_colors(G1)
    G2 = initialize_colors(G2)
    count_isomorphism(G1, G2, [], [])
