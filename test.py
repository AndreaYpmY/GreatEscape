import pygame

# Inizializza Pygame
pygame.init()

# Imposta le dimensioni della finestra di gioco
WINDOW_SIZE = (800, 800)
screen = pygame.display.set_mode(WINDOW_SIZE)

# Imposta lo sfondo in nero
screen.fill((0, 0, 0))

# Imposta i contorni delle celle in rosso
cell_color = (255, 0, 0)

# Imposta le dimensioni e il numero di celle della griglia
cell_size = 80
num_cells = 9

# Disegna la griglia
for i in range(num_cells):
    for j in range(num_cells):
        rect = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, cell_color, rect, 1)

# Aggiorna lo schermo
pygame.display.flip()

# Loop principale del gioco
game_running = True
while game_running:
    # Gestisce gli eventi (cioè le interazioni dell'utente con la finestra di gioco)
    for event in pygame.event.get():
        # Se l'utente chiude la finestra, interrompe il gioco
        if event.type == pygame.QUIT:
            game_running = False

# Termina Pygame
pygame.quit()