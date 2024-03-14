from math import *
from vector_matrix import Vector
class Matrix:
    def __init__(self, rows):
        self.rows = rows

    def __add__(self, other):
        if isinstance(other, Matrix) and len(self.rows) == len(other.rows) and len(self.rows[0]) == len(other.rows[0]):
            return Matrix([[x + y for x, y in zip(row1, row2)] for row1, row2 in zip(self.rows, other.rows)])
        raise ValueError("Matrices must have the same dimensions")

    def __sub__(self, other):
        if isinstance(other, Matrix) and len(self.rows) == len(other.rows) and len(self.rows[0]) == len(other.rows[0]):
            return Matrix([[x - y for x, y in zip(row1, row2)] for row1, row2 in zip(self.rows, other.rows)])
        raise ValueError("Matrices must have the same dimensions")

    def __mul__(self, other):
        if isinstance(other, Matrix) and len(self.rows[0]) == len(other.rows):
            return Matrix([[sum(a * b for a, b in zip(row1, col)) for col in zip(*other.rows)] for row1 in self.rows])
        elif isinstance(other, Vector) and len(self.rows[0]) == len(other.elements):
            result = [sum(a * b for a, b in zip(row, other.elements)) for row in self.rows]
            return Vector(result)

        else:
            raise ValueError("Invalid multiplication")

    def euclidean_norm(self):
        print('fmd')
        return sqrt(sum(sum(x**2 for x in row) for row in self.rows))

    def max_norm(self):
        return max(abs(x) for row in self.rows for x in row)

    def __str__(self):
        # Перевизначення методу __str__ для виведення матриці у зручний формат
        return '\n'.join([' '.join(map(str, row)) for row in self.rows])