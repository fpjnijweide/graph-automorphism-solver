from week5 import *
from week4 import *
from week3 import *

FILENAME = "graphs/trees36.grl"
FAST = False


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
                if FAST:
                    print("go fast")
                    graphs[graph1], graphs[graph2] = fast_refinement(graphs[graph1], graphs[graph2])

                    if count_isomorphism_fast(graphs[graph1], graphs[graph2], [], []) > 0:
                        isomorphisms.get(graph1).append(graph2)
                        mapped.append(graph2)
                else:
                    graphs[graph1], graphs[graph2] = CRefignment(graphs[graph1], graphs[graph2])

                    if count_isomorphism(graphs[graph1], graphs[graph2], [], []) > 0:
                        isomorphisms.get(graph1).append(graph2)
                        mapped.append(graph2)

            if len(isomorphisms.get(graph1)) == 0:
                isomorphisms.popitem()
                notisomorphic.append(graph1)

    # Aut problem: only need to calculate for the keys, and graphs not in the dictionary
    for graph in isomorphisms.keys() or notisomorphic:
        sys.stdout.write('\n')
        if FAST:
            graphs[graph], graphs[graph] = fast_refinement(graphs[graph], graphs[graph])
            automorphisms = count_isomorphism_fast(graphs[graph], graphs[graph], [], [])
        else:
            graphs[graph], graphs[graph] = CRefignment(graphs[graph], graphs[graph])
            automorphisms = count_isomorphism(graphs[graph], graphs[graph], [], [])
        if graph in isomorphisms.keys():
            isomorphisms.get(graph).insert(0, graph)
            sys.stdout.write('[' + ', '.join(str(x) for x in isomorphisms.get(graph)) + ']: ' + str(automorphisms))
        else:
            sys.stdout.write(str(graph) + ": " + str(automorphisms))




