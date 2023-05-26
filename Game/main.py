#!/usr/bin/python3

# Libs
import pygame
import os
from time import sleep
import time
from random import randint, shuffle
import math

# Classes
from game import Game
from player import Player
from wall import Wall
from timekeeper import Timekeeper

FPS = 30

TURN_LIMIT = 100

WIDTH, HEIGHT = 1300, 800
CELL_SIZE = 70
WALL_WIDTH = 5
BOARD_WIDTH = CELL_SIZE*9+WALL_WIDTH*8
BOARD_PADDING = 800-(CELL_SIZE*9+WALL_WIDTH*8)

HUD_WIDTH, HUD_HEIGHT = 470, 259

WIN = pygame.display.set_mode((WIDTH,HEIGHT))

GREY = (180,180,180)        # HEX: #B4B4B4
BLACK = (13,13,13)          # HEX: #0D0D0D
WHITE = (255,255,255)       # HEX: #FFFFFF
DARK_BROWN = (82,31,0)      # HEX: #521F00

RED = (255, 0, 0)           # HEX: #FF0000
GREEN = (57, 169, 57)       # HEX: #39A939

YELLOW = (211, 164, 71)     # HEX: #D3A447
BLUE = (9, 64, 190)         # HEX: #0940BE

pygame.display.set_caption("The Great Escape")

BACKGROUND_IMAGE = pygame.image.load(os.path.join("Assets","table.jpg"))
BACKGROUND = pygame.transform.scale_by(BACKGROUND_IMAGE, 0.7)

RED_PLAYER_IMAGE = pygame.image.load(os.path.join("Assets", "Pawns", "red.png"))
RED_PLAYER = pygame.transform.scale(RED_PLAYER_IMAGE, (70,70))

RED_HUD_IMAGE = pygame.image.load(os.path.join("Assets", "HUD", "red.png"))
RED_HUD = pygame.transform.scale(RED_HUD_IMAGE, (HUD_WIDTH,HUD_HEIGHT))

GREEN_PLAYER_IMAGE = pygame.image.load(os.path.join("Assets", "Pawns", "green.png"))
GREEN_PLAYER = pygame.transform.scale(GREEN_PLAYER_IMAGE, (70,70))
GREEN_HUD_IMAGE = pygame.image.load(os.path.join("Assets", "HUD", "green.png"))
GREEN_HUD = pygame.transform.scale(GREEN_HUD_IMAGE, (HUD_WIDTH,HUD_HEIGHT))

BLUE_PLAYER_IMAGE = pygame.image.load(os.path.join("Assets", "Pawns", "blue.png"))
BLUE_PLAYER = pygame.transform.scale(BLUE_PLAYER_IMAGE, (70,70))
BLUE_HUD_IMAGE = pygame.image.load(os.path.join("Assets", "HUD", "blue.png"))
BLUE_HUD = pygame.transform.scale(BLUE_HUD_IMAGE, (HUD_WIDTH,HUD_HEIGHT))

YELLOW_PLAYER_IMAGE = pygame.image.load(os.path.join("Assets", "Pawns", "yellow.png"))
YELLOW_PLAYER = pygame.transform.scale(YELLOW_PLAYER_IMAGE, (70,70))
YELLOW_HUD_IMAGE = pygame.image.load(os.path.join("Assets", "HUD", "yellow.png"))
YELLOW_HUD = pygame.transform.scale(YELLOW_HUD_IMAGE, (HUD_WIDTH,HUD_HEIGHT))

# Overlapping pawns
RED_BLUE_IMAGE = pygame.image.load(os.path.join("Assets", "Pawns", "red_blue.png"))
RED_BLUE = pygame.transform.scale(RED_BLUE_IMAGE, (70,70))

RED_GREEN_IMAGE = pygame.image.load(os.path.join("Assets", "Pawns", "red_green.png"))
RED_GREEN = pygame.transform.scale(RED_GREEN_IMAGE, (70,70))

RED_YELLOW_IMAGE = pygame.image.load(os.path.join("Assets", "Pawns", "red_yellow.png"))
RED_YELLOW = pygame.transform.scale(RED_YELLOW_IMAGE, (70,70))

GREEN_BLUE_IMAGE = pygame.image.load(os.path.join("Assets", "Pawns", "green_blue.png"))
GREEN_BLUE = pygame.transform.scale(GREEN_BLUE_IMAGE, (70,70))

YELLOW_BLUE_IMAGE = pygame.image.load(os.path.join("Assets", "Pawns", "yellow_blue.png"))
YELLOW_BLUE = pygame.transform.scale(YELLOW_BLUE_IMAGE, (70,70))

GREEN_YELLOW_IMAGE = pygame.image.load(os.path.join("Assets", "Pawns", "green_yellow.png"))
GREEN_YELLOW = pygame.transform.scale(GREEN_YELLOW_IMAGE, (70,70))

CELL_IMAGE = pygame.image.load(os.path.join("Assets", "cell.png"))
CELL = pygame.transform.scale(CELL_IMAGE, (CELL_SIZE,CELL_SIZE))

COUNTDOWN_3_IMAGE = pygame.image.load(os.path.join("Assets", "3.png"))
COUNTDOWN_3 = pygame.transform.scale(COUNTDOWN_3_IMAGE, (300,300))
COUNTDOWN_2_IMAGE = pygame.image.load(os.path.join("Assets", "2.png"))
COUNTDOWN_2 = pygame.transform.scale(COUNTDOWN_2_IMAGE, (300,300))
COUNTDOWN_1_IMAGE = pygame.image.load(os.path.join("Assets", "1.png"))
COUNTDOWN_1 = pygame.transform.scale(COUNTDOWN_1_IMAGE, (300,300))

assets = [(RED_PLAYER,RED_HUD,RED),(BLUE_PLAYER,BLUE_HUD,BLUE),(GREEN_PLAYER,GREEN_HUD,GREEN),(YELLOW_PLAYER,YELLOW_HUD,YELLOW)]

overlapping_pawns = {
    "red_blue": RED_BLUE, "red_green": RED_GREEN, "red_yellow": RED_YELLOW, "green_blue": GREEN_BLUE, "yellow_blue": YELLOW_BLUE, "green_yellow": GREEN_YELLOW
}

def draw_window(game, game_started, timekeeper, big_text, medium_text, small_text):
    WIN.blit(BACKGROUND, (0,0))
    
    draw_board(game)
    draw_players(game)
    draw_walls(game)
    
    info_text = pygame.font.SysFont("Arial", 24)
    hotkeys = info_text.render("m - mute audio     u - unmute audio    up - volume up      down - volume down", True, BLACK)
    WIN.blit(hotkeys, ((65, HEIGHT-15-hotkeys.get_height())))

    if not game_started:
        time_elapsed = time.time() - timekeeper.get_start_time()
        # 3 seconds countdown
        if time_elapsed >= 1 and time_elapsed < 2:
            WIN.blit(COUNTDOWN_2, (WIDTH-435,HEIGHT//2-150))
        elif time_elapsed >= 2 and time_elapsed < 3:
            WIN.blit(COUNTDOWN_1, (WIDTH-435,HEIGHT//2-150))
        elif time_elapsed < 1:
            WIN.blit(COUNTDOWN_3, (WIDTH-435,HEIGHT//2-150))
    else:
        draw_hud(game, big_text, medium_text, small_text)

    if game.winner is not None:
        winner_name = medium_text.render(f"{game.current_player.name}", True, game.current_player.color)
        winner_status = medium_text.render(f"won!", True, BLACK)
        WIN.blit(winner_name, (WIDTH-450, HEIGHT//2-winner_name.get_height()))
        WIN.blit(winner_status, (WIDTH-450, HEIGHT//2))

    pygame.display.update()

def draw_hud(game, big_text, medium_text, small_text):
    # Just handles two players for now
    if len(game.players) == 2:
        # Get the hud images
        player_1_hud = game.players[0].hud
        player_2_hud = game.players[1].hud

        # Get the number of walls left
        player_1_walls_left = game.players[0].remaining_walls
        player_2_walls_left = game.players[1].remaining_walls

        # Draw the hud image
        WIN.blit(player_1_hud, (WIDTH-500,50))
        WIN.blit(player_2_hud, (WIDTH-500,HEIGHT-50-HUD_HEIGHT))
        
        # Create the texts that will be displayed
        walls_left_text = small_text.render(f"Walls left:", True, WHITE)
        player_1_name_text = small_text.render(f"{game.players[0].name}", True, WHITE)
        player_2_name_text = small_text.render(f"{game.players[1].name}", True, WHITE)
        player_1_walls_left_text = big_text.render(get_player_walls_string(player_1_walls_left), True, WHITE)
        player_2_walls_left_text = big_text.render(get_player_walls_string(player_2_walls_left), True, WHITE)

        # Draw the texts
        WIN.blit(player_1_name_text, (WIDTH-450, 60+player_1_name_text.get_height()//2))
        WIN.blit(walls_left_text, (WIDTH-450, 60+player_1_name_text.get_height()//2+80))
        WIN.blit(player_2_name_text, (WIDTH-450, HEIGHT-40-HUD_HEIGHT+player_2_name_text.get_height()//2))
        WIN.blit(walls_left_text, (WIDTH-450, HEIGHT-40-HUD_HEIGHT+player_2_name_text.get_height()//2+80))
        WIN.blit(player_1_walls_left_text, (WIDTH-150, 60+player_1_name_text.get_height()//2+80))
        WIN.blit(player_2_walls_left_text, (WIDTH-150, HEIGHT-40-HUD_HEIGHT+player_2_name_text.get_height()//2+80))

def get_player_walls_string(walls_left):
    # It will always be two characters long
    if walls_left < 10:
        return f"0{walls_left}"
    return f"{walls_left}"

def draw_board(game):
    for player in game.players:
        start_pos = (0,0)
        end_pos = (0,0)
        if player.goal == "N":
            start_pos = (BOARD_PADDING//2-WALL_WIDTH, BOARD_PADDING//2-WALL_WIDTH*5)
            end_pos = ((BOARD_PADDING//2)+BOARD_WIDTH, BOARD_PADDING//2-WALL_WIDTH*5)
        elif player.goal == "S":
            start_pos = (BOARD_PADDING//2-WALL_WIDTH, BOARD_PADDING//2+BOARD_WIDTH+WALL_WIDTH*3)
            end_pos = (BOARD_PADDING//2+BOARD_WIDTH, BOARD_PADDING//2+BOARD_WIDTH+WALL_WIDTH*3)
        elif player.goal == "W":
            start_pos = (BOARD_PADDING//2-WALL_WIDTH*5, BOARD_PADDING//2-WALL_WIDTH)
            end_pos = (BOARD_PADDING//2-WALL_WIDTH*5, BOARD_PADDING//2+WALL_WIDTH+BOARD_WIDTH)
        elif player.goal == "E":
            start_pos = (BOARD_PADDING//2+BOARD_WIDTH+WALL_WIDTH*3, BOARD_PADDING//2-WALL_WIDTH)
            end_pos = (BOARD_PADDING//2+BOARD_WIDTH+WALL_WIDTH*3, BOARD_PADDING//2+WALL_WIDTH+BOARD_WIDTH)
        
        draw_dashed_line(WIN, player.color, start_pos, end_pos)
        
    # Draw underlying layer of a brighter color
    pygame.draw.rect(WIN, GREY, (BOARD_PADDING//2-WALL_WIDTH, BOARD_PADDING//2-WALL_WIDTH, BOARD_WIDTH, BOARD_WIDTH))
    # Draw board
    for i in range(9):
        for j in range(9):
            WIN.blit(CELL, (i*CELL_SIZE+WALL_WIDTH*(i-1)+BOARD_PADDING//2, j*CELL_SIZE+WALL_WIDTH*(j-1)+BOARD_PADDING//2, CELL_SIZE, CELL_SIZE))
    
def draw_players(game):
    # Takes player positions, we use them after to avoid drawing mini pawns on top of the big ones
    player_pos = [] 
    for player in game.players:
        player_pos.append((player.r,player.c))

    # Overlapping pawns is only handled when there are 2 players for now
    if len(game.players) == 2:
        if game.players[0].r == game.players[1].r and game.players[0].c == game.players[1].c:
            player_colors = []
            player_colors.append(game.players[0].color)
            player_colors.append(game.players[1].color) 
            if RED in player_colors and BLUE in player_colors:
                WIN.blit(overlapping_pawns["red_blue"], (game.players[0].c*CELL_SIZE+WALL_WIDTH*(game.players[0].c-1)+BOARD_PADDING//2, game.players[0].r*CELL_SIZE+WALL_WIDTH*(game.players[0].r-1)+BOARD_PADDING//2, CELL_SIZE, CELL_SIZE))
            elif RED in player_colors and YELLOW in player_colors:
                WIN.blit(overlapping_pawns["red_yellow"], (game.players[0].c*CELL_SIZE+WALL_WIDTH*(game.players[0].c-1)+BOARD_PADDING//2, game.players[0].r*CELL_SIZE+WALL_WIDTH*(game.players[0].r-1)+BOARD_PADDING//2, CELL_SIZE, CELL_SIZE))
            elif RED in player_colors and GREEN in player_colors:
                WIN.blit(overlapping_pawns["red_green"], (game.players[0].c*CELL_SIZE+WALL_WIDTH*(game.players[0].c-1)+BOARD_PADDING//2, game.players[0].r*CELL_SIZE+WALL_WIDTH*(game.players[0].r-1)+BOARD_PADDING//2, CELL_SIZE, CELL_SIZE))
            elif YELLOW in player_colors and BLUE in player_colors:
                WIN.blit(overlapping_pawns["yellow_blue"], (game.players[0].c*CELL_SIZE+WALL_WIDTH*(game.players[0].c-1)+BOARD_PADDING//2, game.players[0].r*CELL_SIZE+WALL_WIDTH*(game.players[0].r-1)+BOARD_PADDING//2, CELL_SIZE, CELL_SIZE))
            elif GREEN in player_colors and YELLOW in player_colors:
                WIN.blit(overlapping_pawns["green_yellow"], (game.players[0].c*CELL_SIZE+WALL_WIDTH*(game.players[0].c-1)+BOARD_PADDING//2, game.players[0].r*CELL_SIZE+WALL_WIDTH*(game.players[0].r-1)+BOARD_PADDING//2, CELL_SIZE, CELL_SIZE))
            elif GREEN in player_colors and BLUE in player_colors:
                WIN.blit(overlapping_pawns["green_blue"], (game.players[0].c*CELL_SIZE+WALL_WIDTH*(game.players[0].c-1)+BOARD_PADDING//2, game.players[0].r*CELL_SIZE+WALL_WIDTH*(game.players[0].r-1)+BOARD_PADDING//2, CELL_SIZE, CELL_SIZE))
        else:
            # Draw players 
            for player in game.players:
                WIN.blit(player.pawn, (player.c*CELL_SIZE+WALL_WIDTH*(player.c-1)+BOARD_PADDING//2, player.r*CELL_SIZE+WALL_WIDTH*(player.r-1)+BOARD_PADDING//2, CELL_SIZE, CELL_SIZE))
        
        for player in game.players:
            draw_old_positions(player, player_pos)

def draw_walls(game):
    # Draw walls
    for player in game.players:
        for wall in player.walls:
            if(wall[0].orientation==0):
                pygame.draw.rect(WIN, player.color, (CELL_SIZE*wall[0].cell1[1]+WALL_WIDTH*(wall[0].cell1[1]-1)+BOARD_PADDING//2, CELL_SIZE*wall[0].cell1[0]+WALL_WIDTH*(wall[0].cell1[0]-2)+BOARD_PADDING//2, CELL_SIZE*2+WALL_WIDTH, WALL_WIDTH))
            else:
                pygame.draw.rect(WIN, player.color, (CELL_SIZE*wall[0].cell1[1]+WALL_WIDTH*(wall[0].cell1[1]-2)+BOARD_PADDING//2, CELL_SIZE*wall[0].cell1[0]+WALL_WIDTH*(wall[0].cell1[0]-1)+BOARD_PADDING//2, WALL_WIDTH, CELL_SIZE*2+WALL_WIDTH))

''' Original function found at https://codereview.stackexchange.com/questions/70143/drawing-a-dashed-line-with-pygame '''
def draw_dashed_line(surf, color, start_pos, end_pos, width=5, dash_length=10):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dl = dash_length

    if (x1 == x2):
        ycoords = [y for y in range(y1, y2, dl if y1 < y2 else -dl)]
        xcoords = [x1] * len(ycoords)
    elif (y1 == y2):
        xcoords = [x for x in range(x1, x2, dl if x1 < x2 else -dl)]
        ycoords = [y1] * len(xcoords)

    next_coords = list(zip(xcoords[1::2], ycoords[1::2]))
    last_coords = list(zip(xcoords[0::2], ycoords[0::2]))
    for (x1, y1), (x2, y2) in zip(next_coords, last_coords):
        start = (round(x1), round(y1))
        end = (round(x2), round(y2))
        pygame.draw.line(surf, color, start, end, width)

'''
# TODO: FUNZIONE DI PROVA (DA RIMUOVERE GRZ)
def handle_play(game, keys_pressed):
    player = game.current_player

    is_movement = True
    current_pos = (player.r, player.c)
    next_pos = (player.r, player.c)
    wall = ()

    choose = input("Vuoi muoverti o piazzare un muro? (1/2)")
    if choose == "1":
        if(keys_pressed[pygame.K_UP]):
            next_pos = (player.r-1, player.c)
        elif(keys_pressed[pygame.K_DOWN]):
            next_pos = (player.r+1, player.c)
        elif(keys_pressed[pygame.K_LEFT]):
            next_pos = (player.r, player.c-1)
        elif(keys_pressed[pygame.K_RIGHT]):
            next_pos = (player.r, player.c+1)
    else:
        muro = input("Vuoi inserire le coordinate o vuoi un muro random? (1/2)")
        if(muro == "1"):
            row = int(input("Row: "))
            col = int(input("Col: "))
            orientation = int(input("Orientation: "))
            wall = player.generate_wall(row,col,orientation)
        else:
            wall = get_random_wall(player)
        is_movement = False                 # I'm going to place a wall
            


    if is_movement:
        if game.valid_movement(current_pos, next_pos):               # If no walls are traspassed
            player.new_position(next_pos[0], next_pos[1])
            game.switch_player()
        else:
            print(f"{game.current_player.id} è stato squalificato (mossa illegale)")
    else:
        if game.valid_wall(wall):
            player.place_wall(wall)
            game.switch_player()
'''

def get_random_wall(player):
    orientation = randint(0,1)  
    row = 0
    col = 0
    if orientation == 0:
        row = randint(1,8)
        col = randint(0,7)
    else:
        row = randint(0,7)
        col = randint(1,8)
    
    return player.generate_wall(row,col,orientation)


def draw_old_positions(player,player_pos):
    for pos in player.old_positions:
        if player.id == 1:
            x = pos[1] * CELL_SIZE + WALL_WIDTH * (pos[1] - 1) + BOARD_PADDING//2 + 30
            y = pos[0] * CELL_SIZE + WALL_WIDTH * (pos[0] - 1) + BOARD_PADDING//2 + 30
        else:
            x = pos[1] * CELL_SIZE + WALL_WIDTH * (pos[1] - 1) + BOARD_PADDING//2 + CELL_SIZE - 30
            y = pos[0] * CELL_SIZE + WALL_WIDTH * (pos[0] - 1) + BOARD_PADDING//2 + CELL_SIZE - 30

        if not (pos[0],pos[1]) in player_pos:
            pygame.draw.circle(WIN, player.color, (x,y), 5)

def handle_volume_control(keys_pressed, ost):
    volume = ost.get_volume()
    if keys_pressed[pygame.K_UP]:
        ost.set_volume(volume + 0.1)
    if keys_pressed[pygame.K_DOWN]:
        ost.set_volume(volume - 0.1)
    if keys_pressed[pygame.K_m]:
        ost.set_volume(0)
    if keys_pressed[pygame.K_u] and volume == 0:
        ost.set_volume(0.2)

def main():
    pygame.font.init()
    pygame.mixer.init()

    ost = [pygame.mixer.Sound(os.path.join("Assets", "Sounds", "laxity_again.mp3")), pygame.mixer.Sound(os.path.join("Assets", "Sounds", "giana_sisters.mp3")), pygame.mixer.Sound(os.path.join("Assets", "Sounds", "zerd_01.mp3")), pygame.mixer.Sound(os.path.join("Assets", "Sounds", "fairstars.mp3"))]
    shuffle(ost)
    victory = pygame.mixer.Sound(os.path.join("Assets", "Sounds", "victory.mp3"))

    ost[0].set_volume(0)        # Music starts muted
    ost[0].play()
    
    try:
        big_text = pygame.font.Font(os.path.join("Assets", "Fonts", "Barrio-Regular.ttf"), 70)
        small_text = pygame.font.Font(os.path.join("Assets", "Fonts", "Barrio-Regular.ttf"), 40)
        medium_text = pygame.font.Font(os.path.join("Assets", "Fonts", "Barrio-Regular.ttf"), 55)
    except:
        raise Exception("Font file not found")

    run = True
    clock = pygame.time.Clock()
    game = Game(assets)
    game_started = False
    timekeeper = Timekeeper()
    timekeeper.start()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            keys_pressed = pygame.key.get_pressed()
            if (True in keys_pressed):
                handle_volume_control(keys_pressed, ost[0])   
                #handle_play(game, keys_pressed)
                
        if game_started:
            game.check_goal()
            
            if time.time() - timekeeper.get_start_time() > timekeeper.MAX_TURN_DURATION_SECONDS:
                game.switch_player()
                if game.turn > 1:
                    if game.winner is not None:
                        # TODO: Implementare fine del gioco, con cambio di scenario
                        run = False
                        print(f"Winner: {game.winner}")    
        else:
            time_elapsed = time.time() - timekeeper.get_start_time()
            if time_elapsed >= 3:
                game_started = True
                game.switch_player()

        draw_window(game, game_started, timekeeper, big_text, medium_text, small_text)

        clock.tick(FPS)
    
    # Start the 5 seconds cooldown after the game ends
    timekeeper.start()
    run_cooldown = True
    ost[0].stop()
    victory.set_volume(0.2)
    victory.play()
    while time.time() - timekeeper.get_start_time() < 5 and run_cooldown:      
        if event.type == pygame.QUIT:
            run_cooldown = False
        draw_window(game, game_started, timekeeper, big_text, medium_text, small_text)
        clock.tick(FPS)
    pygame.mixer.music.stop()    

if __name__ == '__main__':
    main()