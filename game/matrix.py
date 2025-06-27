import numpy as np

class Matrix:
    @staticmethod
    def load_matrix_from_file(filepath):
        symbol_to_value = {
            '#': -1,  # obstacle
            '.': 1,   # cible
            'B': 2,   # boîte
            'P': 3,   # joueur
            ' ': 0    # vide
        }

        matrix = []

        with open(filepath, 'r') as file:
            for line in file:
                row = [symbol_to_value.get(char, 0) for char in line.rstrip('\n')]
                matrix.append(row)

        return np.array(matrix)
