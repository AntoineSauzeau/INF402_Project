

class Literal:

    def __init__(self, value, neg):
        self.value = value 
        self.neg = neg
    def get_value(self):
        return self.value
    def get_neg(self):
        return self.neg
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
    
    def __len__(self):
        return len(self.l_literal)

class Cnf:

    def __init__(self):
        self.l_clause = []

    def __iadd__(self, clause):
        self.l_clause.append(clause)
        return self
    def __len__(self):
        return len(self.l_clause)
    def get_l_clause(self):
        return self.l_clause
    def get_l_literal(self):
        l_variable = []
        for clause in self.l_clause:
            l_literal = clause.get_l_literal()
            for literal in l_literal:
                if str(literal) not in l_variable:
                    l_variable.append(str(literal))

        return l_variable

    def count_variable_number(self):

        l_variable = []
        for clause in self.l_clause:
            l_literal = clause.get_l_literal()
            for literal in l_literal:
                if str(literal) not in l_variable:
                    l_variable.append(str(literal))

        return len(l_variable)


    def write_to_dimacs_file(self, file_name,x,y,solver):
        try:
            file = open(file_name, "w")
        except IOError:
            print("impossible d'ouvrir le fichier :", file_name)

        file.write("p cnf " + str(self.count_variable_number()) + " " + str(len(self.l_clause)) + "\n")

        for clause in self.l_clause:
            file.write(str(clause) + "0\n")
            l = clause.get_l_literal()
            l2 = []
            for lit in l:
                l2.append(int(str(lit)))
            solver.add_clause(l2)




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

    #∀(i1, j1)...(in, jm) ∈ Rk, (xi1,j1 ∨ ... ∨ xin,jm ) ∧ (yi1,j1 ∨ ... ∨ yin,jm ) ---> au moins une bille et balle par région
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

                if cell_1.get_y() * grid.get_n_case_x() + cell_1.get_x() >= cell_2.get_y() * grid.get_n_case_x() + cell_2.get_x() :
                    continue
                
                clause_1 = Clause()
                clause_2 = Clause()

                lit_1 = Literal(get_literal_index("x", cell_1.get_x(), cell_1.get_y(), grid.get_n_case_x()), True)
                lit_2 = Literal(get_literal_index("x", cell_2.get_x(), cell_2.get_y(), grid.get_n_case_x()), True)

                lit_3 = Literal(get_literal_index("y", cell_1.get_x(), cell_1.get_y(), grid.get_n_case_x()), True)
                lit_4 = Literal(get_literal_index("y", cell_2.get_x(), cell_2.get_y(), grid.get_n_case_x()), True)

                clause_1 += lit_1
                clause_1 += lit_2
                clause_2 += lit_3
                clause_2 += lit_4

                cnf += clause_1
                cnf += clause_2

    #regle sur le placement des ballons
    for c in range(grid.get_n_case_x()):
        for l in range(grid.get_n_case_y()):

            cell = grid[l][c]

            if cell.get_type() == 0 and l != 0:

                for i in range(1, l+1):

                    cell_2 = grid[l-i][c]

                    if cell_2.get_type() == 1:
                        break 

                    clause = Clause()

                    lit_1 = Literal(get_literal_index("x", c, l, grid.get_n_case_x()), True)
                    lit_2 = Literal(get_literal_index("x", c, l-i, grid.get_n_case_x()), False)
            
                    clause += lit_1
                    clause += lit_2
            
                    cnf += clause

    #regle sur le placement des billes
    for c in range(grid.get_n_case_x()):
        for l in range(grid.get_n_case_y()):

            cell = grid[l][c]

            if cell.get_type() == 0 and l != grid.get_n_case_y()-1:
    
                for i in range(1, grid.get_n_case_y()-l):

                    cell_2 = grid[l+i][c]

                    if cell_2.get_type() == 1:
                        break

                    clause = Clause()

                    lit_1 = Literal(get_literal_index("y", c, l, grid.get_n_case_x()), True)
                    lit_2 = Literal(get_literal_index("y", c, l+i, grid.get_n_case_x()), False)
            
                    clause += lit_1
                    clause += lit_2
            
                    cnf += clause

    return cnf

def read_cnf_from_dimacs_file(file_name): 
    try:
        file = open(file_name, "w")
    except IOError:
        print("impossible d'ouvrir le fichier :", file_name)
        
    cnf = Cnf()
    for line in file.readlines():
        clause_line = line.split() #sépare la ligne en une liste de chaque mot séparé par des  espaces
        clause = Clause()
        if len(clause_line) != 0 and clause_line[0] != "p" and clause_line[0] != "c": #c pour les commentaires
            for literal in clause_line:
                literal_value = int(literal)
                if literal_value == 0: #fin de ligne
                    cnf+=clause
                else:
                    # not at the end, then append variable inside the last list!
                    clause+=literal
                    
        elif len(clause_line) != 0 and clause_line[0] == "p":
             nb_variables = int(clause[2])
             nb_clauses = int(clause[3])
    return cnf, num_variables, num_clauses

def convert_cnf_to_3sat(cnf,grid):
    cnf2 = Cnf()
    liste_clauses2 = cnf2.get_l_clause()
    nb_variables = grid.get_n_case_x()*grid.get_n_case_y()*2
    y = nb_variables
    liste_clauses = cnf.get_l_clause()
    for clause in liste_clauses :
        # un littéral x dans la clause : 
        # nouvelles clauses = {x+y1+y2; x+ !y1 +y2; x+y1+ !y2 ;x+ !y1 + !y2} 
        # où y1 et y2 sont des nouvelles variables.
        if len(clause)== 1:
            c1 = Clause()
            c2 = Clause()
            c3 = Clause()
            c4 = Clause()
            l = str(clause.get_l_literal()[0])
            lit1 = str(Literal(y+1,False)) 
            lit1n = str(Literal(y+1,True))
            lit2 = str(Literal(y+2,False))
            lit2n = str(Literal(y+2,True))
            c1+= l
            c1+= lit1
            c1+= lit2
            c2+= l
            c2+=lit1
            c2+= lit2n
            c3+= l
            c3+= lit1n
            c3+= lit2n
            c4+= l
            c4+= lit1n
            c4+=lit2
            cnf2 += c1
            cnf2 += c2
            cnf2 += c3
            cnf2 += c4     
            y+=2
        # deux littéraux x et y dans la clause : 
        # nouvelles clauses = {x+y+z; x+y+!z} 
        # où z est une nouvelle variable.
        elif len(clause)==2:
            c1 = Clause()
            c2 = Clause()
            l1 = str(clause.get_l_literal()[0])
            l2 = str(clause.get_l_literal()[1])
            lit1 = str(Literal(y+1,False))
            lit1n = str(Literal(y+1,True))
            c1+= l1
            c1+= lit1
            c1+= l2
            c2+= l1
            c2+= lit1n
            c2+= l2
            cnf2 += c1
            cnf2 += c2
            y+=1
        # plus de 3 littéraux dans la clause (k littéraux) : 
        # nouvelles clauses = {x1+x2+y1; !y1+x3+y2; !y2+x4+y3; !y3+x5+y4; ...; !y(k−3)+x(k−1)+x(k)} 
        # où y sont les nouvelles variables.
        elif len(clause)>3:
            c1 = Clause()
            l1 = str(clause.get_l_literal()[0])
            l2 = str(clause.get_l_literal()[1])
            lit1 = str(Literal(y+1,False))
            c1+=l1
            c1+=l2
            c1+=lit1
            cnf2+=c1
            y+=1
            for i in range(1,len(clause)-3):
                c = Clause()
                lit1 = str(Literal(y,True))
                lit2 = str(Literal(y+1,False))
                l2 = str(clause.get_l_literal()[i+1])
                c += l2
                c += lit1
                c += lit2 
                cnf2+=c
                y+=1
            c2 = Clause()
            l1 = str(clause.get_l_literal()[len(clause)-2])
            l2 = str(clause.get_l_literal()[len(clause)-1])
            lit1 = str(Literal(y+1,True))
            c2+=l1
            c2+=l2
            c2+=lit1
            cnf2+=c2
            y+=1
        else :
            cnf2 += clause
            
            
    return cnf2
    
def dpll(cnf, assignments):
    if len(cnf) == 0:
        return True, assignments
    clauses = cnf.get_l_clause()
    for clause in clauses :
        if len(clause)==0:
            return False, None
 
    l,f = select_literal(cnf,assignments)
    n = l.get_neg()
    v = l.get_value()
    if f:
        #print("New cnf with ",v,"=", not n," and clauses : ")
        new_cnf =  Cnf()
        for clause in clauses:
            lit = clause.get_l_literal()
            add = True
            c2 = Clause()
            for literal in lit:
                if literal.get_value()!=v:
                    c2+=literal
                else :
                    if literal.get_neg()==n:
                        add = False
            if add :
                new_cnf+=c2
                #print(str(c2))
        if (v, n) in assignments:
            assignments.pop(assignments.index((v, n)))
        if not (v,not n) in assignments :
            assignments.append((v, not n))
        #print(assignments)
        sat, vals = dpll(new_cnf, assignments)    
        if sat:
            return sat, vals
        
        return False, None
        
    
    new_cnf =  Cnf()
    #print("New cnf with ",v,"=", not n," and clauses : ")
    for clause in clauses:
        lit = clause.get_l_literal()
        add = True
        c2 = Clause()
        for literal in lit:
            if literal.get_value()!=v:
                c2+=literal
            else :
                if literal.get_neg()==n:
                    add = False
        if add :
            #print(str(c2))
            new_cnf+=c2
    if (v, n) in assignments:  
        assignments.pop(assignments.index((v, n)))
    if not (v,not n) in assignments :
        assignments.append((v, not n))
    #print(assignments)
    sat, vals = dpll(new_cnf, assignments)
    if sat:
        return sat, vals
    else :
        #print("On revient sur notre choix de cnf avec ",v," = ", n, " et les clauses :")
        
        new_cnf =  Cnf()
        for clause in clauses:
            lit = clause.get_l_literal()
            add = True
            c2 = Clause()
            for literal in lit:
                if literal.get_value()!=v:
                    c2+=literal
                else :
                    if literal.get_neg()!=n:
                        add = False
            if add :
                new_cnf+=c2
                #print(str(c2))
        if (v, not n) in assignments:  
            assignments.pop(assignments.index((v, not n)))
        if not (v, n) in assignments :
            assignments.append((v, n))
        #print(assignments)
        sat, vals = dpll(new_cnf, assignments)
        if sat:
            return sat, vals
    return False, None

def select_literal(cnf,assignments):
    clauses = cnf.get_l_clause()
    for c in clauses:
        if len(c)==1:
            return c.get_l_literal()[0], True
            
    for c in clauses:
        lit = c.get_l_literal()
        for l in lit:
            v = l.get_value()
            n = l.get_neg()
            if not (v,n) in assignments:
                return l, False
            
        