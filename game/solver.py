from collections import deque

class Solver:
    def __init__(self, level):
        self.level = level
        self.walls = set(level.walls)
        self.goals = set(level.goals)

    def solve(self):
        start = (self.level.player, tuple(sorted(self.level.boxes)))
        visited = set()
        visited.add(start)
        queue = deque()
        queue.append((start, []))  # état, chemin jusqu'ici

        while queue:
            (player, boxes), path = queue.popleft()
            for direction in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
                new_player, new_boxes = self.simulate_move(player, boxes, direction)
                if (new_player, tuple(sorted(new_boxes))) not in visited:
                    visited.add((new_player, tuple(sorted(new_boxes))))
                    if self.is_win(new_boxes):
                        return path + [direction]
                    queue.append(((new_player, tuple(sorted(new_boxes))), path + [direction]))

        return None  # aucune solution trouvée

    def is_win(self, boxes):
        return all(pos in self.goals for pos in boxes)

    def simulate_move(self, player, boxes, direction):
        dx, dy = self.direction_to_delta(direction)
        x, y = player
        new_pos = (x + dx, y + dy)
        boxes = list(boxes)

        if new_pos in self.walls:
            return player, boxes

        if new_pos in boxes:
            box_index = boxes.index(new_pos)
            new_box_pos = (new_pos[0] + dx, new_pos[1] + dy)
            if new_box_pos in self.walls or new_box_pos in boxes:
                return player, boxes  # impossible de pousser
            boxes[box_index] = new_box_pos
            return new_pos, boxes  # pousse la caisse
        else:
            return new_pos, boxes  # déplacement simple

    def direction_to_delta(self, direction):
        return {
            'UP': (0, -1),
            'DOWN': (0, 1),
            'LEFT': (-1, 0),
            'RIGHT': (1, 0)
        }[direction]
