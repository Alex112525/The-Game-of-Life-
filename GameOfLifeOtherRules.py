import pygame
import numpy as np
import time

pygame.init()

width, height = 700, 700
screen = pygame.display.set_mode((height, width))

bg_color = 25, 25, 25  # Background color
screen.fill(bg_color)

X_cells, Y_cells = 60, 60  # Number of cell in X and Y

size_CW = width / X_cells  # size of cells
size_CH = height / Y_cells

game_state = np.zeros((X_cells, Y_cells))  # Matrix of zeros Alive = 1, Death = 0

game_state[30, 28] = 1
game_state[30, 29] = 1
game_state[31, 29] = 1

game_state[28, 30] = 1
game_state[29, 30] = 1
game_state[29, 31] = 1

Pause = True
count = 0
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

                # Rule 1
                #if game_state[x, y] == 0 and n_neigh == 2:
                #    newGame_state[x, y] = 1

                # Rule 2
                if game_state[x, y] == 1 and (n_neigh < 1 or n_neigh > 2):
                    newGame_state[x, y] = 0

                if n_neigh > 3:
                    newGame_state[x, y] = 0
                elif n_neigh == 2:
                    newGame_state[x, y] = 1

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
    if not Pause:
        pygame.image.save(screen, "screenshot" + str(count) + ".jpg")
        count += 1
