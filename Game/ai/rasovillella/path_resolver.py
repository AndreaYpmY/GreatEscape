
import networkx as nx
from .path import Path

import sys
sys.path.append("..\\..")
from player import Player
from wall import Wall

class PathResolver():

    def __init__(self,players,myId):
        self.players = players
        self.myId = myId
        self.walls = []
        self.destination_nodes = -1
        self.start_cell = (self.players[self.myId-1].r,self.players[self.myId-1].c)
        self.graph = nx.DiGraph()
        self.path = []
        self.graphInit()

    def graphInit(self):

        for r in range(9):
            for c in range(9):
                current_cell = (r, c)
                self.graph.add_node(current_cell)
        
        for r in range(9):
                for c in range(9):
                    current_cell = (r, c)
                    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        neighbor = (r + dr, c + dc)
                        if 0 <= neighbor[0] < 9 and 0 <= neighbor[1] < 9:
                            self.graph.add_edge(current_cell, neighbor, weight=1)
        
        for player in self.players:
            if(player.id == self.myId):
                if(player.goal == "E"):
                    self.destination_nodes = [(r, c) for r in range(9) for c in range(9) if c == 8]
                elif(player.goal == "W"):
                    self.destination_nodes = [(r, c) for r in range(9) for c in range(9) if c == 0]
                elif(player.goal == "N"):
                    self.destination_nodes = [(r, c) for r in range(9) for c in range(9) if r == 0]
                elif(player.goal == "S"):
                    self.destination_nodes = [(r, c) for r in range(9) for c in range(9) if r == 8]
        
        for node in self.destination_nodes:
            self.graph.add_edge(node, 'Destination', weight=0)


    def loadWall(self):

        for player in self.players:
            for wall in player.walls:
                smallWall1 = (wall[0].cell1[0],wall[0].cell1[1],wall[0].cell2[0],wall[0].cell2[1])
                smallWall2 = (wall[1].cell1[0],wall[1].cell1[1],wall[1].cell2[0],wall[1].cell2[1])
                self.walls.append(smallWall1)
                self.walls.append(smallWall2)
        
        for wall in self.walls:
            r, c, r1, c1 = wall
            if self.graph.has_edge((r, c), (r1, c1)):
                self.graph.remove_edge((r, c), (r1, c1))
                self.graph.remove_edge((r1, c1), (r, c))
        
    def findMinPath(self):

        self.loadWall()
        shortest_path = nx.shortest_path(self.graph, source=self.start_cell, target='Destination')
        shortest_path_lenght = nx.shortest_path_length(self.graph, source=self.start_cell, target= 'Destination')-1
        shortest_path.pop(0)
        shortest_path.pop()

        for cell in shortest_path:
            path = Path(self.myId,cell[0],cell[1],shortest_path_lenght)
            self.path.append(path)
        