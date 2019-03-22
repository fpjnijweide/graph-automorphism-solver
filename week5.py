from week4 import *
import time


def fast_refinement(G: Graph, H: Graph):
    partition = create_partition(G.vertices + H.vertices)
    queue = []
    for current_color in range(len(partition)):
        if len(partition[current_color]) >= 1:
            queue.append(current_color)
            break

    while len(queue) != 0:
        for color in range(len(partition)): #todo weten we zeker dat dit klopt? Ik zou vanaf nu alleen naar de queue kijken (for i in queue ofzo)
            if len(partition[color]) > 1:
                vertices_of_this_color = partition[color]
                first_vertex=vertices_of_this_color[0]
                queue_color=queue[0]
                first_vertex_neighbor_count = neighbor_colors(first_vertex).count(queue_color)
                vertices_of_color_1 = []
                vertices_of_color_2 = []
                for v in range(1, len(vertices_of_this_color)):
                    current_vertex_neighbor_count = neighbor_colors(vertices_of_this_color[v]).count(queue_color)
                    if current_vertex_neighbor_count == first_vertex_neighbor_count:
                        vertices_of_color_1.append(vertices_of_this_color[v])
                    else:
                        vertices_of_color_2.append(vertices_of_this_color[v])

                if len(vertices_of_color_2) == 0:
                    continue

                amount_of_colors = len(partition)
                for v in vertices_of_color_2: #todo hier opnieuw "v" gebruiken is slecht en kan alleen problemen veroorzaken
                    v.colornum = amount_of_colors

                if color in queue: # todo wtf gebeurt hier lol
                    queue.append(amount_of_colors)
                else:
                    if len(vertices_of_color_1) < len(vertices_of_color_2):
                        queue.append(color)
                    else:
                        queue.append(amount_of_colors)
                partition = create_partition(G.vertices + H.vertices)
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
