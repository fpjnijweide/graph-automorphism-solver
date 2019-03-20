from week5 import *
from week4 import *
from week3 import *

FILENAME = "graphs/trees36.grl"
FAST = True


if __name__ == '__main__':
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
                if FAST:
                    graphs[graph1], graphs[graph2] = fast_refinement(graphs[graph1], graphs[graph2])

                    if count_isomorphism(graphs[graph1], graphs[graph2], [], []) > 0:
                        isomorphisms.get(graph1).append(graph2)
                        mapped.append(graph2)
                else:
                    graphs[graph1], graphs[graph2] = CRefignment(graphs[graph1], graphs[graph2])

                    if count_isomorphism_fast(graphs[graph1], graphs[graph2], [], []) > 0:
                        isomorphisms.get(graph1).append(graph2)
                        mapped.append(graph2)

            if len(isomorphisms.get(graph1)) == 0:
                isomorphisms.popitem()
                notisomorphic.append(graph1)

    # Print isomorphisms
    for key in isomorphisms.keys():
        isomorphisms.get(key).insert(0, key)
        sys.stdout.write('\n')
        sys.stdout.write('[' + ', '.join(str(x) for x in isomorphisms.get(key)) + ']')


    # Aut problem: only need to calculate for the keys, and graphs not in the dictionary
    sys.stdout.write('\n')
    sys.stdout.write("#Aut problem:")
    for graph in isomorphisms.keys() and notisomorphic:
        graphs[graph] = initialize_colors(graphs[graph])

        sys.stdout.write('\n')
        if FAST:
            graphs[graph], graphs[graph] = fast_refinement(graphs[graph], graphs[graph])
            sys.stdout.write(str(graph) + ": " + str(count_isomorphism_fast(graphs[graph], graphs[graph], [], [])))
        else:
            graphs[graph], graphs[graph] = CRefignment(graphs[graph], graphs[graph])
            sys.stdout.write(str(graph) + ": " + str(count_isomorphism(graphs[graph], graphs[graph], [], [])))




