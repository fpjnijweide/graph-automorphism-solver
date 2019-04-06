from graph import *
from week3 import *
from week4 import *
import time
from graphviz import render
from week5 import *
from permv2 import *
from basicpermutationgroup import *

def count_automorphisms_groups(G: Graph, H: Graph, D, I, G_partition_backup, H_partition_backup):
    # Recursively counts all isomorphs of this graph
    old_D=D[:]
    old_I=I[:]
    color_by_partition(G_partition_backup)
    color_by_partition(H_partition_backup)
    G.partition = G_partition_backup
    H.partition = H_partition_backup

    # Color the last instances of D and I
    if len(D) != 0:
        newcol = len(G.partition)
        i = len(D) - 1
        last_D = G.vertices[D[i]]
        last_I = H.vertices[I[i]]

        last_D.colornum = newcol
        last_I.colornum = newcol
        last_D.label = last_D.colornum
        last_I.label = last_I.colornum

    # Refine the colors of G and H

    G.partition = create_partition(G.vertices)
    H.partition = create_partition(H.vertices)


    G, H = color_refinement(G, H)

    # If this coloring is not stable, return 0
    if not is_isomorphism(G, H):
        return 0
    else:
        # Else, check if all colors are unique. If so, it is an isomorph
        all_colors_are_unique = True
        for i in range(len(G.partition)):
            if len(G.partition[i]) > 1 or len(H.partition[i]) > 1:
                all_colors_are_unique = False
                break
        if all_colors_are_unique:
            cycle_list = []
            P2 = permutation(len(G._v))
            for i in range(len(D)):
                new_cycle = [D[i], I[i]]

                if [new_cycle[1], new_cycle[0]] not in cycle_list:
                    cycle_list.append(new_cycle)
                    P2 = P2 * permutation(len(G._v), cycles=[new_cycle])
            print(P2)
            return 1 #TODO return to the last visited trivial ancestor node

    # We have now found a stable coloring that has non-unique colors

    if Settings.PREPROCESSING and len(D) == 0:  # only once, after first call of fast refignment
        disconnectedG = disconnectedVertices(G)
        for v in disconnectedG:
            G._v.remove(v)
        disconnectedH = disconnectedVertices(H)
        for v in disconnectedH:
            H._v.remove(v)
    if Settings.TREE_CHECK and len(D) == 0:
        if isTree(G) and isTree(H):
            return countTreeIsomorphism(G)

    # Choose a color that is not unique
    chosen_color = -1
    for i in range(len(G.partition)):
        Gcolor = G.partition[i][:]  # list with vertices of same color
        Hcolor = H.partition[i][:]
        if len(Gcolor) + len(Hcolor) >= 4:
            chosen_color = i
            break
    if chosen_color == -1:
        # If no color has been chosen something obviously went wrong
        return 0

    # Choose a twin vertex of this color in G (and first vertex if this does not exist) and check for all y of this color in H
    # if they are isomorphs
    if Settings.TWIN_CHECK:
        x = find_twins(G.partition[chosen_color])
    else:
        x = G.partition[chosen_color][0]
    H_partition_chosen_color = H.partition[chosen_color][:]
    nr_of_isomorphisms = 0

    new_G_partition = G.partition
    new_H_partition = H.partition
    # color_by_partition(G_partition_backup)
    # color_by_partition(H_partition_backup)
    #
    # G.partition = G_partition_backup
    # H.partition = H_partition_backup


    for y in H_partition_chosen_color: #TODO start with y=x if possible
        D= old_D[:] + [G._v.index(x)]

        I= old_I[:] + [H._v.index(y)]

        cycle_list = []
        P2 = permutation(len(G._v))
        for i in range(len(D)):
            new_cycle=[D[i],I[i]]


            if [new_cycle[1],new_cycle[0]] not in cycle_list:
                cycle_list.append(new_cycle)
                P2 = P2* permutation(len(G._v), cycles=[new_cycle])
        # todo maybe remove permutation code here
        # P1 = permutation(len(G._v), cycles=cycle_list)  # todo what to do with this perm?


        # mapping1=list(range(len(G._v)))
        # for i in range(len(D)):
        #     mapping1[D[i]]=I[i]
        # P = permutation(len(G._v), mapping=mapping1)


        res = count_automorphisms_groups(G, H, D,I, new_G_partition,
                                               new_H_partition)
        if res==1:
            pass
            #TODO we may stop exploring this tree?
        nr_of_isomorphisms+= res

    return nr_of_isomorphisms


if __name__ == '__main__':
    G1, G2 = load_graphs("graphs/slides.gr", 0,0)

    # from week2 import *
    # G1=create_complete_graph(4)
    # G2=create_complete_graph(4)


    if (G1==G2):
        G2=copy_graph(G2)
    G1 = initialize_colors(G1)
    G2 = initialize_colors(G2)

    G_partition_backup = create_partition(G1.vertices)

    H_partition_backup = create_partition(G2.vertices)
    print(is_isomorphism(G1,G2))
    print(count_automorphisms_groups(G1, G2, [], [], G_partition_backup, H_partition_backup))

    write_graph_to_dot_file(G1, "G1")
    write_graph_to_dot_file(G2, "G2")
    # render('dot', 'png', 'graphG1.dot')
    # render('dot', 'png', 'graphG2.dot')