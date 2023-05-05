from languages.predicate import Predicate

class Wall(Predicate):
    predicate_name = "wall"
    
    def __init__(self, row, col, orientation):
        Predicate.__init__(self, [("r1"), ("c1"), ("r2"), ("c2")])
        self.cell1 = (row,col)
        self.r1, self.c1 = row, col
        self.orientation = orientation        # 0 - Horizontal, 1 - Vertical
        self.cell2 = self.__generate_cell2__()
        self.r2, self.c2 = self.cell2[0], self.cell2[1]

    #def __init__(self, cell1, cell2):
    #    Predicate.__init__(self, [(cell1[0]), (cell1[1]), (cell2[0]), (cell2[1])])
    #    self.cell1 = cell1
    #    self.cell2 = cell2
    #    self.orientation = self.__generate_orientation__()

    def __generate_orientation__(self):
        if(self.cell1[0] == self.cell2[0]):     # Vertical
            return 1
        
        # Horizontal
        return 0

    def __generate_cell2__(self):
        if(self.orientation == 0):       # Horizontal
            return (self.cell1[0]-1,self.cell1[1])
        
        # Vertical
        return (self.cell1[0],self.cell1[1]-1)
    
    # Getters
    def get_r1(self):
        return self.r1

    def get_c1(self):
        return self.c1

    def get_r2(self):
        return self.r2

    def get_c2(self):
        return self.c2

    # Setters
    def set_r1(self, r1):
        self.r1 = r1

    def set_c1(self, c1):
        self.c1 = c1

    def set_r2(self, r2):
        self.r2 = r2

    def set_c2(self, c2):
        self.c2 = c2
    
    def __str__(self):
        return f"Wall: ({self.cell1} {self.cell2})"