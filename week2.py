from graph import *
import random


def create_graph_with_path(n):
    G = Graph(False, n)

    unused_vertices = G.vertices.copy()
    done = False
    unused_vertices.remove(random.choice(unused_vertices))  # remove a random vertex to make a path of n-1
    vertex2 = random.choice(unused_vertices)
    unused_vertices.remove(vertex2)
    while not done:
        vertex1 = vertex2
        vertex2 = random.choice(unused_vertices)
        unused_vertices.remove(vertex2)
        e = Edge(vertex1, vertex2)
        G.add_edge(e)
        if len(unused_vertices) == 0:
            done = True
    return G


def create_graph_with_cycle(n):
    G = Graph(False, n)

    for i in range(len(G.vertices)):
        if i != len(G.vertices) - 1:
            e = Edge(G.vertices[i], G.vertices[i + 1])

        else:
            e = Edge(G.vertices[i], G.vertices[0])

        G.add_edge(e)
    return G


def create_complete_graph(n):
    G = Graph(False, n)

    for i in range(len(G.vertices) - 1):
        for j in range(i+1, len(G.vertices)):
            e = Edge(G.vertices[i], G.vertices[j])
            G.add_edge(e)
    return G

def complement(G: Graph):
    new_G = Graph(G.directed, 0, G.simple)
    d = {}
    for v in G.vertices:
        new_v = Vertex(new_G, v.label)
        new_G.add_vertex(new_v)
        d[v] = new_v
    for i in range(len(G.vertices) - 1):
        for j in range(i + 1, len(G.vertices)):
            if len(G.find_edge(G.vertices[i], G.vertices[j])) == 0:
                new_G.add_edge(Edge(d[G.vertices[i]], d[G.vertices[j]]))
    return new_G

def BFS(G: Graph):
    current_vertex = G.vertices[0]
    done = False
    seen_vertices = {current_vertex: 0}

    next_neighbors_to_visit = []
    visiting_order=0
    current_vertex.label=visiting_order
    while not done:
        visiting_order+=1
        current_vertex.label = visiting_order
        # look at neighbours of current vertex and put their lengths in dict
        for neighbour in current_vertex.neighbours:
            if neighbour not in seen_vertices:
                neighbour_distance=seen_vertices[current_vertex] + 1
                seen_vertices[neighbour] = neighbour_distance

                neighbour.colornum = neighbour_distance
                next_neighbors_to_visit.append(neighbour)
        # find new vertex to do this from
        if len(next_neighbors_to_visit)>0:
            current_vertex=next_neighbors_to_visit[0]
            next_neighbors_to_visit.remove(current_vertex)
        else:
            done=True

    connected=True
    # checking if connected
    for vertex in G.vertices:
        if vertex not in seen_vertices:
            connected=False
            break

    return connected, seen_vertices

def DFS(G: Graph):
    current_vertex = G.vertices[0]
    done = False
    seen_vertices = {current_vertex: 0}

    next_neighbors_to_visit = []
    visiting_order=0
    current_vertex.label=visiting_order
    while not done:
        visiting_order+=1
        current_vertex.label = visiting_order
        # look at neighbours of current vertex and put their lengths in dict
        for neighbour in current_vertex.neighbours:
            if neighbour not in seen_vertices:
                neighbour_distance=seen_vertices[current_vertex] + 1
                seen_vertices[neighbour] = neighbour_distance

                neighbour.colornum = neighbour_distance
                next_neighbors_to_visit.insert(0,neighbour)
        # find new vertex to do this from
        if len(next_neighbors_to_visit)>0:
            current_vertex=next_neighbors_to_visit[0]
            next_neighbors_to_visit.remove(current_vertex)
        else:
            done=True

    connected=True
    # checking if connected
    for vertex in G.vertices:
        if vertex not in seen_vertices:
            connected=False
            break

    return connected, seen_vertices

if __name__ == '__main__':
    G = create_complete_graph(5)
    H= create_graph_with_cycle(7)
    J= create_graph_with_path(9)
    print(G)
    print(H)
    print(J)

    new=G+H
    print(new)
