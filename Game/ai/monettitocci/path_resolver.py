import heapq

class PathResolver():
    def __init__(self,players,my_id):
        self.players = players
        self.my_id = my_id
        self.walls = self.__get_all_walls(self.players)

        # Minimum paths cost, each element is a tuple (start_cell, end_cell, cost) 
        self.min_paths_cost = []

    def generate_min_paths_cost(self):
        pos_to_check = []
        

        for player in self.players:
            neighbors = self.__get_neighbors((player.r,player.c),9,9)
            pos_to_check.append((player.id, (player.r,player.c), player.goal))
            for neighbor in neighbors:
                pos_to_check.append((player.id, neighbor, player.goal))

        for pos in pos_to_check:
            player_id = pos[0]
            initial_node = pos[1]
            player_goal = pos[2]
            path = self.__dijkstra(initial_node,player_goal)
            if path is not None:
                goal_node = path[-1]
                self.min_paths_cost.append((player_id,initial_node,goal_node,len(path)-1))
        
    def get_min_paths_cost(self):
        return self.min_paths_cost

    '''
        Put the cost limits in the following format: [(player_id, cost_limit), ...] in a list
    '''
    def get_cost_limits(self):
        cost_limits = []
        for player in self.players:
            costs = []
            for path in self.min_paths_cost:
                if path[0] == player.id:
                    costs.append(path[3])
            cost_limits.append((player.id,max(costs)))
        
        return cost_limits

    def __get_all_walls(self,players):
        walls = []
        for player in players:
            for wall in player.walls:
                walls.append(wall)
        return walls

    # Dijkstra algorithm, which returns the minimum path from a cell to another
    def __dijkstra(self, initial_node, player_goal):
        rows, cols = 9, 9

        #initial_node = (player.r,player.c)

        ## Creazione di una matrice delle distanze con valori infiniti per tutti i nodi tranne il nodo di partenza
        distances = [[float('inf')] * cols for _ in range(rows)]
        distances[initial_node[0]][initial_node[1]] = 0
        
        ## Coda di priorità per memorizzare i nodi da visitare
        queue = [(0, initial_node)]
        
        ## Dizionario per tenere traccia dei predecessori di ogni nodo
        predecessors = {}
        
        while queue:
            current_dist, current_node = heapq.heappop(queue)
            
            if self.__is_goal(player_goal, current_node[0], current_node[1]):
                ## Se il nodo corrente è quello di destinazione, restituisci il percorso trovato
                return self.__construct_path(predecessors, initial_node, current_node)

            ## Scopri i vicini del nodo corrente
            neighbors = self.__get_neighbors(current_node, rows, cols)
            
            for neighbor in neighbors:
                row, col = neighbor
                new_dist = current_dist + 1  ## Peso degli archi è 1
                
                if new_dist < distances[row][col]:
                    ## Aggiorna la distanza minima per il vicino e il predecessore
                    distances[row][col] = new_dist
                    predecessors[neighbor] = current_node
                    heapq.heappush(queue, (new_dist, neighbor))
        
        ## Se non è stato trovato un percorso tra i nodi, restituisci None
        return None

    def __get_neighbors(self,node,rows,cols):
        row, col = node
        neighbors = []
        
        if row > 0 and not self.__wall_exists((row,col),(row-1,col)):
            neighbors.append((row - 1, col))
        if row < rows - 1 and not self.__wall_exists((row,col),(row+1,col)):
            neighbors.append((row + 1, col))
        if col > 0 and not self.__wall_exists((row,col),(row,col-1)):
            neighbors.append((row, col - 1))
        if col < cols - 1 and not self.__wall_exists((row,col),(row,col+1)):
            neighbors.append((row, col + 1))
        
        return neighbors

    def __wall_exists(self,cell1,cell2):
        for player in self.players:
            for wall in player.walls:
                if (wall[0].cell1 == cell1 and wall[0].cell2 == cell2) or (wall[0].cell2 == cell1 and wall[0].cell1 == cell2) or (wall[1].cell1 == cell1 and wall[1].cell2 == cell2) or (wall[1].cell2 == cell1 and wall[1].cell1 == cell2):
                    return True
        return False

    def __construct_path(self,predecessors, start_node, end_node):
        path = [end_node]
        current_node = end_node

        while current_node != start_node:
            current_node = predecessors[current_node]
            path.append(current_node)
        
        path.reverse()
        return path      

    def __is_goal(self,player_goal,r,c):
        if (player_goal == 'N' and r == 0) or (player_goal == 'S' and r == 8) or (player_goal == 'W' and c == 0) or (player_goal == "E" and c == 8):
            return True
        return False     
