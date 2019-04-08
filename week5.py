from week3 import *
import time
#from graphviz import render


def fast_refinement(G: Graph, H: Graph):
    partitions = create_partition_DLL(G.vertices + H.vertices)

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
            for n in v_col0.neighbors:
                if n.colornum not in colours_neighbouring_queue0:
                    colours_neighbouring_queue0.append(n.colornum)

        for colour in colours_neighbouring_queue0:

            vertices_dll = partitions[colour]
            print(vertices_dll)

            # Empty partition - no vertices with this colour
            '''if len(vertices) == 0:
                continue'''

            vertex0 = vertices_dll.head

            num_col0neighbours_group1 = neighbor_colors(vertex0.data).count(queue[queueindex])

            group1 = []
            group2 = []

            for v in vertices_dll:
                if neighbor_colors(v).count(queue[queueindex]) == num_col0neighbours_group1:
                    # Has the same number of neighbours with colour queue[0] as vertex0
                    group1.append(v)
                else:
                    group2.append(v)
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
    G1, G2 = load_graphs("graphs/threepaths5.gr", 0, 0)

    G1 = initialize_colors(G1)
    G2 = initialize_colors(G2)

    start = time.time()
    G1, G2 = fast_refinement(G1, G2)
    end = time.time()
    print("fast:", end - start)

    G3, G4 = load_graphs("graphs/threepaths5.gr", 0, 0)
    G3 = initialize_colors(G3)
    G4 = initialize_colors(G4)
    start = time.time()
    G3, G4 = color_refinement(G3, G4)
    end = time.time()
    print("normal:", end - start)

    write_graph_to_dot_file(G1, "G1")
    write_graph_to_dot_file(G3, "G2")
    render('dot', 'png', 'graphG1.dot')
    render('dot', 'png', 'graphG2.dot')