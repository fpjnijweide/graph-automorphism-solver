from main import *
from week3 import *
#from graphviz import render
from graph import *
import math


def find_twins(G: Graph):  # will return groups of twins and groups of false twins in a list
    v = G.vertices

    result = [[v[0]]]
    for i in range(1, len(v)):
        added = False
        for j in result:
            if set(v[i]._neighborset).symmetric_difference(set(j[0]._neighborset)) == set([]):
                j.append(v[i])
                added = True
            elif are_twins(v[i], j[0]):
                j.append(v[i])
                added = True
        if not added:
            result.append([v[i]])

    trueResult = []
    for i in result:
        if len(i) > 1:
            trueResult.append(i)
    if len(trueResult) > 0:
        Settings.FOUND_TYPE = "Twins"

    return trueResult


def are_twins(v0, v1):
    s1 = set(v1._neighborset)
    s2 = set(v0._neighborset)
    s3 = s1.symmetric_difference(s2)

    if v0 in s3 and v1 in s3 and len(s3) == 2:  # the only difference should be each other when they are true twins
        return True
    return False


def reduce_twins(G: Graph, twins_G):
    # we keep one of the twins with index 0, all others will be deleted and their edges will be added to the twin that is kept.
    for i in twins_G:
        for vertex in range(1, len(i)):
            for e in i[vertex].incidence:
                if (e.head == i[vertex] and e.tail in i) or (e.tail == i[vertex] and e.head in i): # connection between true twins can be left out
                    break
                else:
                    if e.head == i[vertex]:
                        edge = Edge(e.tail, i[0])
                        G.add_edge(edge)
                    elif e.tail == i[vertex]:
                        edge = Edge(i[0], e.head)
                        G.add_edge(edge)

    for j in twins_G:
        for x in range(1, len(j)):
            if j[x] in G.vertices:
                G.del_vertex(j[x])


def copy_graph(inputG: Graph):
    # Copies a graph

    G: Graph = copy.copy(inputG)  # Shallow copy it

    G._e = []  # Delete its edges

    G_copied_vertices = {}  # Dictionary to go from old vertex to new vertex

    # Copying vertices
    G._v = inputG._v[:]  # Copy list of vertices
    for i in range(len(G._v)):
        G._v[i] = copy.copy(inputG._v[i])  # Copying each vertex individually
        G._v[i]._graph = G  # Set its graph attribute to the new graph

        G_copied_vertices[inputG._v[i]] = G._v[i]  # Add it to the dictionary
        G._v[i]._incidence = {}  # Reset its incidence
        G._v[i]._neighborset=[]

    # Re-add all edges
    for edge in inputG._e:
        new_edge = Edge(tail=G_copied_vertices[edge.tail], head=G_copied_vertices[edge.head], weight=edge.weight)
        G.add_edge(new_edge)


    return G


def color_by_partition(partition: List):
    for color in range(len(partition)):
        for vertex in partition[color]:
            vertex.colornum = color
            vertex.label = color


def countTreeIsomorphism(G: Graph):
    # if the tree contains string form, we can remove it and multiply result by amount of strings times 2
    degree1 = []
    strings = []
    for v in G.vertices:
        if v.degree == 1:
            degree1.append(v)
    for w in degree1:
        next = w.neighbors
        string = [w]
        while len(next) != 0:
            check = next.pop(0)
            string.append(check)
            if len(check.neighbors) > 2:
                break
            else:
                for x in check.neighbors:
                    if x not in string:
                        next.append(x)
        if string[0] in degree1 and string[len(string) - 1] in degree1:
            strings.append(string)
            degree1.remove(string[0])
            degree1.remove(string[len(string) - 1])
            for z in string:
                G.del_vertex(z)

    result = 1  # result depends on position of the root, so we check for every vertex as root
    for v in G.vertices:
        root = v  # root
        children = dict()  # parent points to array of its children

        visited = []  # fill the dictionary by breath first search
        next = [root]
        while len(next) != 0:
            inspect = next.pop(0)
            visited.append(inspect)
            if len(inspect.neighbors) > 0:
                children[inspect] = []
                for x in inspect.neighbors:
                    if x not in visited:
                        next.append(x)
                        children[inspect].append(x)

        num = 1
        for x in children:
            if len(children[x]) > 1:  # children with same parent x, now check the subtrees

                equalChildren = [[children[x][0]]]
                for l in range(1, len(children[x])):  # create a list of lists containing subtrees that are equal
                    addedToEqualChildren = False
                    for m in equalChildren:
                        if compareSubtrees(m[0], children[x][l], children):
                            m.append(children[x][l])
                            addedToEqualChildren = True
                    if not addedToEqualChildren:
                        equalChildren.append([children[x][l]])

                for q in equalChildren:
                    if len(q) > 1:
                        num = num * math.factorial(len(q))

        if num > result:
            result = num
    for x in strings:
       result = result * 2
    return result


def compareSubtrees(parent1, parent2, children):  # children of first generation
    comp = True
    sameNeighbors = len(parent1.neighbor_colors) == len(
        parent2.neighbor_colors)  # to check if the parents have the same neighbourhood
    if sameNeighbors:
        for x in set(parent1.neighbor_colors):
            if parent1.neighbor_colors.count(x) != parent2.neighbor_colors.count(x):
                sameNeighbors = False
                break

    if sameNeighbors:  # because same neighbourhood, we now have to compare their subtrees
        for x in children[parent1]:  # find equal subtree of parent 2 for each subtree of parent 1
            found = False
            for y in children[parent2]:
                found = found or compareSubtrees(x, y, children)
            if not found:  # no equal subtree of parent 2 for subtree of parent 1, so not the same
                comp = False
    else:  # parents do not have same neighbourhood so subtrees can not be equal
        comp = False
    return comp


def disconnectedVertices(G: Graph):  # to return a list of all not connected vertices
    disconnected = []
    for v in G.vertices:
        if v.degree == 0:
            disconnected.append(v)
    return disconnected


def isTree(G: Graph):
    vertices = G.vertices
    queue = []
    visited = []
    # add first vertex to queue en make it true so visited
    queue.append([vertices[0], vertices[0]])
    visited.append(vertices[0])
    while len(queue) != 0:
        v = queue.pop()
        for w in v[0].neighbors:
            if w not in visited:
                queue.insert(0, [w, v[0]])
                visited.insert(0, w)
            else:
                if w != v[1]:
                    return False
    return True


def is_twin(v, list_of_twins):
    result = False
    for i in list_of_twins:
        if v in i:
            result = True
    return result

def check_dihedral(G: Graph):

    is_cycle=True

    for i in range(len(G._v)):
        v=G._v[i]
        if len(v.neighbors)==2:
            pass
        else:
            is_cycle=False
            break
    if is_cycle:
        Settings.FOUND_TYPE+="Dihedral"
    return is_cycle

def check_complete(G: Graph):
    is_complete=True
    G_size=len(G._v)
    for i in range(len(G._v)):
        v = G._v[i]
        if not len(v.neighbors)==G_size-1:
            is_complete=False
            break
    if is_complete:
        Settings.FOUND_TYPE+="Complete"
    return is_complete

def count_automorphisms(G: Graph, H: Graph, D, I, G_partition_backup, H_partition_backup, constant=0):
    # Recursively counts all isomorphs of this graph

    if not D and Settings.DIHEDRAL_COMPLETE_CHECK:
        if len(G._v)==len(H._v):
            if check_dihedral(G) and check_dihedral(H):
                return 2*len(G._v)
            elif check_complete(G) and check_complete(H):
                fact=1

                for i in range(1, len(G._v) + 1):
                    fact = fact * i
                return fact


    if not D and Settings.TWIN_CHECK:
        twins_G = find_twins(G)
        twins_H = find_twins(H)
        constantGH = 1
        for i in twins_G:
            constantGH = constantGH * math.factorial(len(i))
        reduce_twins(G, twins_G)
        reduce_twins(H, twins_H)
    else:
        constantGH = constant

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

    if Settings.FAST:
        G, H = fast_refinement(G, H)
    else:
        G.partition = create_partition(G.vertices)
        H.partition = create_partition(H.vertices)
        G, H = color_refinement(G, H)

    # If this coloring is not stable, return 0
    if not is_stable(G, H):
        return 0
    else:
        # Else, check if all colors are unique. If so, it is an isomorph. Also we ignore the twins and calculate those
        # in the end when twin check is True.
        all_colors_are_unique = True
        for i in range(len(G.partition)):
            if len(G.partition[i]) > 1 or len(H.partition[i]) > 1:
                all_colors_are_unique = False
                break
        if all_colors_are_unique:
            if Settings.TWIN_CHECK:
                return 1 * constantGH
            else:
                return 1

    # We have now found a stable coloring that has non-unique colors

    if not D and Settings.PREPROCESSING:  # only once, after first call of refignment
        disconnectedG = disconnectedVertices(G)
        if len(disconnectedG) > 0:
            Settings.FOUND_TYPE = "Disconnected"
        for v in disconnectedG:
            G._v.remove(v)
        disconnectedH = disconnectedVertices(H)
        for v in disconnectedH:
            H._v.remove(v)
    if not D and Settings.TREE_CHECK:
        if isTree(G) and isTree(H):
            Settings.FOUND_TYPE = "Tree"
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
        print("ERROR CHOOSING COLOR")
        return 0

    # if they are isomorphs

    x = G.partition[chosen_color][0]
    H_partition_chosen_color = H.partition[chosen_color][:]
    nr_of_isomorphs = 0

    new_G_partition = G.partition
    new_H_partition = H.partition
    # color_by_partition(G_partition_backup)
    # color_by_partition(H_partition_backup)
    #
    # G.partition = G_partition_backup
    # H.partition = H_partition_backup

    for y in H_partition_chosen_color:
        nr_of_isomorphs += count_automorphisms(G, H, D + [G._v.index(x)], I + [H._v.index(y)], new_G_partition,
                                               new_H_partition, constantGH)
    return nr_of_isomorphs


def is_isomorphic(G: Graph, H: Graph, D, I, G_partition_backup, H_partition_backup):
    # Returns true as soon as we find an isomorphism (count_automorphism maar dan anders)
    if Settings.TWIN_CHECK and len(D) == 0:
        twins_G = find_twins(G)
        twins_H = find_twins(H)
        constantG = 1
        constantH = 1
        for i in twins_G:
            constantG = constantG * math.factorial(len(i))
        for j in twins_H:
            constantH = constantH * math.factorial(len(j))
        reduce_twins(G, twins_G)
        reduce_twins(H, twins_H)

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

    if Settings.FAST:
        G, H = fast_refinement(G, H)
    else:
        G.partition = create_partition(G.vertices)
        H.partition = create_partition(H.vertices)
        G, H = color_refinement(G, H)

    # If this coloring is not stable, return 0
    if not is_stable(G, H):
        return 0
    else:
        # Else, check if all colors are unique. If so, it is an isomorph. Also we ignore the twins and calculate those in the end when twin check is True.
        all_colors_are_unique = True
        for i in range(len(G.partition)):
            if len(G.partition[i]) > 1 or len(H.partition[i]) > 1:
                all_colors_are_unique = False
                break
        if all_colors_are_unique:
            return 1

    # We have now found a stable coloring that has non-unique colors

    if Settings.PREPROCESSING and not D:  # only once, after first call of refignment
        disconnectedG = disconnectedVertices(G)
        for v in disconnectedG:
            G._v.remove(v)
        disconnectedH = disconnectedVertices(H)
        for v in disconnectedH:
            H._v.remove(v)
    if Settings.TREE_CHECK and not D:
        if isTree(G) and isTree(H):
            Settings.FOUND_TYPE = "Tree"
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
        print("ERROR CHOOSING COLOR")
        return 0

    # if they are isomorphs

    x = G.partition[chosen_color][0]
    H_partition_chosen_color = H.partition[chosen_color][:]
    nr_of_isomorphs = 0

    new_G_partition = G.partition
    new_H_partition = H.partition
    # color_by_partition(G_partition_backup)
    # color_by_partition(H_partition_backup)
    #
    # G.partition = G_partition_backup
    # H.partition = H_partition_backup

    for y in H_partition_chosen_color:
        if (nr_of_isomorphs > 0):
            return True
        else:
            nr_of_isomorphs += count_automorphisms(G, H, D + [G._v.index(x)], I + [H._v.index(y)], new_G_partition,
                                               new_H_partition)
    return False


if __name__ == "__main__":
    G1, G2 = load_graphs("graphs/cubes5.grl", 0, 0)

    # from week2 import *
    # G1=create_complete_graph(4)
    # G2=create_complete_graph(4)

    if (G1 == G2):
        G2 = copy_graph(G2)
    G1 = initialize_colors(G1)
    G2 = initialize_colors(G2)


    G_partition_backup = create_partition(G1.vertices)
    H_partition_backup = create_partition(G2.vertices)
    # print(is_isomorphic(G1, G2))
    print(count_automorphisms(G1, G2, [], [], G_partition_backup, H_partition_backup, 0))

    write_graph_to_dot_file(G1, "G1")
    write_graph_to_dot_file(G2, "G2")

    # DEBUGGING CODE
    # copy to wherever needed
    # write_graph_to_dot_file(G1, "G1")
    # write_graph_to_dot_file(G2, "G2")
    #render('dot', 'png', 'graphG1.dot')
    #render('dot', 'png', 'graphG2.dot')

    # END DEBUGGING CODE
