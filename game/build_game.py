from copy import deepcopy
from game.direction import DIRECTIONS
import pygame, copy
class GameLogic:
    def __init__(self, matrix, player_position):
        self.matrix = matrix
        self.player_position = player_position
        self.boxes = [(r, c) for r, row in enumerate(matrix) for c, val in enumerate(row) if val == 2]
        # Stocker les cibles pour pouvoir les remettre si besoin
        self.targets = [(r, c) for r, row in enumerate(matrix) for c, val in enumerate(row) if val == 1]

        pygame.mixer.init()
        self.sound_mouvement = pygame.mixer.Sound("assets/sounds/mouvement.mp3")
        self.sound_mouvement.set_volume(1.0)

        self.move_history = [(self.player_position, tuple(self.boxes))]
        self.matrix_history = [copy.deepcopy(self.matrix)]

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
            self.save_matrix()
            
            dy, dx = direction
            y, x = self.player_position
            ny, nx = y + dy, x + dx
            

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
    
    def save_matrix(self):
        self.matrix_history.append(copy.deepcopy(self.matrix))
        self.move_history.append((self.player_position, tuple(self.boxes)))
    
    def undo(self):
        if self.move_history and len(self.matrix_history) > 1:
            last_state = self.move_history.pop()
            self.matrix = self.matrix_history.pop()
            self.player_position = last_state[0]
            self.boxes = list(last_state[1])
            print(self.matrix)
            print("State Undone")