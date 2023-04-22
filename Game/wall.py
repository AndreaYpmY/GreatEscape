class Wall:
    # Wall(3,4,1)
    def __init__(self, row, col, orientation):
        self.cell1 = (row,col)
        self.orientation = orientation        # 0 - Horizontal, 1 - Vertical
        self.cell2 = self.__generate_cell2__()

    def __generate_cell2__(self):
        if(self.orientation == 0):       # Horizontal
            return (self.cell1[0]-1,self.cell1[1])
        
        # Vertical
        return (self.cell1[0],self.cell1[1]-1)
    
        