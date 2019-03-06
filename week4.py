from graph import *
from graph_io import *
from week3 import *


def revert_changes(D, I, old_colors):
    if len(D) != 0:

        for i in range(len(D)):
            last_D = D[i]
            last_I = I[i]

            last_D.colornum = old_colors[i]
            last_I.colornum = old_colors[i]
            last_D.label = last_D.colornum
            last_I.label = last_I.colornum


def count_isomorphism(inputG: Graph, inputH: Graph, D, I):
    G = copy.copy(inputG)
    G._v = inputG._v[:]
    for i in range(len(G._v)):
        G._v[i] = copy.copy(inputG._v[i])
        G._v[i]._graph=G


    H = copy.copy(inputH)
    H._v = inputH._v[:]
    for i in range(len(H._v)):
        H._v[i] = copy.copy(inputH._v[i])
        H._v[i]._graph = H

    if len(D) != 0:
        newcol = len(G.verts)
        i=len(D)-1
        last_D = G.vertices[D[i]]
        last_I = H.vertices[I[i]]


        last_D.colornum = newcol
        last_I.colornum = newcol
        last_D.label = last_D.colornum
        last_I.label = last_I.colornum

    G = CRefignment(G)
    H = CRefignment(H)


    if not compare_partitions(G, H):
        return 0
    else:
        all_colors_are_unique = True
        for i in range(len(G.verts)):
            if len(G.verts[i]) > 1 or len(H.verts[i]) > 1:
                all_colors_are_unique = False
        if all_colors_are_unique:
            return 1

    C = -1
    for i in range(len(G.verts)):
        Gcolor = G.verts[i][:]  # list with vertices of same color
        Hcolor = H.verts[i][:]
        if len(Gcolor) + len(Hcolor) >= 4:
            C = i
            break

    if C == -1:

        return 0

    # new_G = copy.copy(G)
    # new_G._v = G._v[:]
    # for i in range(len(new_G._v)):
    #     new_G._v[i] = copy.copy(G._v[i])
    #     new_G._v[i]._graph=new_G
    #
    #
    # new_H = copy.copy(H)
    # new_H._v = H._v[:]
    # for i in range(len(new_H._v)):
    #     new_H._v[i] = copy.copy(H._v[i])
    #     new_H._v[i]._graph = new_H

    x = G.verts[C][0]

    num = 0

    for y in H.verts[C]:

        num = num + count_isomorphism(G, H, D + [G._v.index(x)], I + [H._v.index(y)])

    return num


if __name__ == "__main__":
    G1, G2 = load_graphs("graphs/colorref_smallexample_4_7.grl", 0,2)
    G1 = initialize_colors(G1)
    G2 = initialize_colors(G2)
    print(compare_graph_colors(G1, G2))
    print(count_isomorphism(G1, G2, [], []))
    write_graph_to_dot_file(G1, "G1")
    write_graph_to_dot_file(G2, "G2")
