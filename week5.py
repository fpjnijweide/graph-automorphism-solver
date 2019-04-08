from graph import *
from week3 import *
from week4 import *
import time
#from graphviz import render


def neighbors_of_colour(v: Vertex, colour):
    sum = 0
    for c in v.neighbor_colors:
        if c == colour:
            sum += 1
    return sum


def fast_refinement(G: Graph, H: Graph):
    partitions = create_partition_DLL(G.vertices + H.vertices)

    for vertex in (G.vertices + H.vertices):
        vertex.neighbor_colors = neighbor_colors(vertex)

    queue = []
    queueindex = 0

    # Add the colour of the first non-empty partition to the queue first
    for current_colour in range(len(partitions)):
        if partitions[current_colour].head is not None:
            queue.append(current_colour)
            break

    # Loop while we have a non-empty queue, each loop will take queue[0] as the colour to compare everything with
    # (how many neighbours of this colour a vertex has)
    while queueindex < len(queue):

        # Find all colours of the neighbours of queue[0]
        vertices_col0_dll = partitions[queue[queueindex]]
        colours_neighbouring_queue0 = []

        for v_col0 in vertices_col0_dll:
            for col in v_col0.data.neighbor_colors:
                if col not in colours_neighbouring_queue0:
                    colours_neighbouring_queue0.append(col)

        for colour in colours_neighbouring_queue0:

            vertices_dll = partitions[colour]

            vertex0 = vertices_dll.head

            num_col0neighbours_group1 = neighbors_of_colour(vertex0.data, queue[queueindex])

            group1 = []
            group2 = []

            for v in vertices_dll:
                num_col0neighbours_group2 = neighbors_of_colour(v.data, queue[queueindex])
                if num_col0neighbours_group2 == num_col0neighbours_group1:
                    # Has the same number of neighbours with colour queue[0] as vertex0
                    group1.append(v.data)
                else:
                    group2.append(v.data)
                    vertices_dll.remove(v)

            if len(group2) != 0:
                # Can split the partition based on the number of colour-queue[0] neighbours
                # Change the colour of the vertices in group2, let group1 keep the old colour
                new_colour = len(partitions)
                partitions.append(DoubleLinkedList())
                for node in group2:
                    node.colornum = new_colour
                    node.label = new_colour
                    partitions[new_colour].append(node)

                # Change the neighbor_colors stuff since this isn't correct anymore
                for vtx in vertices_dll:
                    if queue[queueindex] in vtx.data.neighbor_colors:
                        vtx.data.neighbor_colors = neighbor_colors(vtx.data)
                for vtx0 in vertices_col0_dll:
                    if queue[queueindex] in vtx0.data.neighbor_colors:
                        vtx0.data.neighbor_colors = neighbor_colors(vtx0.data)

                # Add to queue
                if colour in queue or len(group2) < len(group1):
                    addtoqueue = new_colour
                else:
                    addtoqueue = colour
            else:
                addtoqueue = colour

            if addtoqueue not in queue:
                queue.append(addtoqueue)

        queueindex += 1

    G.partition = create_partition(G.vertices)
    H.partition = create_partition(H.vertices)

    return G, H


if __name__ == "__main__":
    # main method
    G1, G2 = load_graphs("graphs/cubes5.grl", 0, 0)

    G1 = initialize_colors(G1)
    G2 = initialize_colors(G2)

    start = time.time()
    G1, G2 = fast_refinement(G1, G2)
    end = time.time()
    print("fast:", end - start)

    '''G3, G4 = load_graphs("graphs/threepaths640.gr", 0, 0)
    G3 = initialize_colors(G3)
    G4 = initialize_colors(G4)
    start = time.time()
    G3, G4 = color_refinement(G3, G4)
    end = time.time()
    print("normal:", end - start)

    write_graph_to_dot_file(G1, "G11")
    write_graph_to_dot_file(G2, "G22")
    #render('dot', 'png', 'graphG11.dot')
    #render('dot', 'png', 'graphG22.dot')'''