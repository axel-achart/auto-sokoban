from math import e
import pygame
from config import *

COLORS = COLORS_INTERFACE

CELL_SIZE = CELL_SIZE_

class DisplayGame:
    def __init__(self, matrix):
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0]) if self.rows > 0 else 0
        self.width = self.cols * CELL_SIZE
        self.height = self.rows * CELL_SIZE

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Sokoban Game")

    def draw_grid(self):
        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):
                color = COLORS.get(cell, (200, 200, 200))  # gris par défaut
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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_UP:
                        
                    elif event.key == pygame.K_DOWN:
                        
                    elif event.key == pygame.K_LEFT:
                        
                    elif event.key == pygame.K_RIGHT:
                        
            pygame.display.flip()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()