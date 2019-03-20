from graph import *
from graph_io import *
from week3 import *
from week5 import *

def is_bijection(G: Graph, H:Graph, D: List[int], I: List[int]):
    res=True
    for i in range(len(D)):
        last_D = G.vertices[D[i]]
        last_I = H.vertices[I[i]]
        for j in range(len(last_D.neighbours)):
            first_neighbour=last_D.neighbours[j]
            second_neighbour=last_I.neighbours[j]
            res=first_neighbour.colornum==second_neighbour.colornum
            if not res:
                break
                        # break


    return res
        # for j in range(len(last_D.neighbours)):
        #     pass

def copy_graph(inputG: Graph):
    G: Graph = copy.copy(inputG)

    G._e=[]

    G_copied_vertices={}

    G._v = inputG._v[:]
    for i in range(len(G._v)):
        G._v[i] = copy.copy(inputG._v[i])
        G._v[i]._graph=G

        G_copied_vertices[inputG._v[i]]=G._v[i]
        G._v[i]._incidence={}


    bcdef=1
    for edge in inputG._e:
        newedge=Edge(tail=G_copied_vertices[edge.tail],head=G_copied_vertices[edge.head],weight=edge.weight)
        G.add_edge(newedge)
    # G._e = inputG._e[:]
    # G_copied_eges={}
    # for i in range(len(G._e)):
    #     G._e[i] = copy.copy(inputG._e[i])
    #     G._e[i]._head=G_copied_vertices[G._e[i]._head]
    #     G._e[i]._tail = G_copied_vertices[G._e[i]._tail]
    #     G_copied_eges[inputG._e[i]]=G._e[i]
    #

    # for i in range(len(G._v)):
    #     G._v[i]._incidence = copy.copy(inputG._v[i]._incidence)
    #     # incidence is a dict that maps vertex -> set of edges
    #     for vertex, edge_set in list(iter(G._v[i]._incidence.items()))[:]:
    #         G._v[i]._incidence[G_copied_vertices[vertex]] = G._v[i]._incidence.pop(vertex)
    #
    #         for edge in list(iter(edge_set))[:]:
    #             edge_set.remove(edge)
    #
    #             new_edge=G_copied_eges[edge]
    #             edge_set.add(new_edge)
    #
    #         #G._v[i]._incidence[new_key] = dictionary.pop(old_key)

    return G

def count_isomorphism(inputG: Graph, inputH: Graph, D, I):
    G=copy_graph(inputG)
    H=copy_graph(inputH)

    if len(D) != 0:
        newcol = len(G.verts)
        i=len(D)-1
        last_D = G.vertices[D[i]]
        last_I = H.vertices[I[i]]


        last_D.colornum = newcol
        last_I.colornum = newcol
        last_D.label = last_D.colornum
        last_I.label = last_I.colornum

    G, H = CRefignment(G, H)


    if not compare_partitions(G, H):
        return 0
    else:
        all_colors_are_unique = True
        for i in range(len(G.verts)):
            if len(G.verts[i]) > 1 or len(H.verts[i]) > 1:
                all_colors_are_unique = False
                break
        if all_colors_are_unique:
            # DEBUGGING CODE
            # copy to wherever needed
            # write_graph_to_dot_file(G, "G1")
            # write_graph_to_dot_file(H, "G2")
            # render('dot', 'png', 'graphG1.dot')
            # render('dot', 'png', 'graphG2.dot')

            # input()
            # END DEBUGGING CODE
            #print(is_bijection(G, H, D, I))
            return 1

    C = -1
    for i in range(len(G.verts)):
        Gcolor = G.verts[i][:]  # list with vertices of same color
        Hcolor = H.verts[i][:]
        if len(Gcolor) + len(Hcolor) >= 4:
            C = i
            break

    if C == -1:
        return 0

    x = G.verts[C][0]

    num = 0

    for y in H.verts[C]:

        num = num + count_isomorphism(G, H, D + [G._v.index(x)], I + [H._v.index(y)])

    return num

def count_isomorphism_fast(inputG: Graph, inputH: Graph, D, I):

    G = copy.copy(inputG)
    G._v = inputG._v[:]
    for i in range(len(G._v)):
        G._v[i] = copy.copy(inputG._v[i])
        G._v[i]._graph=G


    H = copy.copy(inputH)
    H._v = inputH._v[:]
    for i in range(len(H._v)):
        H._v[i] = copy.copy(inputH._v[i])
        H._v[i]._graph = H

    if len(D) != 0:
        newcol = len(G.verts)
        i=len(D)-1
        last_D = G.vertices[D[i]]
        last_I = H.vertices[I[i]]


        last_D.colornum = newcol
        last_I.colornum = newcol
        last_D.label = last_D.colornum
        last_I.label = last_I.colornum

    G, H = fast_refinement(G, H)


    if not compare_partitions(G, H):
        return 0
    else:
        all_colors_are_unique = True
        for i in range(len(G.verts)):
            if len(G.verts[i]) > 1 or len(H.verts[i]) > 1:
                all_colors_are_unique = False
        if all_colors_are_unique:
            return 1

    C = -1
    for i in range(len(G.verts)):
        Gcolor = G.verts[i][:]  # list with vertices of same color
        Hcolor = H.verts[i][:]
        if len(Gcolor) + len(Hcolor) >= 4:
            C = i
            break

    if C == -1:
        return 0

    x = G.verts[C][0]

    num = 0

    for y in H.verts[C]:

        num = num + count_isomorphism_fast(G, H, D + [G._v.index(x)], I + [H._v.index(y)])

    return num


if __name__ == "__main__":
    G1, G2 = load_graphs("graphs/trees36.grl", 3,5)
    G1 = initialize_colors(G1)
    G2 = initialize_colors(G2)
    G1, G2 = CRefignment(G1, G2)
    print(count_isomorphism(G1, G2, [], []))

    '''G1, G2 = load_graphs("graphs/trees36.grl", 3, 5)
    G1 = initialize_colors(G1)
    G2 = initialize_colors(G2)
    G1, G2 = fast_refinement(G1, G2)
    print(compare_partitions(G1, G2))
    print(count_isomorphism_fast(G1, G2, [], []))'''


    write_graph_to_dot_file(G1, "G1")
    write_graph_to_dot_file(G2, "G2")
