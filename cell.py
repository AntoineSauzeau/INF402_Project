
class Cell:
    
    area=-1
    type=0  #Blanche ou noire

    def __init__(self):
        pass

    def set_area(self, area):
        self.area = area
    
    def set_type(self, type):
        self.type = type

    def get_area(self):
        return self.area

    def get_type(self):
        return self.type
    