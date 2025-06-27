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

        pygame.mixer.init()
        pygame.mixer.music.load("assets/sounds/music.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.4)


    def draw_button(self, surface, rect, text, base_color, hover_color, font):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = rect.collidepoint(mouse_pos)
        color = hover_color if is_hovered else base_color
        pygame.draw.rect(surface, color, rect)

        # Générer le texte du bouton ici
        text_surf = font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)

        return is_hovered


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

        font = pygame.font.SysFont(None, 30)
        buttons = {
            "reset": pygame.Rect(10, 10, 100, 40),
            "cancel": pygame.Rect(120, 10, 100, 40),
            "level1": pygame.Rect(230, 10, 80, 40),
            "level2": pygame.Rect(320, 10, 80, 40),
            "level3": pygame.Rect(410, 10, 80, 40),
            "quit": pygame.Rect(500, 10, 80, 40),
        }
        button_rect = pygame.Rect(600, 10, 150, 40)
        button_color = (50, 50, 200)
        hover_color = (100, 100, 255)

        while running:
            self.screen.fill((255, 255, 255)) 
            self.draw_grid()
            if self.logic.check_win():
                font = pygame.font.Font(None, 74)
                text = font.render("You Win!", True, (0, 255, 0))
                text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
                self.screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.delay(2000)  # Pause pour afficher le message de victoire
                running = False  # Quitter le jeu après la victoire
            hovered = self.draw_button(self.screen, button_rect, "CLIQUE MOI", button_color, hover_color, font)

            for name, rect in buttons.items():
                hovered = rect.collidepoint(pygame.mouse.get_pos())
                color = (200, 0, 0) if hovered else (100, 100, 100)
                pygame.draw.rect(self.screen, color, rect)
                text = font.render(name.upper(), True, (255, 255, 255))
                self.screen.blit(text, text.get_rect(center=rect.center))

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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if buttons["reset"].collidepoint(event.pos):
                        self.logic.reset()
                    elif buttons["cancel"].collidepoint(event.pos):
                        self.logic.undo()
                    elif buttons["level1"].collidepoint(event.pos):
                        self.load_level("niveau1.txt")  # Créé des fichiers pour chaque niveau ?
                    elif buttons["level2"].collidepoint(event.pos):
                        self.load_level("niveau2.txt")  # Créé des fichiers pour chaque niveau ?
                    elif buttons["level3"].collidepoint(event.pos):
                        self.load_level("niveau3.txt")  # Créé des fichiers pour chaque niveau ?
                    elif buttons["quit"].collidepoint(event.pos):
                        running = False

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
