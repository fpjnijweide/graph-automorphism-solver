from main import *
from week3 import *
from graphviz import render

from week5 import *
from graph import *
import math

def find_twins(G: Graph): # will return groups of twins and groups of false twins in a list
    v = G.vertices

    result = [[v[0]]]
    for i in range(1, len(v)):
        added = False
        for j in result:
            if v[i].neighbors == j[0].neighbors:
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

    return trueResult

def are_twins(v0, v1):
    s1 = set(v1.neighbors)
    difference1 = [x for x in v0.neighbors if x not in s1]  # everything that is in v0.neighbours and not in v1.neighbours
    s2 = set(v0.neighbors)
    difference2 = [x for x in v1.neighbors if x not in s2]  # everything that is in v1.neighbours and not in v0.neighbours

    if difference1 == [v1] and difference2 == [v0]:  # the only difference should be each other when they are true twins
        return True
    return False

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
    # if the tree is in string form, we can return 2
    degree1 = 0
    degreemorethan2 = 0
    for v in G.vertices:
        if v.degree == 1:
            degree1 += 1
        if v.degree > 2:
            degreemorethan2 += 1
    if degree1 == 2 and degreemorethan2 == 0:
        return 2

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
            if len(children[x]) > 1: #children with same parent x, now check the subtrees

                equalChildren = [[children[x][0]]]
                for l in range(1, len(children[x])): # create a list of lists containing subtrees that are equal
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
    return result

def compareSubtrees(parent1, parent2, children): #children of first generation
    comp = True
    sameNeighbors = len(parent1.neighbor_colors) == len(parent2.neighbor_colors) # to check if the parents have the same neighbourhood
    if sameNeighbors:
        for x in set(parent1.neighbor_colors):
            if parent1.neighbor_colors.count(x) != parent2.neighbor_colors.count(x):
                sameNeighbors = False
                break

    if sameNeighbors: # because same neighbourhood, we now have to compare their subtrees
        for x in children[parent1]: # find equal subtree of parent 2 for each subtree of parent 1
            found = False
            for y in children[parent2]:
                found = found or compareSubtrees(x, y, children)
            if not found: # no equal subtree of parent 2 for subtree of parent 1, so not the same
                comp = False
    else: # parents do not have same neighbourhood so subtrees can not be equal
        comp = False
    return comp


def disconnectedVertices(G: Graph): # to return a list of all not connected vertices
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


def count_automorphisms(G: Graph, H: Graph, D, I, G_partition_backup, H_partition_backup):
    # Recursively counts all isomorphs of this graph

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
        # Else, check if all colors are unique. If so, it is an isomorph.
        all_colors_are_unique = True
        for i in range(len(G.partition)):
            if len(G.partition[i]) > 1 or len(H.partition[i]) > 1:
                all_colors_are_unique = False
                break
        if all_colors_are_unique: # everything unique except for groups of twins, when twin check is True.
            return 1

    # We have now found a stable coloring that has non-unique colors

    if Settings.PREPROCESSING and len(D) == 0:  # only once, after first call of fast refinement
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

    # Choose a vertex of this color in G and check for all y of this color in H
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

    for y in H_partition_chosen_color:
        nr_of_isomorphisms += count_automorphisms(G, H, D + [G._v.index(x)], I + [H._v.index(y)], new_G_partition,
                                               new_H_partition)

    return nr_of_isomorphisms

def is_twin(v, list_of_twins):
    result = False
    for i in list_of_twins:
        if v in i:
            result = True
    return result

def count_automorphisms_fast(G: Graph, H: Graph, D, I, G_partition_backup, H_partition_backup):
    # Recursively counts all isomorphs of this graph

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

    G, H = fast_refinement(G, H)

    # If this coloring is not stable, return 0
    if not is_isomorphism(G, H):
        return 0
    else:
        # Else, check if all colors are unique. If so, it is an isomorph. Also we ignore the twins and calculate those in the end when twin check is True.
        if Settings.TWIN_CHECK:
            all_colors_are_unique = True
            twins_G = find_twins(G)
            twins_H = find_twins(H)
            for i in range(len(G.partition)):
                if (len(G.partition[i]) > 1 and G.partition[i] not in twins_G) or (len(H.partition[i]) > 1 and H.partition[i] not in twins_H):
                    all_colors_are_unique = False
                    break
            if all_colors_are_unique:
                result = 1
                for i in twins_G:
                    result = result * math.factorial(len(i))
                return result
        else:
            all_colors_are_unique = True
            for i in range(len(G.partition)):
                if len(G.partition[i]) > 1 or len(H.partition[i]) > 1:
                    all_colors_are_unique = False
                    break
            if all_colors_are_unique:
                return 1

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
    twinsofg = find_twins(G)
    x = None
    if Settings.TWIN_CHECK:  # pick a vertex that is not any kind of twin with a color that is not unique
        for i in G.partition:
            if len(i) > 1:  # color is not unique
                for j in i:
                    if not is_twin(j, twinsofg):
                        chosen_color = j.colornum
                        x = j
    else:
        for i in range(len(G.partition)):
            Gcolor = G.partition[i][:]  # list with vertices of same color
            Hcolor = H.partition[i][:]
            if len(Gcolor) + len(Hcolor) >= 4:
                chosen_color = i
                break
    if chosen_color == -1 and not Settings.TWIN_CHECK:
        # If no color has been chosen something obviously went wrong
        print("ERROR CHOOSING COLOR")
        return 0
    if chosen_color == -1 and Settings.TWIN_CHECK:
        # they are all twins of each other
        print("Fak")


    # if they are isomorphs
    if not Settings.TWIN_CHECK:
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

    twinsofh = find_twins(H)
    for y in H_partition_chosen_color:
        if Settings.TWIN_CHECK:
            if not is_twin(y, twinsofh):
                nr_of_isomorphs += count_automorphisms_fast(G, H, D + [G._v.index(x)], I + [H._v.index(y)], new_G_partition,
                                                       new_H_partition)
        else:
            nr_of_isomorphs += count_automorphisms_fast(G, H, D + [G._v.index(x)], I + [H._v.index(y)], new_G_partition,
                                                   new_H_partition)

    return nr_of_isomorphs


if __name__ == "__main__":
    G1, G2 = load_graphs("graphs/products72.grl", 0, 6)

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
    print(count_automorphisms_fast(G1, G2, [], [], G_partition_backup, H_partition_backup))

    write_graph_to_dot_file(G1, "G1")
    write_graph_to_dot_file(G2, "G2")

'''
bigtrees1:
[0,2] 442368 but gives 110592
[1,3] 5308416 correct fak yesss

bigtrees3:

[0, 2] 2772351862699137701073289910157312 correct fak yeeessssss
[1, 3] 462058643783189616845548318359552 correct whooooopppp
'''


    # DEBUGGING CODE
    # copy to wherever needed
    # write_graph_to_dot_file(G1, "G1")
    # write_graph_to_dot_file(G2, "G2")
    # render('dot', 'png', 'graphG1.dot')
    # render('dot', 'png', 'graphG2.dot')

    # END DEBUGGING CODE
