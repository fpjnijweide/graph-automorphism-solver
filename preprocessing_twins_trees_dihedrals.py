# Preprocessing of twins, dihedrals,  and tree graphs etc.
from permutation import *
from basicpermutationgroup import *

from graph_factory import *
from basic_automorphism_checker import *

from graph import *

from main import *



# from week6 import *

FOUND_TYPE = []

def factorial(nr):
    fact = 1

    for i in range(1, nr + 1):
        fact = fact * i
    return fact


def find_twins(G: Graph):  # will return groups of twins and groups of false twins in a list

    v = G.vertices
    global FOUND_TYPE

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
        FOUND_TYPE.append("Twins")
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
        newVertex = Vertex(G)
        G.add_vertex(newVertex)
        for vertex in range(0, len(i)):
            for e in i[vertex].incidence:
                if e.head == i[vertex]:
                    edge = Edge(e.tail, newVertex)
                    G.add_edge(edge)
                elif e.tail == i[vertex]:
                    edge = Edge(newVertex, e.head)
                    G.add_edge(edge)

    for j in twins_G:
        # if j[x] in G.vertices:
        for i in j:
            G.del_vertex(i)


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
        G._v[i]._neighborset = []
        G._v[i]._neighbor_colors = []
        G._v[i]._neighbor_colors_sum = 0

    # Re-add all edges
    for edge in inputG._e:
        new_edge = Edge(tail=G_copied_vertices[edge.tail], head=G_copied_vertices[edge.head], weight=edge.weight)
        G.add_edge(new_edge)

    return G


def color_by_partition(partition: List):
    for color in range(len(partition)):
        for vertex in partition[color]:
            vertex.change_color(color)


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
                        num = num * factorial(len(q))

        if num > result:
            result = num
    for x in strings:
        result = result * 2
    return result


def compareSubtrees(parent1, parent2, children):  # children of first generation
    comp = True
    sameNeighbors = len(parent1._neighbor_colors) == len(
        parent2._neighbor_colors)  # to check if the parents have the same neighbourhood
    if sameNeighbors:
        for x in set(parent1._neighbor_colors):
            if parent1._neighbor_colors.count(x) != parent2._neighbor_colors.count(x):
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
    is_cycle = True
    global FOUND_TYPE

    for i in range(len(G._v)):
        v = G._v[i]
        if len(v.neighbors) == 2:
            pass
        else:
            is_cycle = False
            break
    if is_cycle:
        FOUND_TYPE.append("Dihedral")
    return is_cycle


def check_cube(G: Graph):
    is_cube = True
    global FOUND_TYPE

    first_degree = G._v[0].degree
    for i in range(len(G._v)):
        v = G._v[i]
        if len(v.neighbors) == first_degree:
            pass
        else:
            is_cube = False
            break
    if is_cube:
        FOUND_TYPE.append("Cube/Torus")
        return first_degree
    else:
        return 0


def check_complete(G: Graph):
    is_complete = True
    G_size = len(G._v)
    global FOUND_TYPE

    for i in range(len(G._v)):
        v = G._v[i]
        if not len(v.neighbors) == G_size - 1:
            is_complete = False
            break
    if is_complete:
        FOUND_TYPE.append("Complete")
    return is_complete


def generate_n_dimensional_cube(degree):
    square = create_graph_with_cycle(4)
    result = create_graph_with_cycle(4)
    for i in range(3, degree + 1):
        # result=result+result
        mapping = {}
        original_size = len(result._v)
        for node in range(original_size):
            new_vertex = Vertex(result)
            mapping[result._v[node]] = new_vertex
            result.add_vertex(new_vertex)

        original_edge_size = len(result._e)
        e_map = {}
        # add all edges
        for node in range(original_size):
            for edge in result._v[node].incidence:
                if edge.head == result._v[node]:
                    result.add_edge(Edge(mapping[edge.tail], mapping[edge.head]))
            result.add_edge(Edge(mapping[result._v[node]], result._v[node]))

        # add new edges

        # result=result+result
        # for i in range(len(result._v)//2):
        #     result._v[i]._graph=result
        #     result._v[i + (len(result) // 2)]._graph=result
        #     result.add_edge(Edge(result._v[i],result._v[i+(len(result)//2)]))
    # write_graph_to_dot_file(G1, "G1")
    # write_graph_to_dot_file(G2, "G2")
    # render('dot', 'png', 'graphG1.dot')
    # render('dot', 'png', 'graphG2.dot')
    return result


def count_automorphisms(G: Graph, H: Graph, D, I, G_partition_backup, H_partition_backup, constant=0,
                        do_not_check_automorphism=False):
    # Recursively counts all isomorphs of this graph
    if not D and (Settings.DIHEDRAL_COMPLETE_CHECK or Settings.CUBE_CHECK):
        if len(G._v) == len(H._v):
            if Settings.DIHEDRAL_COMPLETE_CHECK and check_dihedral(G) and check_dihedral(H):
                return 2 * len(G._v)
            elif Settings.DIHEDRAL_COMPLETE_CHECK and check_complete(G) and check_complete(H):
                fact = 1

                for i in range(1, len(G._v) + 1):
                    fact = fact * i
                return fact
            elif not do_not_check_automorphism and Settings.CUBE_CHECK:
                degree_G = check_cube(G)
                if degree_G != 0:
                    if degree_G == check_cube(H):
                        cube = generate_n_dimensional_cube(degree_G)
                        # cube=copy_graph(cube)
                        cube = initialize_colors(cube)
                        if is_isomorphism(G, copy_graph(cube)):
                            fact = 1

                            for i in range(1, degree_G + 1):
                                fact = fact * i
                            return fact * len(G._v)

    if not D and Settings.TWIN_CHECK and not do_not_check_automorphism:
        twins_G = find_twins(G)
        twins_H = find_twins(H)
        # if len(twins_G)>0 or len(twins_H)>0:
        # print("twins!")
        constantGH = 1
        for i in twins_G:
            constantGH = constantGH * factorial(len(i))
        #print("constant ", constantGH)
        reduce_twins(G, twins_G)
        reduce_twins(H, twins_H)
    elif not D and Settings.TWIN_CHECK and do_not_check_automorphism:
        twins_G = find_twins(G)
        twins_H = find_twins(H)
        constantG = 1
        constantH = 1
        for i in twins_G:
            constantG = constantG * factorial(len(i))
        for j in twins_H:
            constantH = constantH * factorial(len(j))
        if constantG != constantH:
            # print("not iso")
            return False
        elif constantG > 0:

            count = count_automorphisms(G, H, D, I, create_partition(G.vertices), create_partition(H.vertices),
                                        constantG, False)
            #print(count)
            if count > 0:
                # print("iso")
                return True
            else:
                # print("not iso 2")
                return False

            # print("constants", constantG, constantH)
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

        last_D.change_color(newcol)
        last_I.change_color(newcol)

    # Refine the colors of G and H

    if Settings.FAST_REFINEMENT:
        G, H = fast_refinement(G, H)
    else:
        # print("new amount vertices")
        G.partition = create_partition(G.vertices)
        H.partition = create_partition(H.vertices)
        G, H = color_refinement(G, H)

    # If this coloring is not stable, return 0
    if not is_stable(G, H):
        # print("not stable")
        if do_not_check_automorphism or not Settings.ALGEBRA_GROUPS:
            #print("uh oh")
            return 0
        else:
            # print("uh oh2")
            return None
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
            elif not do_not_check_automorphism and Settings.ALGEBRA_GROUPS:
                cycle_list2 = list(range(len(G._v)))
                # P = permutation(len(G._v))
                for color in range(len(G.partition)):
                    if G.partition[color]:
                        cycle_list2[G._v.index(G.partition[color][0])] = H._v.index(H.partition[color][0])
                P = permutation(len(G._v), mapping=cycle_list2)

                return P
            else:
                return 1

    # We have now found a stable coloring that has non-unique colors

    if not D and Settings.PREPROCESSING:  # only once, after first call of refignment
        disconnectedG = disconnectedVertices(G)
        global FOUND_TYPE
        if len(disconnectedG) > 0:
            FOUND_TYPE.append("Disconnected")
        for v in disconnectedG:
            G._v.remove(v)
        disconnectedH = disconnectedVertices(H)
        for v in disconnectedH:
            H._v.remove(v)
    if not D and Settings.TREE_CHECK:
        if isTree(G) and isTree(H):
            FOUND_TYPE.append("Tree")
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
        if not Settings.ALGEBRA_GROUPS or do_not_check_automorphism:
            return 0
        else:
            return None

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

    permutations = []
    for y in H_partition_chosen_color:
        result = count_automorphisms(G, H, D + [G._v.index(x)], I + [H._v.index(y)], new_G_partition,
                                     new_H_partition, constantGH, do_not_check_automorphism=do_not_check_automorphism)
        if not do_not_check_automorphism and Settings.ALGEBRA_GROUPS:
            if not result is None:  # if res is not None
                # if not res: #if res is empty
                #     if not [[]] in permutations:
                #         permutations.append([[]])
                # else:
                if isinstance(result, list):
                    permutations.extend(result)
                else:
                    permutations.append(result)
                    ### this code makes it return to previous instance
            if D:
                if D[-1] != I[-1]:  # if this iteration is not trivial
                    return permutations
        else:
            #print("nr + result", nr_of_isomorphs, result)
            nr_of_isomorphs += result
        if do_not_check_automorphism and nr_of_isomorphs > 0:
            return 1
    if not do_not_check_automorphism and Settings.ALGEBRA_GROUPS:
        return permutations
    else:
        #print("return: ", nr_of_isomorphs)
        return nr_of_isomorphs


def is_isomorphism(G: Graph, H: Graph):
    return count_automorphisms(G, H, [], [], G.partition[:], H.partition[:], do_not_check_automorphism=True) > 0


if __name__ == "__main__":
    G1, G2 = load_graphs("graphs/bigtrees1.grl", 1,3)

    # from week2 import *
    # G1=create_complete_graph(4)
    # G2=create_complete_graph(4)

    if (G1 == G2):
        G2 = copy_graph(G2)
    G1 = initialize_colors(G1)
    G2 = initialize_colors(G2)

    G_partition_backup = create_partition(G1.vertices)
    H_partition_backup = create_partition(G2.vertices)
    print("ans:", count_automorphisms(G1, G2, [], [], G_partition_backup, H_partition_backup, False))
    # print(count_automorphisms(G1, G2, [], [], G_partition_backup, H_partition_backup))

    write_graph_to_dot_file(G1, "G1")
    write_graph_to_dot_file(G2, "G2")

    # DEBUGGING CODE
    # copy to wherever needed
    # write_graph_to_dot_file(G1, "G1")
    # write_graph_to_dot_file(G2, "G2")
    # render('dot', 'png', 'graphG1.dot')
    # render('dot', 'png', 'graphG2.dot')

    # END DEBUGGING CODE
