from collections import deque
import copy
from game.direction import DIRECTIONS

class SokobanSolver:
    def __init__(self, matrix, player_pos):
        self.original_matrix = matrix
        self.start_player = player_pos
        self.targets = [(r, c) for r, row in enumerate(matrix) for c, v in enumerate(row) if v == 1]
        self.rows = len(matrix)
        self.cols = len(matrix[0])
    
    def is_win(self, boxes):
        return all(pos in self.targets for pos in boxes)

    def serialize_state(self, boxes, player):
        return (tuple(sorted(boxes)), player)

    def is_in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_free(self, r, c, boxes, matrix):
        return self.is_in_bounds(r, c) and matrix[r][c] != -1 and (r, c) not in boxes

    def reachable_positions(self, start, matrix, boxes):
        """ BFS to find all positions the player can reach given the current state """
        visited = set()
        queue = deque([start])
        visited.add(start)

        while queue:
            y, x = queue.popleft()
            for dy, dx in DIRECTIONS.values():
                ny, nx = y + dy, x + dx
                if (ny, nx) not in visited and self.is_free(ny, nx, boxes, matrix):
                    visited.add((ny, nx))
                    queue.append((ny, nx))
        return visited
    def is_deadlock_position(self, pos, matrix):
        r, c = pos
        if pos in self.targets:
            return False  # Une cible n'est jamais considérée bloquée

        def is_blocking(y, x):
            if not self.is_in_bounds(y, x):
                return True  # Hors limite = mur virtuel
            return matrix[y][x] == -1  # Mur

    # Coin haut-gauche, haut-droit, bas-gauche, bas-droit
        if (is_blocking(r - 1, c) and is_blocking(r, c - 1)) or \
            (is_blocking(r - 1, c) and is_blocking(r, c + 1)) or \
            (is_blocking(r + 1, c) and is_blocking(r, c - 1)) or \
            (is_blocking(r + 1, c) and is_blocking(r, c + 1)):
            return True

        return False

    def solve(self):
        matrix = copy.deepcopy(self.original_matrix)
        # Initial boxes
        boxes = {(r, c) for r, row in enumerate(matrix) for c, v in enumerate(row) if v == 2}
        visited = set()
        queue = deque()
        queue.append((boxes, self.start_player, []))
        visited.add(self.serialize_state(boxes, self.start_player))

        while queue:
            current_boxes, player, path = queue.popleft()

            if self.is_win(current_boxes):
                return path

            reachable = self.reachable_positions(player, matrix, current_boxes)

            for box in current_boxes:
                for dir_name, (dy, dx) in DIRECTIONS.items():
                    by, bx = box
                    py, px = by - dy, bx - dx  # position derrière la boîte
                    ny, nx = by + dy, bx + dx  # destination de la boîte

                    if (py, px) in reachable and self.is_free(ny, nx, current_boxes, matrix):
                        if self.is_deadlock_position((ny, nx), matrix):
                            continue

                        new_boxes = set(current_boxes)
                        new_boxes.remove((by, bx))
                        new_boxes.add((ny, nx))
                        
                        new_player = (by, bx)  # après avoir poussé, le joueur est à la place de l’ancienne boîte

                        state = self.serialize_state(new_boxes, new_player)
                        if state not in visited:
                            visited.add(state)
                            queue.append((new_boxes, new_player, path + [(dir_name, (by, bx), (ny, nx))]))

        return None
