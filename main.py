from week5 import *
from week4 import *
from week3 import *

FILENAME = "graphs/trees36.grl"

class Settings:
    FAST = False
    PREPROCESSING = False
    TREE_CHECK = False

if __name__ == '__main__':
    with open(FILENAME) as file:
        graphs = load_graph(file, read_list=True)[0]
    notisomorphic = []
    mapped = []

    # GI problem:
    sys.stdout.write("Sets of isomorphic graphs and number of automorphisms:")

    isomorphisms = {}
    for graph1 in range(0, len(graphs) - 1):
        if graph1 not in mapped:
            isomorphisms[graph1] = []

            for graph2 in range(graph1 + 1, len(graphs)):
                # Initialisation
                graphs[graph1] = initialize_colors(graphs[graph1])
                graphs[graph2] = initialize_colors(graphs[graph2])

                # Refinement, either colour or fast
                if Settings.FAST:
                    graphs[graph1], graphs[graph2] = fast_refinement(graphs[graph1], graphs[graph2])
                    g1_partition_backup = graphs[graph1].partition[:]
                    g2_partition_backup = graphs[graph2].partition[:]

                    if count_automorphisms_fast(graphs[graph1], graphs[graph2], [], [],
                                                g1_partition_backup, g2_partition_backup) > 0:
                        isomorphisms.get(graph1).append(graph2)
                        mapped.append(graph2)
                else:
                    graphs[graph1], graphs[graph2] = color_refinement(graphs[graph1], graphs[graph2])
                    g1_partition_backup = graphs[graph1].partition[:]
                    g2_partition_backup = graphs[graph2].partition[:]

                    if count_automorphisms(graphs[graph1], graphs[graph2], [], [],
                                           g1_partition_backup, g2_partition_backup) > 0:
                        isomorphisms.get(graph1).append(graph2)
                        mapped.append(graph2)

            if len(isomorphisms.get(graph1)) == 0:
                isomorphisms.popitem()
                notisomorphic.append(graph1)

    # Aut problem: only need to calculate for the keys, and graphs not in the dictionary
    for graph in isomorphisms.keys() or notisomorphic:
        sys.stdout.write('\n')
        graphcopy = copy_graph(graphs[graph])
        if Settings.FAST:
            graphs[graph], graphcopy = fast_refinement(graphs[graph], graphcopy)
            g_partition_backup = graphs[graph].partition[:]
            gcopy_partition_backup = graphcopy.partition[:]
            automorphisms = count_automorphisms_fast(graphs[graph], graphcopy, [], [],
                                                     g_partition_backup, gcopy_partition_backup)
        else:
            graphs[graph], graphcopy = color_refinement(graphs[graph], graphcopy)
            g_partition_backup = graphs[graph].partition[:]
            gcopy_partition_backup = graphcopy.partition[:]
            automorphisms = count_automorphisms(graphs[graph], graphcopy, [], [],
                                                g_partition_backup, gcopy_partition_backup)
        if graph in isomorphisms.keys():
            isomorphisms.get(graph).insert(0, graph)
            sys.stdout.write('[' + ', '.join(str(x) for x in isomorphisms.get(graph)) + ']: ' + str(automorphisms))
        else:
            sys.stdout.write(str(graph) + ": " + str(automorphisms))




