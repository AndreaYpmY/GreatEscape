from wall import Wall
from languages.predicate import Predicate

class Player(Predicate):
    predicate_name = "player"

    def __init__(self, id, r, c, goal, image, color):
        Predicate.__init__(self, [("id"), ("r"), ("c"), ("remaining_walls"), ("goal")])
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

    def generate_wall(self,r,c,o):
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


    # Getters
    def get_id(self):
        return self.id
    
    def get_r(self):
        return self.r

    def get_c(self):
        return self.c

    def get_remaining_walls(self):
        return self.remaining_walls
    
    def get_goal(self):
        return self.goal

    # Setters
    def set_id(self, id):
        self.id = id

    def set_r(self, r):
        self.r = r
    
    def set_c(self, c):
        self.c = c
    
    def set_remaining_walls(self, remaining_walls):
        self.remaining_walls = remaining_walls

    def set_goal(self, goal):
        self.goal = goal

    def __str__(self):
        return f"Player: ({self.id} {self.r} {self.c} {self.remaining_walls} {self.goal})"

        