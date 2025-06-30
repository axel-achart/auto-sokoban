from display.display_game import DisplayGame
from display.display_menu import display_menu
import numpy as np
import sys

def initialize_matrix(rows, columns, obstacles, targets, boxes, player_position):
    matrix = np.zeros((rows, columns), dtype=int)
    for (r, c) in obstacles:
        matrix[r][c] = -1
    for (r, c) in targets:
        matrix[r][c] = 1
    for (r, c) in boxes:
        matrix[r][c] = 2
    matrix[player_position[0]][player_position[1]] = 3
    return matrix

username = display_menu()
if not username:
    print("Aucun joueur sélectionné. Fermeture du jeu.")
    sys.exit()

print(f"Bienvenue, {username} ! Chargement du jeu...")

rows = 11
columns = 11
obstacles = [(0, 0), (0, 1), (1, 0)]
targets = [(1, 2), (2, 2)]
boxes = [(2, 1), (3, 3)]
player_position = (3, 1)

game_matrix = initialize_matrix(rows, columns, obstacles, targets, boxes, player_position)

game = DisplayGame(game_matrix, username=username, level_id=1)
game.run()
