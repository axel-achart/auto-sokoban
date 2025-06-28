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

        # Vérification des coins
        if (is_blocking(r - 1, c) and is_blocking(r, c - 1)) or \
           (is_blocking(r - 1, c) and is_blocking(r, c + 1)) or \
           (is_blocking(r + 1, c) and is_blocking(r, c - 1)) or \
           (is_blocking(r + 1, c) and is_blocking(r, c + 1)):
            return True
        return False

    def solve(self):
        initial_state = (self.start_player, tuple([(r, c) for r, row in enumerate(self.original_matrix) for c, v in enumerate(row) if v == 2]))  # Positions des boîtes
        queue = deque([(initial_state, [])])  # Ajout d'une liste pour stocker les mouvements
        visited = set()
        visited.add(self.serialize_state(initial_state[1], self.start_player))

        while queue:
            (player, boxes), moves = queue.popleft()
            if self.is_win(boxes):
                return moves  # Retourne la liste des mouvements nécessaires

            for direction_name, direction in DIRECTIONS.items():
                new_player = (player[0] + direction[0], player[1] + direction[1])
                if self.is_free(new_player[0], new_player[1], boxes, self.original_matrix):
                    new_boxes = list(boxes)
                    # Vérification si le joueur pousse une boîte
                    if new_player in boxes:
                        box_index = boxes.index(new_player)
                        new_box = (new_player[0] + direction[0], new_player[1] + direction[1])
                        if self.is_free(new_box[0], new_box[1], new_boxes, self.original_matrix):
                            new_boxes[box_index] = new_box
                            move = (direction_name, new_player, new_box)
                            new_state = self.serialize_state(new_boxes, new_player)
                            if new_state not in visited:
                                visited.add(new_state)
                                queue.append(((new_player, tuple(new_boxes)), moves + [move]))
                        else:
                            continue  # Ne peut pas pousser la boîte
                    else:
                        new_state = self.serialize_state(new_boxes, new_player)
                        if new_state not in visited:
                            visited.add(new_state)
                            queue.append(((new_player, tuple(new_boxes)), moves + [(direction_name, None, None)]))

        return None  # Aucune solution trouvée
