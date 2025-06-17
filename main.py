"""
Initialize matrix with dimensions [rows][columns]
For each cell in matrix:
    If cell is an obstacle, set value to -1
    If cell is an empty space, set value to 0
    If cell is a target location, set value to 1
    If cell contains a box, set value to 2
    If cell contains the player, set value to 3
"""

import numpy as np
def initialize_matrix(rows, columns, obstacles, targets, boxes, player_position):
    #On crée une matrice de zéros
    matrix = np.zeros((rows, columns), dtype=int)
    #On remplace chaque matrice par les valeurs connues
    for (r,c) in obstacles:
        matrix[r][c] = -1
    for (r,c) in targets :
        matrix[r][c] = 1
    for (r,c) in boxes:
        matrix[r][c] = 2
    matrix[player_position[0]][player_position[1]] = 3

    return matrix

#Exemple matrix

rows = 5
columns = 5
obstacles = [(0, 0), (0, 1), (1, 0)]
targets = [(1, 2), (2, 2)]
boxes = [(2, 1)]
player_position = (3, 1)

game_matrix = initialize_matrix(rows, columns, obstacles, targets, boxes, player_position)
print(game_matrix)

"""
Function movePlayer(direction):
    Determine new position based on direction (up, down, left, right)
    If new position is within bounds:
        If new position is an obstacle (-1):
            Return "Move blocked by wall"
        Else if new position is empty (0) or target (1):
            Update player position in matrix
        Else if new position contains a box (2):
            Calculate box's new position in the same direction
            If box's new position is empty (0) or target (1):
                Move box to new position
                Update player position
            Else:
                Return "Move blocked by box"
    Else:
        Return "Move out of bounds"
"""



"""
Function checkWinCondition():
    For each target location (1) in matrix:
        If corresponding cell does not contain a box (2):
            Return False
    Return True  // All boxes are on target locations
"""



"""
While game is running:
    Get user input for movement
    Call movePlayer(input)
    If checkWinCondition() is True:
        Print "You win!"
        End game
"""