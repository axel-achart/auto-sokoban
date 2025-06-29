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

    def is_in_bounds(self, y, x):
        return 0 <= y < len(self.original_matrix) and 0 <= x < len(self.original_matrix[0])
    
    def is_free(self, y, x, boxes, matrix):
        if not self.is_in_bounds(y, x):
            return False
        if matrix[y][x] == -1:  # Mur
            return False
        if (y, x) in boxes:  # Boîte
            return False
        return True
    
    
    def is_win(self, boxes):
        return all(pos in self.targets for pos in boxes)

    def serialize_state(self, boxes, player):
        return (tuple(sorted(boxes)), player)

    def reachable_positions(self, start, matrix, boxes):
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

    def is_deadlock_position(self, pos, boxes):
        r, c = pos
        if pos in self.targets:
            return False  # Une cible n'est jamais considérée bloquée

        def is_blocking(y, x):
            if not self.is_in_bounds(y, x):
                return True  # Hors limite = mur virtuel
            return self.original_matrix[y][x] == -1 or (y, x) in boxes  # Mur ou autre boîte

        # Vérification des coins
        if (is_blocking(r - 1, c) and is_blocking(r, c - 1)) or \
           (is_blocking(r - 1, c) and is_blocking(r, c + 1)) or \
           (is_blocking(r + 1, c) and is_blocking(r, c - 1)) or \
           (is_blocking(r + 1, c) and is_blocking(r, c + 1)):
            return True
        # Vérification si la boîte ne peut pas atteindre une cible
        reachable = self.reachable_positions(pos, self.original_matrix, boxes)
        if not any(target in reachable for target in self.targets):
            return True
        
        return False

    def solve(self):
        initial_state = (self.start_player, tuple())  # (position du joueur, positions des boîtes)
        queue = deque([initial_state])
        visited = set()
        visited.add(self.serialize_state((), self.start_player))

        while queue:
            player, boxes = queue.popleft()
            if self.is_win(boxes):
                return boxes  # Retourne les positions des boîtes si gagnant

            for direction in DIRECTIONS.values():
                new_player = (player[0] + direction[0], player[1] + direction[1])
                if self.is_free(new_player[0], new_player[1], boxes, self.original_matrix):
                    new_boxes = list(boxes)
                    # Vérification si le joueur pousse une boîte
                    if new_player in boxes:
                        box_index = boxes.index(new_player)
                        new_box = (new_player[0] + direction[0], new_player[1] + direction[1])
                        if self.is_free(new_box[0], new_box[1], new_boxes, self.original_matrix):
                            new_boxes[box_index] = new_box
                        else:
                            continue  # Ne peut pas pousser la boîte
                    new_state = self.serialize_state(new_boxes, new_player)
                    if new_state not in visited:
                        visited.add(new_state)
                        queue.append((new_player, tuple(new_boxes)))

        return None  # Aucune solution trouvée

