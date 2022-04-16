from cell import Cell
from graph import Graph, Vertex
import interface

CELL_SIZE=32        #Pixel
MAX_GRID_SIZE=30

class Grid:

    n_case_x = 15
    n_case_y = 15
    pos_x = 0
    pos_y = 0
    grid = []

    def __init__(self, x, y):

        self.create_empty_grid()

        self.pos_x = x
        self.pos_y = y

    def create_empty_grid(self):

        self.grid = []

        for l in range(MAX_GRID_SIZE):

            line_grid = [] 
            for c in range(MAX_GRID_SIZE):
                line_grid.append(Cell(c, l))
            
            self.grid.append(line_grid)

    def is_in_grid(self, x, y):
        return x > self.pos_x and x < (self.pos_x + self.get_grid_width()) and y > self.pos_y and y < (self.pos_y + self.get_grid_height())

    def get_cell_neighbours(self, cell):
        l_neighbour = []

        x = cell.get_x()
        y = cell.get_y()

        if x > 0:
            l_neighbour.append(self.grid[y][x-1])
        if x+1 != self.n_case_x:
            l_neighbour.append(self.grid[y][x+1])
        if y > 0:
            l_neighbour.append(self.grid[y-1][x])
        if y+1 != self.n_case_y:
            l_neighbour.append(self.grid[y+1][x])

        return l_neighbour

    def get_cell_pos_from_pixel_coords(self, x, y):

        x_index = (x - interface.GRID_POS_X) // CELL_SIZE
        y_index = (y - interface.GRID_POS_Y) // CELL_SIZE

        return self.grid[y_index][x_index]

    def is_cell_seq_linked(self, seq_cell):

        graph = Graph()

        for cell in seq_cell:
            vertex = Vertex(str(cell.get_y() * self.n_case_y + cell.get_x()))
            graph.add_vertex(vertex)

        for cell in seq_cell:

            cell_vertex_name = str(cell.get_y() * self.n_case_y + cell.get_x())
            cell_vertex = graph.get_vertex_from_name(cell_vertex_name)

            print("cell : ", cell_vertex_name)

            l_neighbor = self.get_cell_neighbours(cell)
            for neighbor_cell in l_neighbor:
                if neighbor_cell in seq_cell:
                    print(neighbor_cell)
                    neighbor_vertex_name = str(neighbor_cell.get_y() * self.n_case_y + neighbor_cell.get_x())
                    print(neighbor_vertex_name)
                    neighbor_cell_vertex = graph.get_vertex_from_name(neighbor_vertex_name)

                    cell_vertex.add_neighbor(neighbor_cell_vertex)

        print(seq_cell)

        return graph.is_connected()
                    








    def get_n_case_x(self):
        return self.n_case_x

    def get_n_case_y(self):
        return self.n_case_y

    def get_grid_width(self):
        return CELL_SIZE * self.n_case_x
    
    def get_grid_height(self):
        return CELL_SIZE * self.n_case_y

    def set_n_case_x(self, n):
        self.n_case_x = n

    def set_n_case_y(self, n):
        self.n_case_y = n

    #Surdéfinions de l'opérateur []
    def __getitem__(self, index):
        return self.grid[index]

    def __setitem__(self, index, value):
        self.grid[index] = value