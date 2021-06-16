# module for reading/writing graphs, original authors P. Bonsma and P. Bos

import sys
from typing import IO, Tuple, List, Union

from graph import Graph, Edge

DEFAULT_COLOR_SCHEME = "paired12"
NUM_COLORS = 12


def read_line(f: IO[str]) -> str:
    line = f.readline()

    while len(line) > 0 and line[0] == '#':
        line = f.readline()

    return line


def read_graph(graphclass, f: IO[str]) -> Tuple[Graph, List[str], bool]:
    options = []

    while True:
        try:
            line = read_line(f)
            n = int(line)
            graph = graphclass(directed=False, n=n)
            break
        except ValueError:
            if len(line) > 0 and line[-1] == '\n':
                options.append(line[:-1])
            else:
                options.append(line)

    line = read_line(f)
    edges = []

    try:
        while True:
            comma = line.find(',')
            if ':' in line:
                colon = line.find(':')
                edges.append((int(line[:comma]), int(line[comma + 1:colon]), int(line[colon + 1:])))
            else:
                edges.append((int(line[:comma]), int(line[comma + 1:]), None))
            line = read_line(f)
    except Exception:
        pass

    indexed_nodes = list(graph.vertices)

    for edge in edges:
        graph += Edge(indexed_nodes[edge[0]], indexed_nodes[edge[1]], edge[2])

    if line != '' and line[0] == '-':
        return graph, options, True
    else:
        return graph, options, False


def read_graph_list(graph_class, f: IO[str]) -> Tuple[List[Graph], List[str]]:
    options = []
    graphs = []
    cont = True

    while cont:
        graph, new_options, cont = read_graph(graph_class, f)
        options += new_options
        graphs.append(graph)

    return graphs, options


def load_graph(f: IO[str], graph_class=Graph, read_list: bool = False) -> Union[Tuple[List[Graph], List[str]], Graph]:
    if read_list:
        graph_list, options = read_graph_list(graph_class, f)
        return graph_list, options
    else:
        graph, options, tmp = read_graph(graph_class, f)
        return graph  # ,options


def input_graph(graph_class=Graph, read_list: bool = False) -> Union[Tuple[List[Graph], List[str]], Graph]:
    return load_graph(f=sys.stdin, graph_class=graph_class, read_list=read_list)


def write_line(f: IO[str], line: str):
    f.write(line + '\n')


def write_graph_list(graph_list: List[Graph], f: IO[str], options=[]):
    for S in options:
        try:
            int(S)
        except ValueError:
            write_line(f, str(S))

    for i, g in enumerate(graph_list):
        n = len(g)
        write_line(f, '# Number of vertices:')
        write_line(f, str(n))

        # Give the vertices (temporary) labels from 0 to n-1:
        label = {}
        for vertex_index, vertex in enumerate(g):
            label[vertex] = vertex_index

        write_line(f, '# Edge list:')

        for e in g.edges:
            if e.weight:
                write_line(f, str(label[e.tail]) + ',' + str(label[e.head]) + ':' + str(e.weight))
            else:
                write_line(f, str(label[e.tail]) + ',' + str(label[e.head]))

        if i + 1 < len(graph_list):
            write_line(f, '--- Next graph:')


def save_graph(graph_list: Union[Graph, List[Graph]], f: IO[str], options=[]):
    if type(graph_list) is list:
        write_graph_list(graph_list, f, options)
    else:
        write_graph_list([graph_list], f, options)


def print_graph(graph_list: Union[Graph, List[Graph]], options=[]):
    if type(graph_list) is list:
        write_graph_list(graph_list, sys.stdout, options)
    else:
        write_graph_list([graph_list], sys.stdout, options)


def write_dot(graph: Graph, f: IO[str], directed=False):
    if directed:
        f.write('digraph G {\n')
    else:
        f.write('graph G {\n')

    name = {}
    next_name = 0
    for v in graph:
        name[v] = next_name
        next_name += 1
        options = 'penwidth=3,'
        if hasattr(v, 'label'):
            options += 'label="' + str(v.label) + '",'
        if hasattr(v, 'colortext'):
            options += 'color="' + v.colortext + '",'
        elif hasattr(v, 'colornum'):
            options += 'color=' + str(v.colornum % NUM_COLORS + 1) + ', colorscheme=' + DEFAULT_COLOR_SCHEME + ','
            if v.colornum >= NUM_COLORS:
                options += 'style=filled,fillcolor=' + str((v.colornum // NUM_COLORS) % NUM_COLORS + 1) + ','
        if len(options) > 0:
            f.write('    ' + str(name[v]) + ' [' + options[:-1] + ']\n')
        else:
            f.write('    ' + str(name[v]) + '\n')
    f.write('\n')

    for e in graph.edges:
        options = 'penwidth=2,'
        if hasattr(e, 'weight'):
            options += 'label="' + str(e.weight) + '",'
        if hasattr(e, 'colortext'):
            options += 'color="' + e.colortext + '",'
        elif hasattr(e, 'colornum'):
            options += 'color=' + str(e.colornum % NUM_COLORS + 1) + ', colorscheme=' + DEFAULT_COLOR_SCHEME + ','
        if len(options) > 0:
            options = ' [' + options[:-1] + ']'
        if directed:
            f.write('    ' + str(name[e.tail]) + ' -> ' + str(name[e.head]) + options + '\n')
        else:
            f.write('    ' + str(name[e.tail]) + '--' + str(name[e.head]) + options + '\n')

    f.write('}')


if __name__ == "__main__":
    from mygraphs import MyGraph

    with open('examplegraph.gr') as f:
        G = load_graph(f, MyGraph)
    print(G)
    G.del_vert(next(iter(G.vertices)))
    print(G)
