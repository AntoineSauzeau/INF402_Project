from cell import Cell
from graph import Graph, Vertex
import interface
from pickle import Pickler, Unpickler
from pathlib import Path
import os
import tkinter as tk
from tkinter import filedialog


MAX_GRID_SIZE=30
GRID_SIZE = 540 #pixels

class Grid:

    n_case_x = 15
    n_case_y = 15
    pos_x = 0
    pos_y = 0
    grid = []

    l_ball_pos = []
    l_marble_pos = []

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
        return x > self.pos_x and x < (self.pos_x + GRID_SIZE) and y > self.pos_y and y < (self.pos_y + GRID_SIZE)

    def get_top_cell(self, cell):
        x = cell.get_x()
        y = cell.get_y()

        if y > 0:
            return self.grid[y-1][x]

        return None

    def get_bottom_cell(self, cell):
        x = cell.get_x()
        y = cell.get_y()

        if y+1 != self.n_case_y:
            return self.grid[y+1][x]

        return None

    def get_left_cell(self, cell):
            x = cell.get_x()
            y = cell.get_y()

            if x > 0:
                return self.grid[y][x-1]

            return None

    def get_right_cell(self, cell):
            x = cell.get_x()
            y = cell.get_y()

            if x+1 != self.n_case_x:
                return self.grid[y][x+1]

            return None

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

    def get_cell_pos_from_pixel_coords(self, x, y, nb_cases):

        x_index = (x - interface.GRID_POS_X) // int((GRID_SIZE/nb_cases))
        y_index = (y - interface.GRID_POS_Y) // int((GRID_SIZE/nb_cases))

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

    def get_cell_by_area(self):

        l_cell_by_area = {}
        for l in range(self.n_case_y):
            for c in range(self.n_case_x):

                cell = self.grid[l][c]
                area = str(cell.get_area())
                if area == "-1":
                    continue

                if area not in l_cell_by_area.keys():
                    l_cell_by_area[area] = []

                l_cell_by_area[area].append(cell)

        return l_cell_by_area

    def get_black_cells(self):
        l_cell = []

        for l in range(self.n_case_y):
            for c in range(self.n_case_x):

                cell = self.grid[l][c]
                if cell.get_type() == 1:
                    l_cell.append(cell)

        return l_cell

    def reset(self):

        for l in range(MAX_GRID_SIZE):
            for c in range(MAX_GRID_SIZE):
                self.grid[l][c].reset()

    def get_n_case_x(self):
        return self.n_case_x

    def get_n_case_y(self):
        return self.n_case_y

    def get_l_marble_pos(self):
        return self.l_marble_pos

    def get_l_ball_pos(self):
        return self.l_ball_pos

    def set_n_case_x(self, n):
        self.n_case_x = n

    def set_n_case_y(self, n):
        self.n_case_y = n

    #Surdéfinions de l'opérateur []
    def __getitem__(self, index):
        return self.grid[index]

    def __setitem__(self, index, value):
        self.grid[index] = value




def save_grid_to_file(grid_object):

    root = tk.Tk()
    root.withdraw()

    filepath = filedialog.asksaveasfilename(initialdir=str(Path("./Grids/")))

    try:
        file = open(str(Path(filepath)), "wb")
    except Exception as e:
        print(e)
    else:
        Pickler(file).dump(grid_object)
        file.close()

def load_grid_from_file():

    root = tk.Tk()
    root.withdraw()

    filepath = filedialog.askopenfilename(initialdir=str(Path("./Grids/")))

    try:
        file = open(str(Path(filepath)), "rb")
        #Si le fichier est vide, inutile d'essayer de le charger
        if(os.path.getsize(filepath) == 0):
            return
    except Exception as e:
        print(e)
    else:
        grid_object = Unpickler(file).load()

        grid_object.l_ball_pos.clear()
        grid_object.l_marble_pos.clear()

        file.close()
        return grid_object