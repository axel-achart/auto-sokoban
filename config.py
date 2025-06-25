import pygame

COLORS_INTERFACE = {
    0: (255, 255, 255),  # blanc - vide
    1: (0, 0, 0),        # noir - mur
    2: (255, 0, 0),      # rouge - joueur
    3: (0, 255, 0),      # vert - objectif
    4: (0, 0, 255),      # bleu - ennemi, par exemple
}

CELL_SIZE_ = 70 # px

button_color = (0, 200, 0)
hover_color = (0, 255, 0)
text_color = (255, 255, 255)
button_rect = pygame.Rect(200, 150, 200, 60)