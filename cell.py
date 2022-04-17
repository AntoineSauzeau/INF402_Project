
class Cell:

    def __init__(self, x, y):
        self.x_index = x
        self.y_index = y
        self.type=0  #Blanche ou noire
        self.is_selected=False
        self.area = -1

    def reset(self):
        self.type=0  
        self.is_selected=False
        self.area = -1

    def set_area(self, area):
        self.area = area
    
    def set_type(self, type):
        self.type = type

    def set_is_selected(self, is_selected):
        self.is_selected = is_selected

    def get_area(self):
        return self.area

    def get_type(self):
        return self.type

    def get_is_selected(self):
        return self.is_selected

    def get_x(self):
        return self.x_index

    def get_y(self):
        return self.y_index
    