from wall import Wall

class Player:
    def __init__(self, id, r, c, goal, image, color):
        self.id = id 
        self.r = r
        self.c = c
        self.remaining_walls = 10
        self.walls = []
        self.image = image
        self.color = color
        self.goal = goal
        self.done = False

    def place_wall(self, walls):
        self.walls.append(walls)

    def generate_wall(r,c,o):
        wall1 = Wall(r,c,o)
        if(o == 0):
            wall2 = Wall(r,c+1,o)
        else:
            wall2 = Wall(r+1,c,o)
        
        return((wall1,wall2))

    def new_position(self,r,c):
        self.r = r
        self.c = c

    def dec_remaining_walls(self):
        self.remaining_walls-=1

        