from languages.predicate import Predicate

class Path(Predicate):
    predicate_name = "path"
    def __init__(self,id,r,c,w):
        Predicate.__init__(self, [("id"), ("r"), ("c"), ("w")])
        self.id = id
        self.r = r
        self.c = c
        self.w = w

    # Getter
    def get_id(self):
        return self.id
    
    def get_r(self):
        return self.r

    def get_c(self):
        return self.c
    
    def get_w(self):
        return self.w

    # Setter
    def set_id(self, id):
        self.id = id
    
    def set_id(self, r):
        self.r = r

    def set_id(self, c):
        self.c = c

    def set_id(self, w):
        self.w = w

    def __str__(self):
        return f"Path: ({self.id} {self.r} {self.c} {self.w})"

