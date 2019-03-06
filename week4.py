from graph import *
from graph_io import *
from week3 import *


def count_isomorphism(G: Graph, H: Graph, D, I):

    if len(D) != 0:
        print("b")
        newcol = len(G.verts)
        i = len(D) - 1
        x = D[i]
        y = I[i]

        x.colornum = newcol
        y.colornum = newcol
        x.label = x.colornum
        y.label = y.colornum

    G = CRefignment(G)
    H = CRefignment(H)


    if not compare_partitions(G, H):
        print("c")
        return 0
    else:
        print("a")
        all_colors_are_unique=True
        for i in range(len(G.verts)):

            if len( G.verts[i])>1 or len (H.verts[i])>1:
                all_colors_are_unique=False
        if all_colors_are_unique:
            print("+1")
            return 1

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
    G1, G2 = load_graphs("graphs/cubes5.grl", 2, 3)
    print(compare_graph_colors(G1, G2))
    G1 = initialize_colors(G1)
    G2 = initialize_colors(G2)
    print(compare_graph_colors(G1, G2))
    print(count_isomorphism(G1, G2, [], []))
    write_graph_to_dot_file(G1, "G1")
    write_graph_to_dot_file(G2, "G2")
