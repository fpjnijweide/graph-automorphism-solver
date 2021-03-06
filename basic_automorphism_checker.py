from graph import *
from graph_io import *

from DLL import *


# from week5 import *

def load_graphs(filename: str, nr1: int, nr2: int):
    # loads two graphs from a file, where nr1 and nr2 specify which graphs to load from the file
    with open(filename) as f:
        graph_file = load_graph(f, read_list=True)
        G1 = graph_file[0][nr1]
        G2 = graph_file[0][nr2]
        return G1, G2


def initialize_colors(G: Graph):
    # sets the colornum and label of all vertices to equal to their degree (amount of neighbors)
    for v in G.vertices:
        v.change_color(v.degree)
    G.partition = create_partition(G.vertices)
    return G


def color_refinement(G: Graph, H: Graph):
    # Refine the colors of the graph using colorGraph until the colors are stable (do not change anymore)
    equal = False
    while not equal:
        amount_colors_G = len(G.partition)
        amount_colors_H = len(H.partition)
        refine_colors(G, H)
        new_amount_colors_G = len(G.partition)
        new_amount_colors_H = len(H.partition)
        equal = amount_colors_G == new_amount_colors_G and amount_colors_H == new_amount_colors_H
    return G, H


def create_partition(vertices: list):
    # a list of lists, where the index equals the color and the list at that index is a list of vertices with that color
    partition = []

    for v in vertices:
        # if the degree is not found in partition, add empty lists to it
        add_to_partition(v, partition)

    return partition


def add_to_partition(v: Vertex, partition):
    if v.colornum > len(partition) - 1:
        diff = v.colornum - (len(partition) - 1)
        for i in range(diff):
            partition.append([])
    # add the vertex to its respective index in partition
    partition[v.colornum].append(v)


def create_partition_DLL(vertices: list):
    # a list of lists, where the index equals the color and the list at that index is a list of vertices with that color
    partition = []

    for v in vertices:
        # if the degree is not found in partition, add empty lists to it
        if v.colornum > len(partition) - 1:
            diff = v.colornum - (len(partition) - 1)
            for i in range(diff):
                partition.append(DoubleLinkedList())
        # add the vertex to its respective index in partition
        partition[v.colornum].append(v)

    return partition


def refine_colors(G: Graph, H: Graph):
    # Refines colors

    vertices = G.vertices + H.vertices
    partition = create_partition(vertices)

    # go through vertices with same color
    for i in range(len(partition)):
        vertices_with_this_color = partition[i][:]  # list with vertices of same color
        new_color = len(partition)
        # to create new color for vertices that are not the same as first_vertex

        # now look only at color group of multiple vertices
        if len(vertices_with_this_color) > 1:
            # first_vertex is vertex with smallest sum of colors of neighbours
            first_vertex = vertices_with_this_color[0]

            for other_vertex in vertices_with_this_color:

                if other_vertex._neighbor_colors_sum < first_vertex._neighbor_colors_sum:
                    first_vertex = other_vertex

            vertices_needing_change = []

            for j in range(0, len(vertices_with_this_color)):
                current_vertex = vertices_with_this_color[j]
                if first_vertex != current_vertex:

                    needs_change = False
                    for x in set(first_vertex._neighbor_colors):
                        if current_vertex._neighbor_colors.count(x) != first_vertex._neighbor_colors.count(x):
                            needs_change = True
                            break

                    # if not compare(first_vertex.neighbor_colors, current_vertex.neighbor_colors):
                    if needs_change:
                        vertices_needing_change.append(current_vertex)

            for changing_vertex in vertices_needing_change:
                if new_color == len(partition):
                    partition.append([])
                partition[new_color].append(changing_vertex)
                partition[changing_vertex.colornum].remove(changing_vertex)
                changing_vertex.change_color(new_color)

    G.partition = create_partition(G.vertices)
    H.partition = create_partition(H.vertices)


def write_graph_to_dot_file(G: Graph, title: str):
    with open('graph' + title + '.dot', 'w') as f:
        write_dot(G, f)


def is_stable(g1: Graph, g2: Graph):
    # Returns true as soon as we find 1 isomorphism
    g1.partition = create_partition(g1.vertices)
    g2.partition = create_partition(g2.vertices)
    for i in range(len(g1.partition)):
        # Check if the amount of vertices in this partition are equal in both graphs
        if len(g1.partition[i]) != len(g2.partition[i]):
            return False
    return True


if __name__ == "__main__":
    # main method
    G1, G2 = load_graphs("graphs/bigtrees1.grl", 0, 2)
    G1 = initialize_colors(G1)
    G2 = initialize_colors(G2)
    G1, G2 = color_refinement(G1, G2)
    write_graph_to_dot_file(G1, "G1")
    write_graph_to_dot_file(G2, "G2")
    # render('dot', 'png', 'graphG1.dot')
    # render('dot', 'png', 'graphG2.dot')
    result = is_isomorphic(G1, G2)
    print(result)
