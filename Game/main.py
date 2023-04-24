#!/usr/bin/python3

# Libs
import pygame
import os
from random import choice, randint

# Classes
from player import Player
from wall import Wall

FPS = 30

TURN_LIMIT = 100

WIDTH, HEIGHT = 800, 800
CELL_SIZE = 70
WALL_WIDTH = 5
BOARD_PADDING = WIDTH-(CELL_SIZE*9+WALL_WIDTH*8)

WIN = pygame.display.set_mode((WIDTH,HEIGHT))

BLACK = (0,0,0)
WHITE = (255,255,255)
DARK_BROWN = (82,31,0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.display.set_caption("The Great Escape")

BACKGROUND_IMAGE = pygame.image.load(os.path.join("Assets","table.jpg"))
BACKGROUND = pygame.transform.scale_by(BACKGROUND_IMAGE, 0.5)

RED_PLAYER_IMAGE = pygame.image.load(os.path.join("Assets", "Pawns", "red.png"))
RED_PLAYER = pygame.transform.scale(RED_PLAYER_IMAGE, (70,70))

GREEN_PLAYER_IMAGE = pygame.image.load(os.path.join("Assets", "Pawns", "green.png"))
GREEN_PLAYER = pygame.transform.scale(GREEN_PLAYER_IMAGE, (70,70))

BLUE_PLAYER_IMAGE = pygame.image.load(os.path.join("Assets", "Pawns", "blue.png"))
BLUE_PLAYER = pygame.transform.scale(BLUE_PLAYER_IMAGE, (70,70))


players = []
pawns = [(RED_PLAYER,RED),(GREEN_PLAYER,GREEN),(BLUE_PLAYER,BLUE)]

def draw_window():
    WIN.blit(BACKGROUND, (0,0))
    draw_board()
    pygame.display.update()

def draw_board():
    for i in range(9):
        for j in range(9):
            pygame.draw.rect(WIN, DARK_BROWN, (i*CELL_SIZE+WALL_WIDTH*(i-1)+BOARD_PADDING//2, j*CELL_SIZE+WALL_WIDTH*(j-1)+BOARD_PADDING//2, CELL_SIZE, CELL_SIZE))
    # Draw players 
    for player in players:
            WIN.blit(player.image, (player.c*CELL_SIZE+WALL_WIDTH*(player.c-1)+BOARD_PADDING//2, player.r*CELL_SIZE+WALL_WIDTH*(player.r-1)+BOARD_PADDING//2, CELL_SIZE, CELL_SIZE))

    # Draw walls
    for player in players:
       for wall in player.walls:
            if(wall[0].orientation==0):
                pygame.draw.rect(WIN, player.color, (CELL_SIZE*wall[0].cell1[1]+WALL_WIDTH*(wall[0].cell1[1]-1)+BOARD_PADDING//2, CELL_SIZE*wall[0].cell1[0]+WALL_WIDTH*(wall[0].cell1[0]-2)+BOARD_PADDING//2, CELL_SIZE*2+WALL_WIDTH, WALL_WIDTH))
            else:
                pygame.draw.rect(WIN, player.color, (CELL_SIZE*wall[0].cell1[1]+WALL_WIDTH*(wall[0].cell1[1]-2)+BOARD_PADDING//2, CELL_SIZE*wall[0].cell1[0]+WALL_WIDTH*(wall[0].cell1[0]-1)+BOARD_PADDING//2, WALL_WIDTH, CELL_SIZE*2+WALL_WIDTH))

# TODO: FUNZIONE DI PROVA (DA RIMUOVERE GRZ)
def handle_movement(player, keys_pressed):
    current_pos = (player.r, player.c)
    next_pos = (player.r, player.c)

    if(keys_pressed[pygame.K_UP]) and player.r > 0:
        next_pos = (player.r-1, player.c)
    elif(keys_pressed[pygame.K_DOWN]) and player.r < 8:
        next_pos = (player.r+1, player.c)
    elif(keys_pressed[pygame.K_LEFT]) and player.c > 0:
        next_pos = (player.r, player.c-1)
    elif(keys_pressed[pygame.K_RIGHT]) and player.c < 8:
        next_pos = (player.r, player.c+1)

    if valid_move(current_pos, next_pos):               # If no walls are traspassed
        player.new_position(next_pos[0], next_pos[1])

def valid_move(current_pos, next_pos):
    for player in players:
        for wall in player.walls:
            if (wall[0].cell1 == current_pos and wall[0].cell2 == next_pos) or (wall[0].cell2 == current_pos and wall[0].cell1 == next_pos) or (wall[1].cell1 == current_pos and wall[1].cell2 == next_pos) or (wall[1].cell2 == current_pos and wall[1].cell1 == next_pos):
                return False
    return True
    

def create_players():
    # Player(1,0,7,RED_PLAYER,RED), Player(2,8,2,GREEN_PLAYER,GREEN)
    goals = ['N', 'S', 'W', 'E']
    for i in range(2):                  # Only two players (for now)
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

        players.append(Player(i+1, start_r, start_c, goal, pawns[i][0], pawns[i][1]))

def check_goal():            
    for player in players: 
        if ((player.goal == 'N' and player.r == 0) or (player.goal == 'S' and player.r == 8) or (player.goal == 'W' and player.c == 0) or (player.goal == "E" and player.c == 8)) and (not player.done):
            player.done = True
            print(f"{player.id} ha finito")

def main():
    run = True
    create_players()
    # TODO: MURI DI PROVA (DA RIMUOVERE GRZ)
    players[0].walls.append((Wall(3,4,1), Wall(4,4,1)))
    players[0].walls.append((Wall(6,3,0), Wall(6,4,0)))
    players[1].walls.append((Wall(2,2,0), Wall(2,3,0)))
    print(f"Red player goal: {players[0].goal}")
    print(f"Green player goal: {players[1].goal}")
    turn = 0
    clock = pygame.time.Clock()
    while run and turn < 100:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys_pressed = pygame.key.get_pressed()
        handle_movement(players[0], keys_pressed)
        
        check_goal()
        draw_window()

if __name__ == '__main__':
    main()