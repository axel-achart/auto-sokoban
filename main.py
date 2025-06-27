
from display.display_game import DisplayGame
import numpy as np

# Charger la matrice depuis un fichier texte
#game_matrix = Matrix.load_matrix_from_file("level1.txt")

def initialize_matrix(rows, columns, obstacles, targets, boxes, player_position):

    matrix = np.zeros((rows, columns), dtype=int)

    for (r,c) in obstacles:
        matrix[r][c] = -1
    for (r,c) in targets :
        matrix[r][c] = 1
    for (r,c) in boxes:
        matrix[r][c] = 2
    matrix[player_position[0]][player_position[1]] = 3

    return matrix


rows = 10
columns = 10
obstacles = [(0, 0), (0, 1), (1, 0)]
targets = [(1, 2), (2, 2)]
boxes = [(2, 1),(3,3)]
player_position = (3, 1)
game_matrix = initialize_matrix(rows, columns, obstacles, targets, boxes, player_position)
print(game_matrix)

game = DisplayGame(game_matrix)
game.run()
