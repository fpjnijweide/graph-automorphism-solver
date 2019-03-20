from week5 import *
from week4 import *
from week3 import *

FILENAME = "graphs/trees36.grl"
GI_problem = True
Aut_problem = True
fast_refinement = False


if __name__ == '__main__':
    with open(FILENAME) as file:
        graphs = load_graph(file, read_list=True)[0]

    # GI problem:
    sys.stdout.write("Sets of isomorphic graphs:")
    for graph1 in range(0, len(graphs) - 1):
        for graph2 in range(graph1 + 1, len(graphs)):
            # Initialisation
            graphs[graph1] = initialize_colors(graphs[graph1])
            graphs[graph2] = initialize_colors(graphs[graph2])

            # Refinement, either colour or fast
            if fast_refinement:
                graphs[graph1], graphs[graph2] = fast_refinement(graphs[graph1], graphs[graph2])
            else:
                graphs[graph1], graphs[graph2] = CRefignment(graphs[graph1], graphs[graph2])

            # Print the isomorphic graphs
            if count_isomorphism(graphs[graph1], graphs[graph2], [], []) > 0:
                print()
                out = "[" + str(graph1) + ", " + str(graph2) + "]"
                print(out)
                #sys.stdout.write(out)

