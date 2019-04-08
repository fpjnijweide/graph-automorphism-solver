from graph import *
from week3 import *
from week4 import *
import time
from graphviz import render
from week5 import *
from permv2 import *
from basicpermutationgroup import *
from week2 import *

def check_dihedral(G: Graph):

    is_cycle=True

    for i in range(len(G._v)):
        v=G._v[i]
        if len(v.neighbors)==2:
            pass
        else:
            is_cycle=False
            break
    return is_cycle

def check_complete(G: Graph):
    is_complete=True
    G_size=len(G._v)
    for i in range(len(G._v)):
        v = G._v[i]
        if not len(v.neighbors)==G_size-1:
            is_complete=False
            break
    return is_complete





def generate_group(generators):
    res=generators[:]
    for i in generators:
        for j in generators:
            product=i*j
            if product not in res:
                res.append(product)
    return res

def generate_group_recursive(generators):
    res = generate_group(generators)
    if res==generators:
        return res
    else:
        return generate_group_recursive(res)

def membership_check(element,group):
    if element in group:
        return True
    if group==[] or group==[[]]:
        return False

    orbits=[None]*element.n
    traversals=None*element.n
    orbit_nrs=[]
    for nr in range(len(element.P)):
        if element.P[nr]!=nr:
            orb,trans=Orbit(group,nr,True)
            orbits[nr]= orb
            traversals[nr]= trans
            orbit_nrs.append((nr,element.P[nr]))
    non_trivial_orbit_nr=-1
    for orbit_and_image in orbit_nrs:
        if len(orbits[orbit_and_image[0]])>1:
            non_trivial_orbit_nr=orbit_and_image[0]
            break

    group_stabilizer=Stabilizer(group,non_trivial_orbit_nr)

    for orbit_and_image in orbit_nrs:
        orbit_nr=orbit_and_image[0]
        image=orbit_and_image[1]
        traversal_perm=traversals[orbit_nr][image]
        composition_perm=-traversal_perm*element
        if membership_check(composition_perm,group_stabilizer):
            return True



    return False
    # if element in group


def stabilizer_magic(gr_size, orb, trans,stab,permutations_list):
    new_stab=[]
    for stab_element in stab:
        if membership_check(stab_element,permutations_list):
            new_stab.append(stab_element)

    current_stab=new_stab[0]



    first_stab_el=current_stab.cycles()[0][0]
    new_orb,new_trans=Orbit(new_stab,first_stab_el,True)
    next_stab=Stabilizer(new_stab,first_stab_el)

    # if len(new_stab)==0 or len(new_stab)==1:
    #     final_stab_size=len(new_orb)*len(new_stab)
    if next_stab==[]:
        final_stab_size=len(new_orb)
    else:

        final_stab_size=stabilizer_magic(gr_size,new_orb,new_trans,next_stab,permutations_list)


    res=len(orb)*final_stab_size
    return res
#

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

    if Settings.FAST:
        G, H = fast_refinement(G, H)
    else:
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
                # print(P2)
                return P2
            else:
                return None

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
        return None

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
        if not res is None: # if res is not None
            if not res: #if res is empty
                if not [[]] in permutations:
                    permutations.append([[]])
            else:
                if not isinstance(res,permutation):
                    permutations.extend(res)
                else:
                    permutations.append(res.cycles())
                ### this code makes it return to previous instance
                if old_D:
                    if old_D[-1] != old_I[-1]: #if this iteration is not trivial
                        return permutations
                ### uncomment if needed



    return permutations



# def stabilizer_magic2(permutation_list):
#     gr_size=permutation_list[0].n
#     orbits=[]
#     transversals=[]
#     stabilizers=[]
#     non_trivial_orbit=-1
#     for i in range(gr_size):
#         o,trans=Orbit(permutation_list,i,True)
#         if len(o)>1:
#             non_trivial_orbit=i
#         s=Stabilizer(permutation_list,i)
#         orbits.append(o)
#         transversals.append(trans)
#         stabilizers.append(s)
#
#     new_stabilizers=[]
#     current_stabilizers: list[permutation]=stabilizers[non_trivial_orbit]
#     for stab in current_stabilizers:
#
#         for nr in range(gr_size):
#             if stab.P[nr]!=nr:
#                 #todo check if u0->2 ^-1 * f in h
#                 composition = -transversals[nr][stab.P[nr]]*stab
#                 # comp2=
#                 if membership_check(composition,stabilizers[nr]):
#
#
#                     new_stabilizers.append(stab)
#     if new_stabilizers==[]:
#         final_stab_size=1
#     else:
#         current_stab = new_stabilizers[0]
#         if current_stab.cycles==[] or current_stab.cycles()==[[]]:
#             final_stab_size=1
#         else:
#             final_stab_size=stabilizer_magic2([current_stab])
#
#     res = len(orbits[non_trivial_orbit]) * final_stab_size
#     return res


def algebra_magic(input_cycles,gr_size):
    print(input_cycles)

    permutations_list=[]

    a:list = [1,2,3]


    for cycle_composition in input_cycles:


        new_perm_list=[]
        cycle_perm=permutation(gr_size,cycles=cycle_composition)
        is_unique=True

        for cycle in cycle_composition:
            for nr in range(1,len(cycle)):
                try:
                    #todo fix that this doesnt respod well to (0,3)(1,2)
                    orb, trs = Orbit(permutations_list, cycle[nr-1], True)
                    # print("trans:::::" + str(trs))
                    # print("orb:::::" + str(orb))
                    # print("stab::::" + str(Stabilizer(permutations_list, cycle[0])))
                    trans_cycle=trs[orb.index(cycle[nr])]
                    composition_perm=-trans_cycle*cycle_perm
                    # print("composition perm:" + str(composition_perm))
                    # print("permutation list cycles:" + str(permutations_list))
                    if composition_perm in permutations_list: #todo
                        is_unique=False
                        break

                    # new_perm_list.append = (trs(orb.index(cycle[nr])) * cycle)
                    # print("yeahh")

                except ValueError:
                    pass
        # print("new_perm::: " + str(new_perm_list))
        # if trs(orb.index(cycle[1]))*cycle not in Stabilizer(permutations_list,cycle[0]):

        #     pass


        # todo maybe just don't add permutation that is multiple oof 2 other (1,4,5)
        if is_unique:
            permutations_list.append(cycle_perm)




    i=0
    o,trans = Orbit(permutations_list, i,True)
    while len(o)<2:
        i+=1
        o,trans = Orbit(permutations_list, i,True)
    # i=i+1
    print(i)
    s=Stabilizer(permutations_list,i)
    big_perm=generate_group(permutations_list)
    # new_big_perm=[]

    print("permutations: " + str(permutations_list))
    print("big_perm: " + str(big_perm))
    print("orbit: "+ str(o))
    print("stabilizer: "+ str(s)) #todo this is actually a generating set

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

    #todo if dihedral, just use s

    abb=stabilizer_magic(gr_size,o,trans,s,permutations_list)
    # abb=stabilizer_magic2(permutations_list)
    return abb
    # big_s=generate_group(s)
    # # print("big_s: "+  str(big_s))
    #
    # # permutation(3)
    # new_s = []
    # for s_perm in big_s: #just using S works for dihedral groups. generate S recursive works for complete.
    #     cycle_composition=s_perm.cycles()
    #     is_in_generators=False
    #     for cycle in cycle_composition:
    #         for nr in range(0, len(cycle)):
    #             try:
    #
    #
    #
    #                 trans_cycle = trans[o.index(cycle[nr])]
    #                 composition_perm = -trans_cycle * s_perm
    #                 # comp_perm2 = s_perm * -trans_cycle
    #
    #                 if composition_perm in permutations_list:
    #                     is_in_generators = True
    #                     break
    #
    #                 # new_perm_list.append = (trs(orb.index(cycle[nr])) * cycle)
    #                 # print("yeahh")
    #
    #             except ValueError:
    #                 pass
    #     if is_in_generators:
    #         new_s.append(s_perm)
    #
    # print("new_s: " + str(new_s))
    #
    # trivial_perm=permutation(gr_size)
    # if not o:
    #     o=[0]
    # if trivial_perm not in new_s:
    #     new_s.append(trivial_perm)

    # return len(o)*len(new_s)



def count_automorphisms_groups(G1, G2, D,I, G_partition_backup, H_partition_backup):
    cycle_list=automorphisms_cycles(G1, G2, D,I, G_partition_backup, H_partition_backup)
    print("--- finished finding unique permutations ---")
    if cycle_list is None:
        return 0
    elif cycle_list==[]:
        return 1
    elif isinstance(cycle_list,int):
        return cycle_list
    else:
        return algebra_magic(cycle_list,len(G1._v))



if __name__ == '__main__':
    # G1, G2 = load_graphs("graphs/cubes4.grl", 1,1)


    G1=create_graph_with_cycle(5)
    G2=G1


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