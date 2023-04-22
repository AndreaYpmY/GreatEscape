#!/usr/bin/python3

# Libs
import pygame
import os

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

players = [Player(1,4,0,RED_PLAYER,RED), Player(2,2,8,GREEN_PLAYER,GREEN)]

# TODO: MURI DI PROVA (DA RIMUOVERE GRZ)
players[0].walls.append((Wall(3,4,1), Wall(4,4,1)))
players[0].walls.append((Wall(6,3,0), Wall(6,4,0)))
players[1].walls.append((Wall(2,2,0), Wall(2,3,0)))

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
    if(keys_pressed[pygame.K_UP]) and player.r > 0:
        player.new_position(player.r-1, player.c)
    elif(keys_pressed[pygame.K_DOWN]) and player.r < 8:
        player.new_position(player.r+1, player.c)
    elif(keys_pressed[pygame.K_LEFT]) and player.c > 0:
        player.new_position(player.r, player.c-1)
    elif(keys_pressed[pygame.K_RIGHT]) and player.c < 8:
        player.new_position(player.r, player.c+1)

def main():
    run = True
    turn = 0
    clock = pygame.time.Clock()
    while run and turn < 100:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys_pressed = pygame.key.get_pressed()
        handle_movement(players[0], keys_pressed)
        draw_window()

if __name__ == '__main__':
    main()