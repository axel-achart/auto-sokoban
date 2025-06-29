from copy import deepcopy
from game.direction import DIRECTIONS
import pygame, copy

class GameLogic:
    def __init__(self, matrix, player_position):
        self.matrix = matrix
        self.player_position = player_position
        # Stocker les cibles pour pouvoir les remettre si besoin
        self.targets = [(r, c) for r, row in enumerate(matrix) for c, val in enumerate(row) if val == 1]

        pygame.mixer.init()
        self.sound_mouvement = pygame.mixer.Sound("assets/sounds/mouvement.mp3")
        self.sound_mouvement.set_volume(1.0)

        self.move_history = []

    def check_valid_moves(self, direction):
        dy, dx = direction
        y, x = self.player_position
        ny, nx = y + dy, x + dx

        # Correction 1 : inversion des dimensions Y/X
        if not (0 <= ny < len(self.matrix) and 0 <= nx < len(self.matrix[0])):
            return False

        cell = self.matrix[ny][nx]

        if cell == -1:  # obstacle
            return False
        elif cell == 2:  # box
            return self.check_valid_push(direction)
        else:
            return True

    def move(self, direction):
        if self.check_valid_moves(direction):
            dy, dx = direction
            y, x = self.player_position
            ny, nx = y + dy, x + dx
            self.save_state()

            if self.sound_mouvement:
                self.sound_mouvement.play()

            if self.matrix[ny][nx] == 2:
                self.push(direction)

            # Remettre la valeur cible si nécessaire à l'ancienne position du joueur
            if (y, x) in self.targets:
                self.matrix[y][x] = 1
            else:
                self.matrix[y][x] = 0

            self.matrix[ny][nx] = 3
            self.player_position = (ny, nx)
            

    def check_valid_push(self, direction):
        dy, dx = direction
        y, x = self.player_position
        ny, nx = y + dy, x + dx
        ny2, nx2 = ny + dy, nx + dx

        if not (0 <= ny2 < len(self.matrix) and 0 <= nx2 < len(self.matrix[0])):
            return False

        return self.matrix[ny2][nx2] in (0, 1)  # cases vides ou cibles

    def push(self, direction):
        dy, dx = direction
        y, x = self.player_position
        ny, nx = y + dy, x + dx
        ny2, nx2 = ny + dy, nx + dx

        # Remettre la valeur cible si nécessaire à l'ancienne position de la boîte
        if (ny, nx) in self.targets:
            self.matrix[ny][nx] = 1
        else:
            self.matrix[ny][nx] = 0

        self.matrix[ny2][nx2] = 2

    def check_win(self):
        # Vérifie si toutes les cibles sont occupées par des boîtes
        return all(self.matrix[r][c] == 2 for r, c in self.targets)
    
    def save_state(self):
        # On sauvegarde un tuple : (copie matrice, position joueur)
        self.move_history.append((deepcopy(self.matrix), self.player_position))
        print(f"State saved. Total moves: {len(self.move_history)}")


    def undo_move(self):
        if self.move_history:
            previous_matrix = self.move_history.pop()
            # Retrouver la position du joueur dans previous_matrix :
            for r, row in enumerate(previous_matrix):
                for c, val in enumerate(row):
                    if val == 3:
                        player_pos = (r, c)
                        break
                else:
                    continue
                break
            else:
                player_pos = None  # cas improbable

            return previous_matrix, player_pos
        return None
