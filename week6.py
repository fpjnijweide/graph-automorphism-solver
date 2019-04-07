from graph import *
from week3 import *
from week4 import *
import time
from graphviz import render
from week5 import *
from permv2 import *
from basicpermutationgroup import *

def automorphisms_cycles(G: Graph, H: Graph, D, I, G_partition_backup, H_partition_backup):
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
        return None
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
            # print(P2)
            if D:
                return P2.cycles()
            else:
                return []

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
        return []

    # Choose a twin vertex of this color in G (and first vertex if this does not exist) and check for all y of this color in H
    # if they are isomorphs
    if Settings.TWIN_CHECK:
        x = find_twins(G.partition[chosen_color])
    else:
        x = G.partition[chosen_color][0]
    H_partition_chosen_color = H.partition[chosen_color][:]
    permutations=[]

    new_G_partition = G.partition
    new_H_partition = H.partition
    # color_by_partition(G_partition_backup)
    # color_by_partition(H_partition_backup)
    #
    # G.partition = G_partition_backup
    # H.partition = H_partition_backup


    for y in H_partition_chosen_color:
        D= old_D[:] + [G._v.index(x)]

        I= old_I[:] + [H._v.index(y)]



        res = automorphisms_cycles(G, H, D, I, new_G_partition,
                                   new_H_partition)
        if res: # if res is not empty
            if not isinstance(res[0],int):
                permutations.extend(res)
            else:
                permutations.append(res)
            if old_D:
                if old_D[-1] != old_I[-1]: #if this iteration is not trivial
                    return permutations



    return permutations

def algebra_magic(input_cycles,gr_size):
    print(input_cycles)

    permutations_list=[]

    a:list = [1,2,3]


    for cycle in input_cycles:


        new_perm_list=[]
        cycle_perm=permutation(gr_size,cycles=[cycle])
        is_unique=True
        try:
            for nr in range(1,len(cycle)):
                orb, trs = Orbit(permutations_list, cycle[nr-1], True)
                print("trans:::::" + str(trs))
                print("orb:::::" + str(orb))
                print("stab::::" + str(Stabilizer(permutations_list, cycle[0])))
                trans_cycle=trs[orb.index(cycle[nr])]
                composition_perm=-trans_cycle*cycle_perm
                print("composition perm:" + str(composition_perm))
                print("permutation list cycles:" + str(permutations_list))
                if composition_perm in permutations_list: #todo
                    is_unique=False
                    break

                # new_perm_list.append = (trs(orb.index(cycle[nr])) * cycle)
                print("yeahh")

        except ValueError:
            pass
        print("new_perm::: " + str(new_perm_list))
        # if trs(orb.index(cycle[1]))*cycle not in Stabilizer(permutations_list,cycle[0]):

        #     pass


        # todo maybe just don't add permutation that is multiple oof 2 other (1,4,5)
        if is_unique:
            permutations_list.append(cycle_perm)




    i=0
    o,trans = Orbit(permutations_list, i,True)
    while len(o)<2:
        i+=1
        o = Orbit(permutations_list, i)
    print(i)
    s=Stabilizer(permutations_list,i)
    print("orbit: "+ str(o))
    print("stabilizer: "+ str(s))
    print("permutations: " + str(permutations_list))
    print("reduced: " + str(Reduce(permutations_list)))

    print("transversal:" + str(trans))


    # cycle_list_new = []
    # permutations = permutation(gr_size)
    # for i in range(len(input_cycles)):
    #     new_cycle = input_cycles[i]
    #
    #     if [new_cycle[1], new_cycle[0]] not in cycle_list_new:
    #         cycle_list_new.append(new_cycle)
    #         permutations = permutations * permutation(gr_size, cycles=[new_cycle])


    if not o:
        o=[0]
    if not s:
        s=[0]
    return len(o)*len(s)

def count_automorphisms_groups(G1, G2, D,I, G_partition_backup, H_partition_backup):
    cycle_list=automorphisms_cycles(G1, G2, D,I, G_partition_backup, H_partition_backup)

    if cycle_list is None:
        return 0
    elif cycle_list==[]:
        return 1
    else:
        return algebra_magic(cycle_list,len(G1._v))



if __name__ == '__main__':
    G1, G2 = load_graphs("graphs/trees36.grl", 1,1)

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
    print("week 6 answer: "+ str(count_automorphisms_groups(G1, G2, [], [], G_partition_backup, H_partition_backup)))
    print("real nr: "+ str(count_automorphisms(G1, G2, [], [], G_partition_backup, H_partition_backup)))


    write_graph_to_dot_file(G1, "G1")
    write_graph_to_dot_file(G2, "G2")
    # render('dot', 'png', 'graphG1.dot')
    # render('dot', 'png', 'graphG2.dot')