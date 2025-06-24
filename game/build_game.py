from direction import DIRECTIONS

class GameLogic:
    def __init__(self, matrix, player_position):
        self.matrix = matrix
        self.player_position = player_position

    def check_valid_moves(self, direction):
        dx, dy = direction
        x, y = self.player_position
        nx, ny = x + dx, y + dy

        if not (0 <= nx < len(self.matrix) and 0 <= ny < len(self.matrix[0])):
            return False

        cell = self.matrix[nx][ny]

        if cell == "wall":
            return False
        elif cell == "box":
            return self.check_valid_push(direction)
        else:
            return True

    def move(self, direction):
        if self.check_valid_moves(direction):
            dx, dy = direction
            x, y = self.player_position
            nx, ny = x + dx, y + dy

            if self.matrix[nx][ny] == "box":
                self.push(direction)

            self.matrix[x][y] = "empty"
            self.matrix[nx][ny] = "player"
            self.player_position = (nx, ny)

    def check_valid_push(self, direction):
        dx, dy = direction
        x, y = self.player_position
        bx, by = x + dx, y + dy
        nx, ny = bx + dx, by + dy

        if not (0 <= nx < len(self.matrix) and 0 <= ny < len(self.matrix[0])):
            return False

        return self.matrix[nx][ny] in ("empty", "target")

    def push(self, direction):
        dx, dy = direction
        x, y = self.player_position
        bx, by = x + dx, y + dy
        nx, ny = bx + dx, by + dy

        self.matrix[bx][by] = "empty"
        self.matrix[nx][ny] = "box"
