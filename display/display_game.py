from math import e
import pygame, copy, time
from config import *
from game.direction import DIRECTIONS
from game.build_game import GameLogic
from game.sokoban_solver import SokobanSolver
import os

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
        self.initial_matrix = copy.deepcopy(matrix)
        self.initial_player_pos = self.player_pos

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

        self.images = {
            0: pygame.image.load(os.path.join("assets", "img", "floor.png")),  # Case vide
            1: pygame.image.load(os.path.join("assets", "img", "wall.png")),   # Mur
            2: pygame.image.load(os.path.join("assets", "img", "box.png")),    # Boîte
            3: pygame.image.load(os.path.join("assets", "img", "player.png")), # Joueur
            4: pygame.image.load(os.path.join("assets", "img", "goal.png")), # Cible
        }


        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Sokoban Game")

        pygame.mixer.init()
        pygame.mixer.music.load("assets/sounds/music.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.4)

    def reset_to_initial_state(self):
        # Restaurer la matrice initiale
        self.initial_matrix = copy.deepcopy(self.initial_matrix)
        self.matrix = copy.deepcopy(self.initial_matrix)

        # Rechercher la position du joueur dans la nouvelle matrice
        for i, row in enumerate(self.matrix):
            for j, cell in enumerate(row):
                if cell == 3:
                    self.player_pos = (i, j)
                    break
            if self.player_pos:
                break

        # Réinstancier la logique, mais surtout... lier la matrice affichée à celle de la logique
        self.logic = GameLogic(copy.deepcopy(self.matrix), self.player_pos)
        self.matrix = self.logic.matrix  # 🔥 L'affichage et la logique utilisent la MÊME matrice




    def draw_button(self, surface, rect, text, base_color, hover_color, font):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = rect.collidepoint(mouse_pos)
        color = hover_color if is_hovered else base_color
        pygame.draw.rect(surface, color, rect)

        text_surf = font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)

        return is_hovered


    def draw_grid(self):
        # Charger les images une seule fois (au premier appel)
        if not hasattr(self, 'images'):
            self.images = {
                0: pygame.image.load("assets/img/empty.png").convert_alpha(),
                1: pygame.image.load("assets/img/wall.png").convert_alpha(),
                2: pygame.image.load("assets/img/box.png").convert_alpha(),
                3: pygame.image.load("assets/img/player.png").convert_alpha(),
                4: pygame.image.load("assets/img/target.png").convert_alpha()
            }
            # Redimensionner les images à CELL_SIZE
            for key in self.images:
                self.images[key] = pygame.transform.scale(self.images[key], (CELL_SIZE, CELL_SIZE))

        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):
                image = self.images.get(cell)
                if image:
                    self.screen.blit(image, (x * CELL_SIZE, y * CELL_SIZE))
                else:
                    # Couleur par défaut si pas d'image
                    pygame.draw.rect(
                        self.screen,
                        (200, 200, 255),
                        (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    )

                # Bordure fine autour de chaque cellule
                pygame.draw.rect(
                    self.screen,
                    (100, 100, 100),
                    (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                    1
                )


    def play_solution(self, moves):
        for move_dir, box_from, box_to in moves:
            if box_from and box_to: 
                print(f"Pushing box from {box_from} to {box_to}")
            self.logic.move(DIRECTIONS[move_dir])
            self.draw_grid()
            pygame.display.flip()
            pygame.time.delay(300) 

    def load_level(self, level_file):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            level_path = os.path.join(base_dir, "..", "levels", level_file)
            print(f"Chargement depuis : {level_path}")

            with open(level_path, "r") as f:
                self.matrix = [list(map(int, line.strip().split())) for line in f if line.strip()]
            self.rows = len(self.matrix)
            self.cols = len(self.matrix[0]) if self.rows > 0 else 0

            for r, row in enumerate(self.matrix):
                for c, val in enumerate(row):
                    if val == 3:  # Joueur
                        self.player_pos = (r, c)
                        break
                else:
                    continue
                break  

            self.logic = GameLogic(self.matrix, self.player_pos)
            print(f"Niveau chargé à partir de {level_file}.")
        except FileNotFoundError:
            print(f"Erreur : le fichier '{level_file}' n'a pas été trouvé dans le dossier 'levels/'.")
        except Exception as e:
            print(f"Erreur lors du chargement du niveau : {e}")

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
            "solve": pygame.Rect(600, 10, 150, 40),
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
                pygame.time.delay(3000)
                running = False

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
                        self.reset_to_initial_state()
                    elif buttons["cancel"].collidepoint(event.pos):
                        previous_state = self.logic.undo_move()
                        if previous_state is not None:
                            self.matrix, self.player_pos = previous_state
                            self.logic = GameLogic(copy.deepcopy(self.matrix), self.player_pos)
                            print("State Undone")
                        else:
                            print("No State to Undo")

                    elif buttons["level1"].collidepoint(event.pos):
                        self.load_level("niveau1.txt")  
                    elif buttons["level2"].collidepoint(event.pos):
                        self.load_level("niveau2.txt")  
                    elif buttons["level3"].collidepoint(event.pos):
                        self.load_level("niveau3.txt")  
                    elif buttons["quit"].collidepoint(event.pos):
                        running = False

                    elif buttons["solve"].collidepoint(event.pos):
                        solver = SokobanSolver(copy.deepcopy(self.matrix), self.player_pos)
                        solution = solver.solve()
                        if solution:
                            print("Niveau solvable ! Positions boîtes finales :", solution)
                        else:
                            print("Aucune solution trouvée.")

            pygame.display.flip()
            clock.tick(60)
        pygame.quit()
