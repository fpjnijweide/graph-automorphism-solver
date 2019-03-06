from graph import *
from graph_io import *
from week3 import *


def count_isomorphism(G: Graph, H: Graph, D, I):

    if len(D) != 0:
        newcol = len(G.verts)
        i = len(D) - 1
        last_D = D[i]
        last_I = I[i]

        last_D.colornum = newcol
        last_I.colornum = newcol
        last_D.label = last_D.colornum
        last_I.label = last_I.colornum


    new_G=copy.deepcopy(G)
    new_H=copy.deepcopy(H)
    new_G = CRefignment(new_G)
    new_H = CRefignment(new_H)

    if not compare_partitions(new_G, new_H):
        return 0
    else:
        all_colors_are_unique=True
        for i in range(len(new_G.verts)):
            if len( new_G.verts[i])>1 or len (new_H.verts[i])>1:
                all_colors_are_unique=False
        if all_colors_are_unique:
            return 1

    C=-1
    for i in range(len(new_G.verts)):
        Gcolor = new_G.verts[i][:]  # list with vertices of same color
        Hcolor = new_H.verts[i][:]
        if len(Gcolor)+len(Hcolor)>=4:
            C=i
            break

    if C==-1:
        return 0

    x=new_G.verts[C][0]


    num = 0

    for y in new_H.verts[C]:
        num = num + count_isomorphism(new_G, new_H, D + [x], I + [y])


    return num

if __name__ == "__main__":
    G1, G2 = load_graphs("graphs/cubes5.grl", 2,3)
    G1 = initialize_colors(G1)
    G2 = initialize_colors(G2)
    print(count_isomorphism(G1, G2, [], []))
    write_graph_to_dot_file(G1, "G1")
    write_graph_to_dot_file(G2, "G2")
