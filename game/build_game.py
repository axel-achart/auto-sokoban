class Level:
    def __init__(self, path):
        self.map_data = []
        self.player = None
        self.boxes = []
        self.goals = []
        self.walls = []
        self.load_level(path)

    def load_level(self, path):
        with open(path, "r") as f:
            for y, line in enumerate(f):
                row = []
                for x, char in enumerate(line.strip()):
                    row.append(char)
                    if char == "#":
                        self.walls.append((x, y))
                    elif char == "@":
                        self.player = (x, y)
                    elif char == "$":
                        self.boxes.append((x, y))
                    elif char == ".":
                        self.goals.append((x, y))
                self.map_data.append(row)

#Ce code stocke les coordonnées des objets dans des listes 

