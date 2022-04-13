from cell import Cell

CELL_SIZE=32        #Pixel

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

        for l in range(self.n_case_y):

            line_grid = [] 
            for c in range(self.n_case_x):
                line_grid.append(Cell())
            
            self.grid.append(line_grid)

    def get_n_case_x(self):
        return self.n_case_x

    def get_n_case_y(self):
        return self.n_case_y

    def get_grid_width(self):
        return CELL_SIZE * self.n_case_x
    
    def get_grid_height(self):
        return CELL_SIZE * self.n_case_y

    #Surdéfinions de l'opérateur []
    def __getitem__(self, index):
        return self.grid[index]

    def __setitem__(self, index, value):
        self.grid[index] = value