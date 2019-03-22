from week3 import *
# from graphviz import render
# from graphviz import Source
from week5 import *


def is_bijection(G: Graph, H: Graph, D: List[int], I: List[int]):
    res = True
    for i in range(len(D)):
        last_D = G.vertices[D[i]]
        last_I = H.vertices[I[i]]
        for j in range(len(last_D.neighbors)):
            first_neighbour = last_D.neighbors[j]
            second_neighbour = last_I.neighbors[j]
            res = first_neighbour.colornum == second_neighbour.colornum
            if not res:
                break
                # break
    return res


def copy_graph(inputG: Graph):
    G: Graph = copy.copy(inputG)
    G._e = []
    G_copied_vertices = {}

    G._v = inputG._v[:]
    for i in range(len(G._v)):
        G._v[i] = copy.copy(inputG._v[i])
        G._v[i]._graph = G

        G_copied_vertices[inputG._v[i]] = G._v[i]
        G._v[i]._incidence = {}

    for edge in inputG._e:
        newedge = Edge(tail=G_copied_vertices[edge.tail], head=G_copied_vertices[edge.head], weight=edge.weight)
        G.add_edge(newedge)

    return G


def count_isomorphism(inputG: Graph, inputH: Graph, D, I):
    G = copy_graph(inputG)
    H = copy_graph(inputH)

    if len(D) != 0:
        newcol = len(G.partition)
        i = len(D) - 1
        last_D = G.vertices[D[i]]
        last_I = H.vertices[I[i]]

        last_D.colornum = newcol
        last_I.colornum = newcol
        last_D.label = last_D.colornum
        last_I.label = last_I.colornum

    G, H = fast_refinement(G, H)

    if not compare_graphs_by_partition(G, H):
        return 0
    else:
        all_colors_are_unique = True
        for i in range(len(G.partition)):
            if len(G.partition[i]) > 1 or len(H.partition[i]) > 1:
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
            # print(is_bijection(G, H, D, I))
            return 1

    C = -1
    for i in range(len(G.partition)):
        Gcolor = G.partition[i][:]  # list with vertices of same color
        Hcolor = H.partition[i][:]
        if len(Gcolor) + len(Hcolor) >= 4:
            C = i
            break

    if C == -1:
        return 0

    x = G.partition[C][0]

    num = 0

    for y in H.partition[C]:
        num = num + count_isomorphism(G, H, D + [G._v.index(x)], I + [H._v.index(y)])

    return num


if __name__ == "__main__":
    G1, G2 = load_graphs("graphs/cubes5.grl", 0, 1)
    G1 = initialize_colors(G1)
    G2 = initialize_colors(G2)
    G1, G2 = fast_refinement(G1, G2)
    print(compare_graphs_by_partition(G1, G2))

    print(count_isomorphism(G1, G2, [], []))

    write_graph_to_dot_file(G1, "G1")
    write_graph_to_dot_file(G2, "G2")
