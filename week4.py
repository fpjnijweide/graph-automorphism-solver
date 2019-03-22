from week3 import *
# from graphviz import render
# from graphviz import Source
from week5 import *


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


def count_isomorphism(inputG: Graph, inputH: Graph, D, I):
    # Recursively counts all isomorphs of this graph

    # Copy the graphs
    G = copy_graph(inputG)
    H = copy_graph(inputH)

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
    G, H = color_refinement(G, H)

    # If this coloring is not stable, return 0
    if not compare_graphs_by_partition(G, H):
        return 0
    else:
        # Else, check if all colors are unique. If so, it is an isomorph
        all_colors_are_unique = True
        for i in range(len(G.partition)):
            if len(G.partition[i]) > 1 or len(H.partition[i]) > 1:
                all_colors_are_unique = False
                break
        if all_colors_are_unique:
            return 1

    # We have now found a stable coloring that has non-unique colors

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

    # Choose the first vertex of this color in G and check for all y of this color in H
    # if they are isomorphs
    x = G.partition[chosen_color][0]
    nr_of_isomorphs = 0
    for y in H.partition[chosen_color]:
        nr_of_isomorphs += count_isomorphism(G, H, D + [G._v.index(x)], I + [H._v.index(y)])

    return nr_of_isomorphs


if __name__ == "__main__":
    G1, G2 = load_graphs("graphs/cubes5.grl", 0, 0)
    G1 = initialize_colors(G1)
    G2 = initialize_colors(G2)
    G1, G2 = color_refinement(G1, G2)
    # G1,G2=color_refinement(G1,G2)
    print(compare_graphs_by_partition(G1, G2))

    print(count_isomorphism(G1, G2, [], []))
    # DEBUGGING CODE
    # copy to wherever needed
    # write_graph_to_dot_file(G1, "G1")
    # write_graph_to_dot_file(G2, "G2")
    # render('dot', 'png', 'graphG1.dot')
    # render('dot', 'png', 'graphG2.dot')

    # END DEBUGGING CODE
