from wall import Wall
from player import Player
from languages.predicate import Predicate

class AIPlayer(Player):
    def __init__(self, id, name, r, c, goal, pawn, hud, color, ai_manager):
        super().__init__(id, name, r, c, goal, pawn, hud, color)
        self.ai_manager = ai_manager
