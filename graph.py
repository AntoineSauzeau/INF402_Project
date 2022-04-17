
class Vertex:

    def __init__(self, name):
        self.name = name
        self.l_neighbors = []

    def get_l_neighbors(self):
        return self.l_neighbors

    def add_neighbor(self, neighbor):
        self.l_neighbors.append(neighbor)

class Graph:

    def __init__(self):
        self.l_vertex = []

    def add_vertex(self, vertex):
        self.l_vertex.append(vertex)

    def get_vertex_from_name(self, name):

        for vertex in self.l_vertex:

            if(vertex.name == name):
                return vertex

    def is_connected(self):

        l_vertex_visited = []
        
        s = self.l_vertex[0]
        l_vertex_visited.append(s)

        self.rec_depth_path(s, l_vertex_visited)

        return len(l_vertex_visited) == len(self.l_vertex)


    def rec_depth_path(self, u, l_vertex_visited):
        
        for t in u.get_l_neighbors():
            if t not in l_vertex_visited:
                l_vertex_visited.append(t)
                self.rec_depth_path(t, l_vertex_visited)