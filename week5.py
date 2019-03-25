from week4 import *
from week3 import *
import time


def fast_refinement(G: Graph, H: Graph):
    partition = create_partition(G.vertices + H.vertices)
    queue = []
    for current_color in range(len(partition)):
        if len(partition[current_color]) >= 1:
            queue.append(current_color)
            break

    while len(queue) != 0: #todo de queue wordt amper gebruikt..? alleen in first_color_in_queue
        for partition_color in range(len(partition)): #todo weten we zeker dat dit klopt? Ik zou vanaf nu alleen naar kleuren in de queue kijken (for i in queue ofzo)
            if len(partition[partition_color]) > 1:
                partition_color_vertices = partition[partition_color]
                first_partition_color_vertex=partition_color_vertices[0]
                first_color_in_queue=queue[0] # todo er wordt uberhaupt eigenlijk niks gedaan met first_color_in_queue...
                first_partition_color_vertex_neighbor_count = neighbor_colors(first_partition_color_vertex).count(first_color_in_queue)
                vertices_of_color_1 = []
                vertices_of_color_2 = []
                for v in range(1, len(partition_color_vertices)):
                    current_vertex_neighbor_count = neighbor_colors(partition_color_vertices[v]).count(first_color_in_queue)# todo ...behalve hier
                    if current_vertex_neighbor_count == first_partition_color_vertex_neighbor_count:
                        vertices_of_color_1.append(partition_color_vertices[v])
                    else:
                        vertices_of_color_2.append(partition_color_vertices[v]) # todo deze regel wordt nooit bereikt, de if-statement is altijd True

                if len(vertices_of_color_2) == 0:
                    continue

                new_color = len(partition)
                for v in vertices_of_color_2: #todo hier opnieuw "v" gebruiken is slecht en kan alleen problemen veroorzaken
                    # todo deze regels code worden uberhaupt nooit bereikt. vertices_of_color_2 is altijd leeg.
                    v.colornum = new_color
                    v.label=new_color

                if partition_color in queue: # todo wtf gebeurt hier lol waarom wordt partition_color weer gebruikt
                    queue.append(new_color)
                else:
                    if len(vertices_of_color_1) < len(vertices_of_color_2):
                        queue.append(partition_color)
                    else:
                        queue.append(new_color)
                partition = create_partition(G.vertices + H.vertices) # todo dit heeft geen effect op de rest van de for-loop van regel 14, is dat de bedoeling?
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

    write_graph_to_dot_file(G1, "G1")
    write_graph_to_dot_file(G3, "G2")
    # render('dot', 'png', 'graphG1.dot')
    # render('dot', 'png', 'graphG2.dot')