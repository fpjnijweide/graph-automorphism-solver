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


def count_isomorphism(G: Graph, H: Graph, D, I):
    D = D[:]
    I = I[:]
    old_colors = []
    if len(D) != 0:
        newcol = len(G.verts)
        for i in range(len(D)):
            last_D = D[i]
            last_I = I[i]
            old_colors.append(last_D.colornum)

            last_D.colornum = newcol
            last_I.colornum = newcol
            last_D.label = last_D.colornum
            last_I.label = last_I.colornum

    G = CRefignment(G)
    H = CRefignment(H)

    if not compare_partitions(G, H):
        revert_changes(D, I, old_colors)
        return 0
    else:
        all_colors_are_unique = True
        for i in range(len(G.verts)):
            if len(G.verts[i]) > 1 or len(H.verts[i]) > 1:
                all_colors_are_unique = False
        if all_colors_are_unique:
            revert_changes(D, I, old_colors)
            return 1

    C = -1
    for i in range(len(G.verts)):
        Gcolor = G.verts[i][:]  # list with vertices of same color
        Hcolor = H.verts[i][:]
        if len(Gcolor) + len(Hcolor) >= 4:
            C = i
            break

    if C == -1:
        revert_changes(D, I, old_colors)
        return 0

    x = G.verts[C][0]

    num = 0

    revert_changes(D, I, old_colors)
    for y in H.verts[C]:
        num = num + count_isomorphism(G, H, D + [x], I + [y])

    return num


if __name__ == "__main__":
    G1, G2 = load_graphs("graphs/cubes5.grl", 2, 3)
    G1 = initialize_colors(G1)
    G2 = initialize_colors(G2)
    print(count_isomorphism(G1, G2, [], []))
    write_graph_to_dot_file(G1, "G1")
    write_graph_to_dot_file(G2, "G2")
