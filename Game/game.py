from ai_manager import AIManager
from ai_manager_monettitocci import AIManagerMonettiTocci
from player import Player
from timekeeper import Timekeeper
from wall import Wall

from random import choice, randint
import heapq

import time

TURN_LIMIT = 100
PLAYERS_NUM = 2              # Only two players (for now)
BOARD_DIM = 9

class Game:
    def __init__(self, pawns):
        self.turn = 0
        self.players = []
        self.create_players(pawns)
        self.ai_manager = AIManager()
        self.ai_manager_monetti_tocci = AIManagerMonettiTocci()
        self.timekeeper = Timekeeper()
        self.switch_player()
        self.matrix = [[0 for i in range(9)] for j in range(9)]     # Board matrix

        # TODO: MURI DI PROVA (DA RIMUOVERE GRZ)
        self.players[0].walls.append((Wall(3,4,1), Wall(4,4,1)))
        self.players[0].walls.append((Wall(6,3,0), Wall(6,4,0)))
        self.players[1].walls.append((Wall(2,2,0), Wall(2,3,0)))
        print(f"Red player goal: {self.players[0].goal}")
        print(f"Green player goal: {self.players[1].goal}")

        

    def create_players(self,pawns):
        goals = ['N', 'S', 'W', 'E']
        for i in range(PLAYERS_NUM):                 
            goal = choice(goals)
            goals.remove(goal)
        
            if goal == 'N':
                start_r = 8                         # Last row
                start_c = randint(1, 7)             # Angles excluded
            elif goal == 'S':
                start_r = 0                         # First row
                start_c = randint(1, 7)             # Angles excluded
            elif goal == 'W':
                start_c = 8                         # Last col
                start_r = randint(1, 7)             # Angles excluded
            else:
                start_c = 0                         # First col
                start_r = randint(1, 7)             # Angles excluded

            self.players.append(Player(i+1, start_r, start_c, goal, pawns[i][0], pawns[i][1]))

    def valid_movement(self, current_pos, next_pos):
        for player in self.players:
            for wall in player.walls:
                if (wall[0].cell1 == current_pos and wall[0].cell2 == next_pos) or (wall[0].cell2 == current_pos and wall[0].cell1 == next_pos) or (wall[1].cell1 == current_pos and wall[1].cell2 == next_pos) or (wall[1].cell2 == current_pos and wall[1].cell1 == next_pos):
                    return False
                if next_pos[0] < 0 or next_pos[0] > 8 or next_pos[1] < 0 or next_pos[1] > 8:
                    return False
        return True
    
    def __is_out_of_board(self, wall):
        if wall[0].orientation == 0:
            return wall[0].cell2[0] < 0 or wall[0].cell1[0] > 8 or wall[1].cell1[1] > 8 or wall[1].cell1[1] < 0
        else:
            return wall[0].cell2[1] < 0 or wall[0].cell1[1] > 8 or wall[1].cell1[0] > 8 or wall[1].cell1[0] < 0

    def valid_wall(self,new_wall):
        # Return false if the wall goes out of the board
        if self.__is_out_of_board(new_wall):
            print("Muro fuori dalla scacchiera") 
            return False
        for player in self.players:
            for wall in player.walls:
                if (new_wall[1].cell1 == wall[1].cell1) or (new_wall[1].cell1 == wall[0].cell1 and new_wall[1].orientation == wall[0].orientation) or (new_wall[0].cell1 == wall[1].cell1 and new_wall[1].orientation == wall[0].orientation) or (new_wall[0].cell1 == wall[0].cell1 and new_wall[0].orientation == wall[1].orientation):
                    print(f"Il tuo muro non è valido per il posizionamento")
                    return False
            if not self.can_reach_goal(player, new_wall):
                print(f"Il tuo muro non è valido perchè blocca il passaggio")	
                return False
        return True

    def __crosses_new_wall(self, curr, next, wall):
        return (wall[0].cell1 == curr and wall[0].cell2 == next) or (wall[0].cell2 == curr and wall[0].cell1 == next) or (wall[1].cell1 == curr and wall[1].cell2 == next) or (wall[1].cell2 == curr and wall[1].cell1 == next)

    def can_reach_goal(self, player, wall):
        queue = []
        visited = [[False for _ in range(BOARD_DIM)] for _ in range(BOARD_DIM)]
        queue.append((player.r, player.c))
        visited[player.r][player.c] = True
        
        while not len(queue)==0:
            r, c = queue.pop(0)
            if self.__is_goal(player, r, c):
                return True
            if r > 0 and not visited[r-1][c] and self.valid_movement((r, c), (r-1, c)) and not self.__crosses_new_wall((r, c), (r-1, c), wall):
                queue.append((r-1, c))
                visited[r-1][c] = True
            if r < BOARD_DIM-1 and not visited[r+1][c] and self.valid_movement((r, c), (r+1, c)) and not self.__crosses_new_wall((r, c), (r+1, c), wall):
                queue.append((r+1, c))
                visited[r+1][c] = True
            if c > 0 and not visited[r][c-1] and self.valid_movement((r, c), (r, c-1)) and not self.__crosses_new_wall((r, c), (r, c-1), wall):
                queue.append((r, c-1))
                visited[r][c-1] = True
            if c < BOARD_DIM-1 and not visited[r][c+1] and self.valid_movement((r, c), (r, c+1)) and not self.__crosses_new_wall((r, c), (r, c+1), wall):
                queue.append((r, c+1))
                visited[r][c+1] = True
        return False

    def switch_player(self):
        self.current_player = self.players[self.turn%PLAYERS_NUM]
        self.turn += 1
        self.timekeeper.start()
        if(self.turn % 2 == 1):
            # self.ai_manager_monetti_tocci.ask_for_a_move(self.current_player.id, self.players)
            print(f"Turno {self.turn} di MonettiTocci")
        else:
            # self.ai_manager_raso_villella.ask_for_a_move(self.current_player.id, self.players)
            print(f"Turno {self.turn} di RasoVillella")

        
        
    def check_goal(self):            
        for player in self.players: 
            if ((player.goal == 'N' and player.r == 0) or (player.goal == 'S' and player.r == 8) or (player.goal == 'W' and player.c == 0) or (player.goal == "E" and player.c == 8)) and (not player.done):
                player.done = True
                print(f"{player.id} ha finito")

    def __is_goal(self,player,r,c):
        if (player.goal == 'N' and r == 0) or (player.goal == 'S' and r == 8) or (player.goal == 'W' and c == 0) or (player.goal == "E" and c == 8):
            return True
        return False
