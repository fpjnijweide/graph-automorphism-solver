from graph import *
from week3 import *
from week4 import *
import time
from graphviz import render
from week5 import *
from permv2 import *
from basicpermutationgroup import *
from week2 import *

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

def membership_check(element,group,recursive=True):
    # print("membership check for " + str(element) + " in " + str(group))
    if recursive and element in group:
        # print("TRUE: element is simply in group")
        return True
    if group==[] or group==[[]]:
        # print("FALSE: group is empty")
        return False
    if element==permutation(group[0].n):
        # print("TRUE: trivial perm")
        return True

    orbits=[None]*element.n
    traversals=[None]*element.n
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
    if non_trivial_orbit_nr==-1:
        # print("FALSE: no non trivial orbit")
        return False

    group_stabilizer=Stabilizer(group,non_trivial_orbit_nr)

    for orbit_and_image in orbit_nrs:
        orbit_nr=orbit_and_image[0]
        image=orbit_and_image[1]
        try:
            image_orbit_index=orbits[orbit_nr].index(image)
        except ValueError:
            return False
        traversal_perm=traversals[orbit_nr][image_orbit_index]
        if traversal_perm is not None:
            # traversal_perm=traversals[orbit_nr][image]
            composition_perm = -traversal_perm* element
            if membership_check(composition_perm, group_stabilizer):
                return True
    return False
    # if element in group


def group_size(group):
    nontriv_orbit=-1
    i=0
    while nontriv_orbit==-1:
        orbit,transversals=Orbit(group,i,True)

        if len(orbit)>1:
            nontriv_orbit=i
        else:
            i += 1
    if nontriv_orbit==-1:
        return 1 #todo maybe turn 0
    stab=Stabilizer(group,nontriv_orbit)
    new_stab=[]
    for stab_element in stab:
        # print("starting checking for " + str(stab_element))
        if membership_check(stab_element,group):
            new_stab.append(stab_element)

    if new_stab==[] or new_stab==[[]]:
        final_stab_size=1
    else:

        final_stab_size=group_size(new_stab)

    # print("size of orbit: " + str(len(orbit)))
    res=len(orbit)*final_stab_size
    return res
#

def automorphisms_cycles(G: Graph, H: Graph, D, I, G_partition_backup, H_partition_backup):
    # Recursively counts all isomorphs of this graph

    if not D and Settings.DIHEDRAL_COMPLETE_CUBE_CHECK:
        if len(G._v)==len(H._v):
            if check_dihedral(G) and check_dihedral(H):
                return 2*len(G._v)
            elif check_complete(G) and check_complete(H):
                fact=1

                for i in range(1, len(G._v) + 1):
                    fact = fact * i
                return fact

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

        last_D.change_color(newcol)
        last_I.change_color(newcol)

    # Refine the colors of G and H

    G.partition = create_partition(G.vertices)
    H.partition = create_partition(H.vertices)

    if Settings.FAST:
        G, H = fast_refinement(G, H)
    else:
        G, H = color_refinement(G, H)

    # If this coloring is not stable, return 0
    if not is_stable(G, H):
        return None
    else:
        # Else, check if all colors are unique. If so, it is an isomorph
        all_colors_are_unique = True
        for i in range(len(G.partition)):
            if len(G.partition[i]) > 1 or len(H.partition[i]) > 1:
                all_colors_are_unique = False
                break

### copy this
        if all_colors_are_unique:
            cycle_list2 = list(range(len(G._v)))
            # P = permutation(len(G._v))
            for color in range(len(G.partition)):
                if G.partition[color]:
                    cycle_list2[G._v.index(G.partition[color][0])] = H._v.index(H.partition[color][0])
            P=permutation(len(G._v),mapping=cycle_list2)

            return P
### end copy

    # We have now found a stable coloring that has non-unique colors

    if Settings.PREPROCESSING and not D:  # only once, after first call of fast refignment
        disconnectedG = disconnectedVertices(G)
        for v in disconnectedG:
            G._v.remove(v)
        disconnectedH = disconnectedVertices(H)
        for v in disconnectedH:
            H._v.remove(v)
    if Settings.TREE_CHECK and not D:
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
        i=0
        x = G.partition[chosen_color][i]


    H_partition_chosen_color = H.partition[chosen_color][:]
    permutations=[]

    new_G_partition = G.partition
    new_H_partition = H.partition

    while i<len(H_partition_chosen_color):
    # for y in H_partition_chosen_color:
        y = H_partition_chosen_color[i]
        i+=1
        # if H._v.index(y) in D or H._v.index(y) in I:
        #     continue
        D= old_D[:] + [G._v.index(x)]

        I= old_I[:] + [H._v.index(y)]



        res = automorphisms_cycles(G, H, D, I, new_G_partition,
                                   new_H_partition)
### copy this
        if not res is None: # if res is not None
            # if not res: #if res is empty
            #     if not [[]] in permutations:
            #         permutations.append([[]])
            # else:
            if not isinstance(res,permutation):
                permutations.extend(res)
            else:
                permutations.append(res.cycles())
                ### this code makes it return to previous instance
        if old_D:
            if old_D[-1] != old_I[-1]: #if this iteration is not trivial
                return permutations
                ### uncomment if needed
### end copy



    return permutations

def algebra_magic(input_cycles,gr_size):
    # print(input_cycles)
    permutations_list=[]
    for cycle in input_cycles:
        permutations_list.append(permutation(gr_size,cycle))

    print(permutations_list)
    print("#### ---- starting stabilizer magic ---- #####")
    abb=group_size(permutations_list)
    # abb=stabilizer_magic2(permutations_list)
    return abb

def count_automorphisms_groups(G1, G2, D,I, G_partition_backup, H_partition_backup):
    cycle_list=automorphisms_cycles(G1, G2, D,I, G_partition_backup, H_partition_backup)
    print("--- finished finding unique permutations ---")
    if cycle_list is None:
        return 0
    elif cycle_list==[] or cycle_list==[[]]:
        return 1
    elif isinstance(cycle_list,int):
        return cycle_list
    else:
        return algebra_magic(cycle_list,len(G1._v))



if __name__ == '__main__':
    G1, G2 = load_graphs("graphs/cubes5.grl", 0,0)


    # G1=create_graph_with_cycle(5)
    # G2=G1


    if (G1==G2):
        G2=copy_graph(G2)
    G1 = initialize_colors(G1)
    G2 = initialize_colors(G2)

    # G1,G2=color_refinement(G1,G2)
    # G2=color_refinement(G2)
    G_partition_backup = create_partition(G1.vertices)

    H_partition_backup = create_partition(G2.vertices)
    # print(is_isomorphism(G1,G2))
    print("week 6 answer: "+ str(count_automorphisms_groups(G1, G2, [], [], G_partition_backup, H_partition_backup)))
    # print("real nr: "+ str(count_automorphisms(G1, G2, [], [], G_partition_backup, H_partition_backup)))


    write_graph_to_dot_file(G1, "G1")
    write_graph_to_dot_file(G2, "G2")
    # render('dot', 'png', 'graphG1.dot')
    # render('dot', 'png', 'graphG2.dot')