"""
Initialize matrix with dimensions [rows][columns]
For each cell in matrix:
    If cell is an obstacle, set value to -1
    If cell is an empty space, set value to 0
    If cell is a target location, set value to 1
    If cell contains a box, set value to 2
    If cell contains the player, set value to 3


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


Function checkWinCondition():
    For each target location (1) in matrix:
        If corresponding cell does not contain a box (2):
            Return False
    Return True  // All boxes are on target locations


While game is running:
    Get user input for movement
    Call movePlayer(input)
    If checkWinCondition() is True:
        Print "You win!"
        End game
"""