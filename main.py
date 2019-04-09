from week4 import *
from week5 import *

FILENAME = "graphs/Isom1.grl"

class Settings:
    AUTOMORPHISMS = False
    FAST = True
    PREPROCESSING = True
    TREE_CHECK = True
    TWIN_CHECK= False # Todo sneller maken
    DIHEDRAL_COMPLETE_CUBE_CHECK = True




if __name__ == '__main__':
    start = time.time()
    print("isomorphisms for {}\n".format(FILENAME.split('/')[1]))
    with open(FILENAME) as file:
        graphs = load_graph(file, read_list=True)[0]
    notisomorphic = []
    mapped = []
    #TODO: we need a graph copy
    # GI problem:
    isomorphisms = {}
    for graph1 in range(0, len(graphs)):
        if graph1 not in mapped:
            isomorphisms[graph1] = []

            for graph2 in range(graph1 + 1, len(graphs)):
                # Initialisation
                graphs[graph1] = initialize_colors(graphs[graph1])
                graphs[graph2] = initialize_colors(graphs[graph2])

                # Refinement, either colour or fast
                if Settings.FAST:
                    graphs[graph1], graphs[graph2] = fast_refinement(graphs[graph1], graphs[graph2])
                else:
                    graphs[graph1], graphs[graph2] = color_refinement(graphs[graph1], graphs[graph2])
                # g1_partition_backup = graphs[graph1].partition[:]
                # g2_partition_backup = graphs[graph2].partition[:]

                if is_isomorphism(graphs[graph1],graphs[graph2]):
                    isomorphisms.get(graph1).append(graph2)
                    mapped.append(graph2)

            if len(isomorphisms.get(graph1)) == 0:
                isomorphisms.popitem()
                notisomorphic.append(graph1)
    # Aut problem: only need to calculate for the keys, and graphs not in the dictionary
    if Settings.AUTOMORPHISMS:
        print('{:>}   {:<}'.format("Sets of isomorphic graphs:", "Number of automorphisms:"))
        for graph in isomorphisms.keys() or notisomorphic:
            graphcopy = copy_graph(graphs[graph])
            graphs[graph] = initialize_colors(graphs[graph])
            graphcopy = initialize_colors(graphcopy)
            g_partition_backup = create_partition(graphs[graph].vertices)
            gcopy_partition_backup = create_partition(graphcopy.vertices)

            automorphisms = count_automorphisms(graphs[graph], graphcopy, [], [],
                                                    g_partition_backup, gcopy_partition_backup)
            if graph in isomorphisms.keys():
                isomorphisms.get(graph).insert(0, graph)
                graph_str = "[" + ', '.join(str(x) for x in isomorphisms.get(graph)) + "]"
                print('{:>26}   {:<}'.format(graph_str, automorphisms))
            else:
                print('{:>26}   {:<}'.format(str(graph), automorphisms))
    else:
        print('{:>}'.format("Sets of isomorphic graphs:"))
        # Print isomorphisms without the number of automorphisms
        if len(isomorphisms.keys()) == 0:
            print("There are no isomorphic graphs")
        for g in isomorphisms.keys():
            isomorphisms.get(g).insert(0, g)
            graph_str = "[" + ', '.join(str(x) for x in isomorphisms.get(g)) + "]"
            print('{:>26}'.format(graph_str))

    print("\n" + '{:>20} {:.2f}s'.format("time it took:", time.time() - start))
    if len(FOUND_TYPE) >= 1:
        print("type of graph found: {:>}".format(", ".join(i for i in set(FOUND_TYPE))))
