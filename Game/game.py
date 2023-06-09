from ai.ai_manager import AIManager
from ai.monettitocci.ai_manager_monettitocci import AIManagerMonettiTocci
from ai.rasovillella.ai_manager_rasovillella import AIManagerRasoVillella
from ai.ai_player import AIPlayer
from player import Player
from timekeeper import Timekeeper
from wall import Wall

from random import choice, randint, shuffle
import heapq

import time

TURN_LIMIT = 100
PLAYERS_NUM = 2              # Only two players (for now)
BOARD_DIM = 9

class Game:
    def __init__(self, pawns):
        self.turn = 0
        self.winner = None
        self.players = []
        self.ai_managers_pool = []          # Pool of AI managers, every entry is a tuple (AIManager, PlayerName)
        
        # YOU MUST ADD YOUR AI MANAGER HERE (as written below)
        self.ai_managers_pool.append((AIManagerMonettiTocci("./ai/monettitocci/asp/monettitocci.asp"), "monettitocci"))
        self.ai_managers_pool.append((AIManagerRasoVillella("./ai/rasovillella/asp/ASP-RasoVillella.asp"), "rasovillella"))

        self.create_players(pawns)
        
        self.timekeeper = Timekeeper()
        
        # self.switch_player()  # Commented because it's called in main (game loop) after the countdown
        
        self.matrix = [[0 for i in range(9)] for j in range(9)]     # Board matrix

    def create_players(self,assets):
        goals = ['N', 'S', 'W', 'E']
        shuffle(self.ai_managers_pool)          # Shuffle the AI managers pool to assign them randomly to the players
        for i in range(PLAYERS_NUM):                 
            goal = choice(goals)
            goals.remove(goal)
            name = self.ai_managers_pool[i][1]
            ai_manager = self.ai_managers_pool[i][0]
        
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

            self.players.append(AIPlayer(i+1, name, start_r, start_c, goal, assets[i][0], assets[i][1], assets[i][2], ai_manager))

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
            print("Wall out of board") 
            return False
        for player in self.players:
            if player == self.current_player:
                # All the walls of the player except the last one (the one that is being placed)
                walls = player.walls[:-1]
            else:
                walls = player.walls

            for wall in walls:
                if (new_wall[1].cell1 == wall[1].cell1) or (new_wall[1].cell1 == wall[0].cell1 and new_wall[1].orientation == wall[0].orientation) or (new_wall[0].cell1 == wall[1].cell1 and new_wall[1].orientation == wall[0].orientation) or (new_wall[0].cell1 == wall[0].cell1 and new_wall[0].orientation == wall[1].orientation):
                    print(f"Your wall is not valid because it overlaps with another wall")
                    return False
            if not self.can_reach_goal(player, new_wall):
                print(f"Your wall is not valid because it blocks the only path left to the goal")	
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
        if self.turn > 0:
            self.__check_last_move_validity()
            if self.winner is not None:
                return

        self.current_player = self.players[self.turn%PLAYERS_NUM]
        self.turn += 1
        self.timekeeper.start()
        
        # Save the current player position and walls. They will be used to check whether the move is illegal
        self.old_player_pos = (self.current_player.r, self.current_player.c)
        self.old_player_walls = self.current_player.walls.copy()
        self.current_player.ai_manager.ask_for_a_move(self.current_player.id, self.players)
        print(f"Turn {self.turn}: {self.current_player.name} plays")
            

         
    def check_goal(self):            
        for player in self.players: 
            if ((player.goal == 'N' and player.r == 0) or (player.goal == 'S' and player.r == 8) or (player.goal == 'W' and player.c == 0) or (player.goal == "E" and player.c == 8)) and (not player.done):
                player.done = True
                print(f"{player.id} reached the goal")

    def __disqualify_player(self, player):
        print(f"{player.id} has been disqualified")
        if PLAYERS_NUM == 2:
            if player.id == 1:
                self.winner = 2
            else:
                self.winner = 1
        else:
            # To be implemented in the future, if we want to play with more than two players
            pass
        

    def __check_last_move_validity(self):
        current_player_pos = (self.current_player.r, self.current_player.c)
        print(f"Current player pos: {current_player_pos}")
        print(f"Old player pos: {self.old_player_pos}")
        # If the current player position is the same as the old one, the player probably placed a wall
        if current_player_pos == self.old_player_pos:
            if self.current_player.walls == self.old_player_walls:
                # The player didn't move and didn't place a wall, so he loses
                self.__disqualify_player(self.current_player)
            # Else the player placed a wall
            else:
                # Check if the wall is valid
                if self.valid_wall(self.current_player.walls[-1]):
                    self.current_player.dec_remaining_walls()
                else:
                    # The wall is not valid, so the player loses
                    self.__disqualify_player(self.current_player)
        # Else the player moved
        else:
            if self.valid_movement(self.old_player_pos, current_player_pos):
                if self.__is_goal(self.current_player, self.current_player.r, self.current_player.c):
                    print(f"{self.current_player.id} ha vinto")
                    self.winner = self.current_player.id
            else:
                self.__disqualify_player(self.current_player)

    def __is_goal(self,player,r,c):
        if (player.goal == 'N' and r == 0) or (player.goal == 'S' and r == 8) or (player.goal == 'W' and c == 0) or (player.goal == "E" and c == 8):
            return True
        return False
