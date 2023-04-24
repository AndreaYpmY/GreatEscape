#!/usr/bin/python3

# Libs
import pygame
import os
from time import sleep

# Classes
from game import Game
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


pawns = [(RED_PLAYER,RED),(GREEN_PLAYER,GREEN),(BLUE_PLAYER,BLUE)]

def draw_window(game):
    WIN.blit(BACKGROUND, (0,0))
    draw_board(game)
    pygame.display.update()

def draw_board(game):
    for i in range(9):
        for j in range(9):
            pygame.draw.rect(WIN, DARK_BROWN, (i*CELL_SIZE+WALL_WIDTH*(i-1)+BOARD_PADDING//2, j*CELL_SIZE+WALL_WIDTH*(j-1)+BOARD_PADDING//2, CELL_SIZE, CELL_SIZE))
    # Draw players 
    for player in game.players:
            WIN.blit(player.image, (player.c*CELL_SIZE+WALL_WIDTH*(player.c-1)+BOARD_PADDING//2, player.r*CELL_SIZE+WALL_WIDTH*(player.r-1)+BOARD_PADDING//2, CELL_SIZE, CELL_SIZE))

    # Draw walls
    for player in game.players:
       for wall in player.walls:
            if(wall[0].orientation==0):
                pygame.draw.rect(WIN, player.color, (CELL_SIZE*wall[0].cell1[1]+WALL_WIDTH*(wall[0].cell1[1]-1)+BOARD_PADDING//2, CELL_SIZE*wall[0].cell1[0]+WALL_WIDTH*(wall[0].cell1[0]-2)+BOARD_PADDING//2, CELL_SIZE*2+WALL_WIDTH, WALL_WIDTH))
            else:
                pygame.draw.rect(WIN, player.color, (CELL_SIZE*wall[0].cell1[1]+WALL_WIDTH*(wall[0].cell1[1]-2)+BOARD_PADDING//2, CELL_SIZE*wall[0].cell1[0]+WALL_WIDTH*(wall[0].cell1[0]-1)+BOARD_PADDING//2, WALL_WIDTH, CELL_SIZE*2+WALL_WIDTH))

# TODO: FUNZIONE DI PROVA (DA RIMUOVERE GRZ)
def handle_movement(game, keys_pressed):
    player = game.current_player

    current_pos = (player.r, player.c)
    next_pos = (player.r, player.c)

    if(keys_pressed[pygame.K_UP]):
        next_pos = (player.r-1, player.c)
    elif(keys_pressed[pygame.K_DOWN]):
        next_pos = (player.r+1, player.c)
    elif(keys_pressed[pygame.K_LEFT]):
        next_pos = (player.r, player.c-1)
    elif(keys_pressed[pygame.K_RIGHT]):
        next_pos = (player.r, player.c+1)

    if game.valid_move(current_pos, next_pos):               # If no walls are traspassed
        player.new_position(next_pos[0], next_pos[1])
        game.switch_player()
    else:
        print(f"{game.current_player.id} è stato squalificato (mossa illegale)")
        

def main():
    run = True
    game = Game(pawns)
    clock = pygame.time.Clock()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        if (True in keys_pressed):
            handle_movement(game, keys_pressed)
    
        game.check_goal()
        draw_window(game)

        clock.tick(FPS)

if __name__ == '__main__':
    main()