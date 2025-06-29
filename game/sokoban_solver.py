from collections import deque

class State:
    def __init__(self, player_pos, box_positions):
        self.player = player_pos
        self.boxes = frozenset(box_positions)

    def __hash__(self):
        return hash((self.player, self.boxes))

    def __eq__(self, other):
        return self.player == other.player and self.boxes == other.boxes


class SokobanSolver:
    def __init__(self, matrix, player_position):
        self.matrix = matrix
        self.player_position = player_position
        self.start_state = self._get_initial_state()
        self.goal_positions = self._get_goal_positions()

    def _get_initial_state(self):
        boxes = set()
        for i, row in enumerate(self.matrix):
            for j, cell in enumerate(row):
                if cell == 2:  # caisse
                    boxes.add((i, j))
        return State(self.player_position, boxes)

    def _get_goal_positions(self):
        goals = set()
        for i, row in enumerate(self.matrix):
            for j, cell in enumerate(row):
                if cell == 1:  # cible
                    goals.add((i, j))
        return frozenset(goals)

    def _is_inside(self, x, y):
        return 0 <= x < len(self.matrix) and 0 <= y < len(self.matrix[0])

    def _get_neighbors(self, state):
        directions = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1)
        }

        neighbors = []

        for direction, (dy, dx) in directions.items():
            y, x = state.player
            ny, nx = y + dy, x + dx

            if not self._is_inside(ny, nx) or self.matrix[ny][nx] == -1:
                continue

            if (ny, nx) in state.boxes:
                ny2, nx2 = ny + dy, nx + dx
                if not self._is_inside(ny2, nx2):
                    continue
                if self.matrix[ny2][nx2] == -1 or (ny2, nx2) in state.boxes:
                    continue
                new_boxes = set(state.boxes)
                new_boxes.remove((ny, nx))
                new_boxes.add((ny2, nx2))
                neighbors.append((State((ny, nx), new_boxes), direction))
            else:
                neighbors.append((State((ny, nx), state.boxes), direction))

        return neighbors

    def solve(self):
        visited = set()
        queue = deque()
        queue.append((self.start_state, []))

        while queue:
            current_state, path = queue.popleft()

            if current_state.boxes == self.goal_positions:
                return path  # Liste de directions : ["up", "left", "right", ...]

            if current_state in visited:
                continue

            visited.add(current_state)

            for neighbor, direction in self._get_neighbors(current_state):
                queue.append((neighbor, path + [direction]))

        return None  # Pas de solution
