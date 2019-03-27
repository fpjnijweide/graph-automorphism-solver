from week4 import *
from week3 import *
import time
from graphviz import render


def fast_refinement_old(G: Graph, H: Graph):
    partition = create_partition(G.vertices + H.vertices)
    queue = []
    for current_color in range(len(partition)):
        if len(partition[current_color]) >= 1 :
            queue.append(current_color)
            break

    while len(queue) != 0: #todo de queue wordt amper gebruikt..? alleen in queue0
        for partition_color in queue: #todo weten we zeker dat dit klopt? Ik zou vanaf nu alleen naar kleuren in de queue kijken (for i in queue ofzo)
            if len(partition[partition_color]) > 2:
                partition_color_vertices = partition[partition_color]
                vertex0 = partition_color_vertices[0]
                queue0 = queue[0] # todo er wordt uberhaupt eigenlijk niks gedaan met queue0...
                neighbours_vertex0_col0 = neighbor_colors(vertex0).count(queue0)
                # The number of neighbours of the current vertex than have the colour at the start of the queue (above)
                vertices_of_color_1 = []
                vertices_of_color_2 = []
                for v in range(1, len(partition_color_vertices)):
                    current_neighbours_col0 = neighbor_colors(partition_color_vertices[v]).count(queue0)# todo ...behalve hier
                    if current_neighbours_col0 == neighbours_vertex0_col0:
                        vertices_of_color_1.append(partition_color_vertices[v])
                    else:
                        vertices_of_color_2.append(partition_color_vertices[v]) # todo deze regel wordt nooit bereikt, de if-statement is altijd True

                if len(vertices_of_color_2) == 0:
                    continue

                new_color = len(partition)
                for v_col2 in vertices_of_color_2: #todo hier opnieuw "v" gebruiken is slecht en kan alleen problemen veroorzaken
                    # todo deze regels code worden uberhaupt nooit bereikt. vertices_of_color_2 is altijd leeg.
                    v_col2.colornum = new_color
                    v_col2.label = new_color

                if partition_color in queue: # todo wtf gebeurt hier lol waarom wordt partition_color weer gebruikt
                    queue.append(new_color)
                else:
                    if len(vertices_of_color_1) < len(vertices_of_color_2):
                        queue.append(partition_color)
                    else:
                        queue.append(new_color)
                #partition = create_partition(G.vertices + H.vertices) # todo dit heeft geen effect op de rest van de for-loop van regel 14, is dat de bedoeling?
        queue.pop(0)
    G.partition = create_partition(G.vertices)
    H.partition = create_partition(H.vertices)
    return G, H


def fast_refinement(G: Graph, H: Graph):
    partitions = create_partition(G.vertices + H.vertices)
    queue = []

    # Add the colour of the first non-empty partition to the queue first
    for current_colour in range(len(partitions)):
        if len(partitions[current_colour]) > 0:
            queue.append(current_colour)
            break

    # Loop while we have a non-empty queue, each loop will take queue[0] as the colour to compare everything with
    # (how many neighbours of this colour a vertex has)
    while len(queue) != 0:
        # Find all colours of the neighbours of queue[0]
        vertices_col0 = partitions[queue[0]]
        colours_neighbouring_queue0 = []
        for v_col0 in vertices_col0:
            for n in v_col0.neighbors:
                if n.colornum not in colours_neighbouring_queue0:
                    colours_neighbouring_queue0.append(n.colornum)

        for colour in colours_neighbouring_queue0:
            vertices = partitions[colour]

            # Empty partition - no vertices with this colour
            '''if len(vertices) == 0:
                continue'''

            vertex0 = vertices[0]

            num_col0neighbours_group1 = neighbor_colors(vertex0).count(queue[0])

            group1 = []
            group2 = []

            for v in vertices:
                if neighbor_colors(v).count(queue[0]) == num_col0neighbours_group1:
                    # Has the same number of neighbours with colour queue[0] as vertex0
                    group1.append(v)
                else:
                    group2.append(v)

            if len(group2) != 0:
                # Can split the partition based on the number of colour-queue[0] neighbours
                # Change the colour of the vertices in group2, let group1 keep the old colour
                new_colour = len(partitions)
                for vertex in group2:
                    vertex.colornum = new_colour
                    vertex.label = new_colour

            # Add/remove from queue
            if colour in queue or (len(group2) != 0 and len(group2) < len(group1)):
                queue.append(new_colour)
            else:
                queue.append(colour)

        queue.pop(0)

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

    write_graph_to_dot_file(G1, "G2")
    write_graph_to_dot_file(G3, "G4")
    render('dot', 'png', 'graphG2.dot')
    render('dot', 'png', 'graphG4.dot')