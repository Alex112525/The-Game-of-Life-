import pygame
import numpy as np
import time

pygame.init()

width, height = 500, 500
screen = pygame.display.set_mode((height, width))

bg_color = 25, 25, 25  # Background color
screen.fill(bg_color)

X_cells, Y_cells = 30, 30  # Number of cell in X and Y

size_CW = width / X_cells  # size of cells
size_CH = height / Y_cells

game_state = np.zeros((X_cells, Y_cells))  # Matrix of zeros Alive = 1, Death = 0

# Stick Automate
# game_state[5, 3] = 1
# game_state[5, 4] = 1
# game_state[5, 5] = 1
# game_state[5, 6] = 1
# game_state[5, 7] = 1
# game_state[5, 8] = 1
# game_state[5, 9] = 1
# game_state[5, 10] = 1
# game_state[5, 11] = 1
# game_state[5, 12] = 1
# game_state[5, 13] = 1
# game_state[5, 14] = 1
Pause = False

while True:
    # Matrix for save the changes
    newGame_state = np.copy(game_state)

    screen.fill(bg_color)  # Clean screen
    time.sleep(0.5)

    # Events in the keyboard and mouse
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            Pause = not Pause

        mouse_click = pygame.mouse.get_pressed()
        if sum(mouse_click) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / size_CW)), int(np.floor(posY / size_CH))
            newGame_state[celX, celY] = 1

    for y in range(0, X_cells):
        for x in range(0, Y_cells):

            if not Pause:
                # Sum of all neighbors
                n_neigh = game_state[(x - 1) % X_cells, (y - 1) % Y_cells] + \
                          game_state[x % X_cells, (y - 1) % Y_cells] + \
                          game_state[(x + 1) % X_cells, (y - 1) % Y_cells] + \
                          game_state[(x - 1) % X_cells, y % Y_cells] + \
                          game_state[(x + 1) % X_cells, y % Y_cells] + \
                          game_state[(x - 1) % X_cells, (y + 1) % Y_cells] + \
                          game_state[x % X_cells, (y + 1) % Y_cells] + \
                          game_state[(x + 1) % X_cells, (y + 1) % Y_cells]

                # Rule 1: A cell dead with exactly 3 neighbors alive, "Alive"
                if game_state[x, y] == 0 and n_neigh == 3:
                    newGame_state[x, y] = 1

                # Rule 2: A cell Alive with less of two o more than 3 neighbors, "Dead
                elif game_state[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGame_state[x, y] = 0

            # coordinates for each square
            poly = [(x * size_CW, y * size_CH),
                    ((x + 1) * size_CW, y * size_CH),
                    ((x + 1) * size_CW, (y + 1) * size_CH),
                    (x * size_CW, (y + 1) * size_CH)]

            # if a cell is alive draw
            if newGame_state[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    game_state = np.copy(newGame_state)
    pygame.display.flip()
