from math import e
import pygame
from config import *
from game.direction import DIRECTIONS
from game.build_game import GameLogic

COLORS = COLORS_INTERFACE

CELL_SIZE = CELL_SIZE_

class DisplayGame:
    def __init__(self, matrix):
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0]) if self.rows > 0 else 0
        self.width = self.cols * CELL_SIZE
        self.height = self.rows * CELL_SIZE
        self.player_pos = None
        for i, row in enumerate(self.matrix):
            for j, cell in enumerate(row):
                if cell == 3: 
                    self.player_pos = (i, j)
                    break
            if self.player_pos:
                break

        if self.player_pos is None:
            raise ValueError("Le joueur ('player') est introuvable dans la matrice.")

        self.logic = GameLogic(self.matrix, self.player_pos)


        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Sokoban Game")

    def draw_grid(self):
        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):
                color = COLORS.get(cell, (200, 200, 255))  # gris par défaut
                pygame.draw.rect(
                    self.screen,
                    color,
                    (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )
                # Ligne de séparation
                pygame.draw.rect(
                    self.screen,
                    (100, 100, 100),
                    (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                    1
                )

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            self.screen.fill((255, 255, 255)) 
            self.draw_grid()
            if self.logic.check_win():
                font = pygame.font.Font(None, 74)
                text = font.render("You Win!", True, (0, 255, 0))
                text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
                self.screen.blit(text, text_rect) 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_UP:
                        self.logic.move(DIRECTIONS["up"])
                    elif event.key == pygame.K_DOWN:
                        self.logic.move(DIRECTIONS["down"])
                    elif event.key == pygame.K_LEFT:
                        self.logic.move(DIRECTIONS["left"])
                    elif event.key == pygame.K_RIGHT:
                        self.logic.move(DIRECTIONS["right"])

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
