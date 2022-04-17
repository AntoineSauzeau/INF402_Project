

class Literal:

    def __init__(self, value, neg):
        self.value = value 
        self.neg = neg

    def __str__(self):
        if self.neg == False:
            return str(self.value)
        else:
            return "-" + str(self.value)

class Clause:

    def __init__(self):
        self.l_literal = []

    def __str__(self):
         
        result = ""
        for literal in self.l_literal:
            result += str(literal) + " "

        return result

    def __iadd__(self, literal):
        self.l_literal.append(literal)
        return self

    def get_l_literal(self):
        return self.l_literal

class Cnf:

    def __init__(self):
        self.l_clause = []

    def __iadd__(self, clause):
        self.l_clause.append(clause)
        return self

    def get_l_clause(self):
        return self.l_clause

    def count_variable_number(self):

        l_variable = []
        for clause in self.l_clause:
            l_literal = clause.get_l_literal()
            for literal in l_literal:
                if str(literal) not in l_variable:
                    l_variable.append(str(literal))

        return len(l_variable)


    def write_to_dimacs_file(self, file_name):
        try:
            file = open(file_name, "w")
        except IOError:
            print("impossible d'ouvrir le fichier :", file_name)

        file.write("p cnf " + str(self.count_variable_number()) + " " + str(len(self.l_clause)) + "\n")

        for clause in self.l_clause:
            file.write(str(clause) + "0\n")




def get_literal_index(var, x, y, grid_size):

    if(var == "x"):
        return y * grid_size + x + 1
    elif(var == "y"):
        return grid_size * grid_size + y * grid_size + x + 1

def convert_grid_to_cnf(grid):

    cnf = Cnf()
    l_cell_by_area = grid.get_cell_by_area()
    print(l_cell_by_area)
    
    #∀(i, j), ¬(xi,j ∧ yi,j ) ≡ ¬xi,j ∨ ¬yi,j )
    for c in range(grid.get_n_case_x()):
        for l in range(grid.get_n_case_y()):
            lit_1 = Literal(get_literal_index("x", c, l, grid.get_n_case_x()), True)
            lit_2 = Literal(get_literal_index("y", c, l, grid.get_n_case_x()), True)

            clause = Clause()
            clause += lit_1
            clause += lit_2

            cnf += clause

    #∀(i1, j1)...(in, jm) ∈ Rk, (xi1,j1 ∨ ... ∨ xin,jm ) ∧ (yi1,j1 ∨ ... ∨ yin,jm )
    for area in l_cell_by_area.keys():

        clause_1 = Clause()
        clause_2 = Clause()

        for cell in l_cell_by_area[area]:
            lit_1 = Literal(get_literal_index("x", cell.get_x(), cell.get_y(), grid.get_n_case_x()), False)
            lit_2 = Literal(get_literal_index("y", cell.get_x(), cell.get_y(), grid.get_n_case_x()), False)

            clause_1 += lit_1
            clause_2 += lit_2

        cnf += clause_1
        cnf += clause_2

    #Il y a au plus une bille et un ballon par région
    for area in l_cell_by_area.keys():

        for cell_1 in l_cell_by_area[area]:
            for cell_2 in l_cell_by_area[area]:

                if cell_1 == cell_2:
                    continue
                
                clause_1 = Clause()
                clause_2 = Clause()

                lit_1 = Literal(get_literal_index("x", cell_1.get_x(), cell_1.get_y(), grid.get_n_case_x()), True)
                lit_2 = Literal(get_literal_index("x", cell_2.get_x(), cell_2.get_y(), grid.get_n_case_x()), True)

                lit_3 = Literal(get_literal_index("y", cell_1.get_x(), cell_2.get_y(), grid.get_n_case_x()), True)
                lit_4 = Literal(get_literal_index("y", cell_1.get_x(), cell_2.get_y(), grid.get_n_case_x()), True)

                clause_1 += lit_1
                clause_1 += lit_2
                clause_2 += lit_3
                clause_2 += lit_4

                cnf += clause_1
                cnf += clause_2

    #regle sur le placement des ballons (voir bille sur case noire)
    for c in range(grid.get_n_case_x()):
        for l in range(grid.get_n_case_y()):

            cell = grid[l][c]

            if cell.get_type() == 0 and l != 0:

                for i in range(1, l+1):

                    cell_2 = grid[l-i][c]

                    if cell.get_type() == 1:
                        continue 

                    clause = Clause()

                    lit_1 = Literal(get_literal_index("x", c, l, grid.get_n_case_x()), True)
                    lit_2 = Literal(get_literal_index("x", c, l-i, grid.get_n_case_x()), False)
            
                    clause += lit_1
                    clause += lit_2
            
                    cnf += clause

    #regle sur le placement des billes (voir bille sur case noire)
    for c in range(grid.get_n_case_x()):
        for l in range(grid.get_n_case_y()):

            cell = grid[l][c]

            if cell.get_type() == 0 and l != grid.get_n_case_y():

                for i in range(1, l+1):

                    cell_2 = grid[l+i][c]

                    if cell.get_type() == 1:
                        continue 

                    clause = Clause()

                    lit_1 = Literal(get_literal_index("y", c, l, grid.get_n_case_x()), True)
                    lit_2 = Literal(get_literal_index("y", c, l+i, grid.get_n_case_x()), False)
            
                    clause += lit_1
                    clause += lit_2
            
                    cnf += clause

    return cnf

def read_cnf_from_dimacs_file():
    pass

def convert_cnf_to_3sat():
    pass

