from player import Player
from wall import Wall
from random import choice, randint

TURN_LIMIT = 100
PLAYERS_NUM = 2              # Only two players (for now)

class Game:
    def __init__(self, pawns):
        self.turn = 0
        self.players = []
        self.create_players(pawns)
        self.switch_player()
        
        self.matrix = [[0 for i in range(9)] for j in range(9)]

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
    
    def valid_wall(self,new_wall):
        for player in self.players:
            for wall in player.walls:
                if (new_wall[1].cell1 == wall[1].cell1) or (new_wall[1].cell1 == wall[0].cell1 and new_wall[1].orientation == wall[0].orientation) or (new_wall[0].cell1 == wall[1].cell1 and new_wall[1].orientation == wall[0].orientation) or (new_wall[0].cell1 == wall[0].cell1 and new_wall[0].orientation == wall[1].orientation):
                    print(f"Il tuo muro non è valido per il posizionamento")
                    return False
            if not self.can_reach_goal(player.r, player.c, new_wall):
                print(f"Il tuo muro non è valido perchè blocca il passaggio")	
                return False
        return True

    def can_reach_goal(self, r, c, wall):
        # crea una lista di tutti i muri sul tavolo di gioco
        board_walls = []
        for player in self.players:
            for wall in player.walls:
                board_walls.append(wall[0])
                board_walls.append(wall[1])

        # aggiunge i muri dati in input alla lista
        board_walls.append(wall[0])
        board_walls.append(wall[1])

        # verifica se esiste un percorso tra il giocatore e la sua meta che non attraversa alcun muro
        visited = [[False for i in range(9)] for j in range(9)]
        q = [(r, c)]
        while q:
            curr_r, curr_c = q.pop(0)
            print(f"curr_r: {curr_r}, curr_c: {curr_c}")
            if self.__is_goal__(curr_r, curr_c):
                return True
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                next_r, next_c = curr_r + dr, curr_c + dc
                if 0 <= next_r < 9 and 0 <= next_c < 9 and not visited[next_r][next_c]:
                    # controlla se la cella successiva non è occupata da un muro
                    blocked = False
                    for wall in board_walls:
                        if wall.orientation == 0:
                            if wall.cell1[0] == min(curr_r, next_r) and wall.cell1[1] == curr_c and wall.cell2[1] == curr_c:
                                blocked = True
                                break
                        else:
                            if wall.cell1[1] == min(curr_c, next_c) and wall.cell1[0] == curr_r and wall.cell2[0] == curr_r:
                                blocked = True
                                break
                    if not blocked:
                        visited[next_r][next_c] = True
                        q.append((next_r, next_c))      
        return False

    def switch_player(self):
        self.current_player = self.players[self.turn%PLAYERS_NUM]
        self.turn += 1
        
    def check_goal(self):            
        for player in self.players: 
            if ((player.goal == 'N' and player.r == 0) or (player.goal == 'S' and player.r == 8) or (player.goal == 'W' and player.c == 0) or (player.goal == "E" and player.c == 8)) and (not player.done):
                player.done = True
                print(f"{player.id} ha finito")

    def __is_goal__(self,r,c):
        player = self.current_player
        if (player.goal == 'N' and r == 0) or (player.goal == 'S' and r == 8) or (player.goal == 'W' and c == 0) or (player.goal == "E" and c == 8):
            return True
        return False


