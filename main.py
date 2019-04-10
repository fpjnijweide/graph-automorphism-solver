from week4 import *
from week5 import *
from week6 import *
filenames=["graphs/basic/basicAut1.gr","graphs/basic/basicAut2.gr","graphs/basic/basicGIAut.grl"]
filenamesGI=["graphs/basic/basicGI1.grl","graphs/basic/basicGI2.grl","graphs/basic/basicGI3.grl"]
FILENAME = "graphs/cographs1.grl"



class Settings:
    AUTOMORPHISMS = True
    FAST_REFINEMENT = False
    PREPROCESSING = False
    TREE_CHECK = False
    TWIN_CHECK= True # Todo fix
    DIHEDRAL_COMPLETE_CUBE_CHECK = False
    ALGEBRA_GROUPS=False
    # group_sizes = {}
    # checked_memberships = {}

# class Struct:




if __name__ == '__main__':

# for FILENAME in filenames:
    start = time.time()
    print("isomorphisms for " + FILENAME)
    with open(FILENAME) as file:
        graphs = load_graph(file, read_list=True)[0]
    notisomorphic = []
    mapped = []

    # Make a copy of all the graphs for the automorphism part since when we have twins we
    # delete vertices in is_isomorphic
    if Settings.AUTOMORPHISMS:
        autographs = []
        for idx in range(0, len(graphs)):
            print(idx)
            autographs.append(copy_graph(graphs[idx]))

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
                if Settings.FAST_REFINEMENT:
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
            graphcopy = copy_graph(autographs[graph])
            autographs[graph] = initialize_colors(autographs[graph])
            graphcopy = initialize_colors(graphcopy)
            g_partition_backup = create_partition(autographs[graph].vertices)
            gcopy_partition_backup = create_partition(graphcopy.vertices)
            if Settings.ALGEBRA_GROUPS:
                automorphisms=count_automorphisms_groups(graphs[graph], graphcopy, [], [],
                                                    g_partition_backup, gcopy_partition_backup)
            else:
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
