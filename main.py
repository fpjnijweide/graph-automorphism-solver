from week3 import *
from week4 import *
from week5 import *

FILENAME = "graphs/cubes5.grl"


class Settings:
    AUTOMORPHISMS = True
    FAST = False
    PREPROCESSING = False
    TREE_CHECK = True
    TWIN_CHECK= False # Todo sneller maken

    #TODO add a setting for check_dihedral (answer =2*n) and check_complete (answer=n!)


if __name__ == '__main__':
    start = time.time()
    with open(FILENAME) as file:
        graphs = load_graph(file, read_list=True)[0]
    notisomorphic = []
    mapped = []

    # GI problem:
    sys.stdout.write("Sets of isomorphic graphs:")
    isomorphisms = {}
    for graph1 in range(0, len(graphs) - 1):
        if graph1 not in mapped:
            isomorphisms[graph1] = []

            for graph2 in range(graph1 + 1, len(graphs)):
                # Initialisation
                graphs[graph1] = initialize_colors(graphs[graph1])
                graphs[graph2] = initialize_colors(graphs[graph2])

                # Refinement, either colour or fast
                '''if Settings.FAST:
                    graphs[graph1], graphs[graph2] = fast_refinement(graphs[graph1], graphs[graph2])
                else:
                    graphs[graph1], graphs[graph2] = color_refinement(graphs[graph1], graphs[graph2])'''
                g1_partition_backup = graphs[graph1].partition[:]
                g2_partition_backup = graphs[graph2].partition[:]

                if is_isomorphic(graphs[graph1], graphs[graph2], [], [],
                                       g1_partition_backup, g2_partition_backup) > 0:
                    isomorphisms.get(graph1).append(graph2)
                    mapped.append(graph2)

            if len(isomorphisms.get(graph1)) == 0:
                isomorphisms.popitem()
                notisomorphic.append(graph1)

    # Aut problem: only need to calculate for the keys, and graphs not in the dictionary
    if Settings.AUTOMORPHISMS:
        for graph in isomorphisms.keys() or notisomorphic:
            sys.stdout.write('\n')
            graphcopy = copy_graph(graphs[graph])
            graphs[graph]=initialize_colors(graphs[graph])
            graphcopy=initialize_colors(graphcopy)
            g_partition_backup=create_partition(graphs[graph])
            gcopy_partition_backup=create_partition(graphcopy)

            if Settings.FAST:
                # graphs[graph], graphcopy = fast_refinement(graphs[graph], graphcopy)
                # g_partition_backup = graphs[graph].partition[:]
                # gcopy_partition_backup = graphcopy.partition[:]
                automorphisms = count_automorphisms(graphs[graph], graphcopy, [], [],
                                                         g_partition_backup, gcopy_partition_backup, 0)
            else:
                # graphs[graph], graphcopy = color_refinement(graphs[graph], graphcopy)
                # g_partition_backup = graphs[graph].partition[:]
                # gcopy_partition_backup = graphcopy.partition[:]
                automorphisms = count_automorphisms(graphs[graph], graphcopy, [], [],
                                                    g_partition_backup, gcopy_partition_backup, 0)
            if graph in isomorphisms.keys():
                isomorphisms.get(graph).insert(0, graph)
                sys.stdout.write('[' + ', '.join(str(x) for x in isomorphisms.get(graph)) + ']: ' + str(automorphisms))
            else:
                sys.stdout.write(str(graph) + ": " + str(automorphisms))
    else:
        # Print isomorphisms without the number of automorphisms
        for g in isomorphisms.keys():
            isomorphisms.get(g).insert(0, g)
            sys.stdout.write('\n')
            sys.stdout.write('[' + ', '.join(str(x) for x in isomorphisms.get(g)) + ']')

    print(" \n ")
    print(time.time() - start)


