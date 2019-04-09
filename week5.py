from graph import *
from week3 import *
from week4 import *
import time
#from graphviz import render


# def neighbors_of_colour(v: Vertex, colour):
#     sum = 0
#     for c in v.neighbor_colors:
#         if c == colour:
#             sum += 1
#     return sum


def fast_refinement(G: Graph, H: Graph):
    partitions = create_partition_DLL(G.vertices + H.vertices)

    for vertex in (G.vertices + H.vertices):
        vertex.neighbor_colors = neighbor_colors(vertex)
        # vertex.neighbors_of_colour={}

    queue = []
    queueindex = 0

    # Add the colour of the first non-empty partition to the queue first
    for current_colour in range(len(partitions)):
        if partitions[current_colour].head is not None:
            queue.append(current_colour)
            break

    # Loop while we have a non-empty queue, each loop will take queue[0] as the colour to compare everything with
    # (how many neighbours of this colour a vertex has)
    k=0
    while queueindex < len(queue):
        k+=1
        # Find all colours of the neighbours of queue[0]
        vertices_col0_dll = partitions[queue[queueindex]]
        colours_neighbouring_queue0 = []

        for v_col0 in vertices_col0_dll:
            for col in v_col0.data.neighbor_colors:
                # if col not in colours_neighbouring_queue0:
                colours_neighbouring_queue0.append(col)

        h=0
        for colour in set(colours_neighbouring_queue0):
            h+=1
            vertices_dll = partitions[colour]

            vertex0 = vertices_dll.head

            # vertex0_neigbors_of_color = neighbors_of_colour(vertex0.data, queue[queueindex])

            group1_int=0
            group2 = []

            for v in vertices_dll:
                # vertex1_neighbors_of_color = neighbors_of_colour(v.data, queue[queueindex])
                # if vertex0_neigbors_of_color == vertex1_neighbors_of_color:
                if vertex0.data.neighbor_colors.count(queue[queueindex])==v.data.neighbor_colors.count(queue[queueindex]):
                    # Has the same number of neighbours with colour queue[0] as vertex0
                    group1_int+=1
                else:
                    group2.append(v.data)
                    vertices_dll.remove(v)

            if len(group2) != 0:
                # Can split the partition based on the number of colour-queue[0] neighbours
                # Change the colour of the vertices in group2, let group1 keep the old colour
                new_colour = len(partitions)
                partitions.append(DoubleLinkedList())
                j=0
                for node in group2:
                    # j+=1
                    partitions[node.colornum].remove(node)
                    # i=0
                    for neighbor in node._neighborset:
                        # try:
                        # i+=1
                        # if node.colornum not in neighbor.neighbor_colors:
                            # pass
                        # neighbor.neighbor_colors.remove(node.colornum)
                        # try:
                        neighbor.neighbor_colors.remove(node.colornum)
                        neighbor.neighbor_colors.append(new_colour)
                        # except ValueError:
                        #     pass
                        # except ValueError:
                        #     pass


                    node.change_color(new_colour)
                    partitions[new_colour].append(node)


                # Change the neighbor_colors stuff since this isn't correct anymore
                # for vtx in vertices_dll:
                #     if queue[queueindex] in vtx.data.neighbor_colors:
                #         vtx.data.neighbor_colors = neighbor_colors(vtx.data)
                # for vtx0 in vertices_col0_dll:
                #     if queue[queueindex] in vtx0.data.neighbor_colors:
                #         vtx0.data.neighbor_colors = neighbor_colors(vtx0.data)

                # Add to queue
                if colour in queue or len(group2) < group1_int:
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
    G1, G2 = load_graphs("graphs/cubes5.grl", 0, 1)

    G1 = initialize_colors(G1)
    G2 = initialize_colors(G2)

    start = time.time()
    G1, G2 = fast_refinement(G1, G2)
    g1_partition_backup = G1.partition[:]
    g2_partition_backup = G2.partition[:]
    #print(is_isomorphic(G1, G2, [], [], g1_partition_backup, g2_partition_backup))

    #print(count_automorphisms(G1, G2, [], [], g1_partition_backup, g2_partition_backup))
    end = time.time()
    print("fast:", end - start)

    G3, G4 = load_graphs("graphs/cubes5.grl", 0, 1)
    G3 = initialize_colors(G3)
    G4 = initialize_colors(G4)
    start = time.time()
    G3, G4 = color_refinement(G3, G4)
    g1_partition_backup = G3.partition[:]
    g2_partition_backup = G4.partition[:]
    #print(is_isomorphic(G3, G4, [], [], g1_partition_backup, g2_partition_backup))

    #print(count_automorphisms(G3, G4, [], [], g1_partition_backup, g2_partition_backup))
    end = time.time()
    print("normal:", end - start)

    write_graph_to_dot_file(G1, "G1")
    write_graph_to_dot_file(G2, "G2")





    # render('dot', 'png', 'graphG1.dot')
    # render('dot', 'png', 'graphG2.dot')