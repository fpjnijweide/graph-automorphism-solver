from graph import *
from graph_io import *
from week3 import *
from week4 import *

def fast_refinement(G: Graph, H: Graph):
    c = create_verts(G.vertices + H.vertices)
    queue = []
    for i in range(len(c)):
        if len(c[i]) >= 1:
            queue.append(i)
            break
    while len(queue) != 0:
        for i in range(len(c)):
            if len(c[i]) > 1:
                list_same_color = c[i]
                amount_v0 = colorNeighbours(list_same_color[0]).count(queue[0])
                c1 = []
                c2 = []
                for v in range(1, len(list_same_color)):
                    amount_v = colorNeighbours(list_same_color[v]).count(queue[0])
                    if amount_v == amount_v0:
                        c1.append(list_same_color[v])
                    else:
                        c2.append(list_same_color[v])

                if len(c2) == 0:
                    continue

                l = len(c)
                for v in c2:
                    v.colornum = l

                if i in queue:
                    queue.append(l)
                else:
                    if len(c1) < len(c2):
                        queue.append(i)
                    else:
                        queue.append(l)
                c = create_verts(G.vertices + H.vertices)

        queue.pop(0)
    return G, H
if __name__ == "__main__":
    # main method
    G1, G2 = load_graphs("graphs/trees36.grl", 0, 7)
    G1 = initialize_colors(G1)
    G2 = initialize_colors(G2)
    G1, G2 = fast_refinement(G1, G2)
    write_graph_to_dot_file(G1, "G1")
    write_graph_to_dot_file(G2, "G2")
    result = compare_partitions(G1, G2)
    print(result)






#def refine_operation():



