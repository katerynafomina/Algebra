from math import *

class Matrix:
    def __init__(self, rows):
        if not isinstance(rows, list):
            raise TypeError("Rows must be provided as a list")
        if not rows:
            raise ValueError("Rows cannot be empty")
        num_columns = len(rows[0])
        if not all(len(row) == num_columns for row in rows):
            raise ValueError("All rows must have the same length")
        self.rows = rows

    def __getitem__(self, index):
        return self.rows[index]

    def __len__(self):
        return len(self.rows)

    def neighbors(self, vertex):
        return [i for i, val in enumerate(self.rows[vertex]) if val != 0]

    def degree(self, vertex):
        return sum(1 for val in self.rows[vertex] if val != 0)

    def reorder(self, order):
        n = len(self.rows)
        new_rows = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                new_rows[i][j] = self.rows[order[i]][order[j]]
        self.rows = new_rows

    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.rows])


class Vector:
    def __init__(self, elements):
        self.elements = elements

    def __add__(self, other):
        if isinstance(other, Vector) and len(self.elements) == len(other.elements):
            return Vector([x + y for x, y in zip(self.elements, other.elements)])
        raise ValueError("Vectors must be of the same length")

    def __len__(self):
        return len(self.elements)

    def __sub__(self, other):
        if isinstance(other, Vector) and len(self.elements) == len(other.elements):
            return Vector([x - y for x, y in zip(self.elements, other.elements)])
        raise ValueError("Vectors must be of the same length")

    def __mul__(self, other):
        if isinstance(other, Vector):
            if len(self.elements) != len(other.elements):
                raise ValueError("Vectors must be of the same length for multiplication")
            result = [x * y for x, y in zip(self.elements, other.elements)]
            return Vector(result)
        elif isinstance(other, Matrix):
            if len(self.elements) != len(other.rows[0]):
                raise ValueError("Vector length must match the number of columns in the matrix")
            result = [sum(x * y for x, y in zip(self.elements, col)) for col in zip(*other.rows)]
            return Vector(result)
        raise ValueError("Multiplication is only supported with scalar, vector, or matrix")

    def euclidean_norm(self):
        print('mdf')
        return sum(x**2 for x in self.elements) ** 0.5

    def max_norm(self):
        return max(abs(x) for x in self.elements)

    def __str__(self):
        return ' '.join(map(str, self.elements))

    def __len__(self):
        return len(self.elements)

    def __getitem__(self, index):
        return self.elements[index]

    def __setitem__(self, index, value):
        self.elements[index] = value
class BandedMatrix:
    def __init__(self, lower_bandwidth, upper_bandwidth, rows):
        self.lower_bandwidth = lower_bandwidth
        self.upper_bandwidth = upper_bandwidth
        self.rows = rows
        self.n = len(rows[0])  # Кількість стовпців у головній діагоналі

    def __getitem__(self, index):
        i, j = index
        band = j - i
        if band < -self.lower_bandwidth or band > self.upper_bandwidth:
            return 0  # Elements outside the bandwidth are zero
        return self.rows[band + self.lower_bandwidth][i]


    def __getitem__(self, index):
        if isinstance(index, tuple):
            i, j = index
            band = j - i
            if band < -self.lower_bandwidth or band > self.upper_bandwidth:
                return 0  # Elements outside the bandwidth are zero
            return self.rows[band + self.lower_bandwidth][i]
        elif isinstance(index, int):
            # Handle single index for getting a row
            return self.rows[index]

    def __setitem__(self, index, value):
        if isinstance(index, tuple):
            i, j = index
            band = j - i
            if band < -self.lower_bandwidth or band > self.upper_bandwidth:
                raise IndexError("Trying to access element outside the bandwidth")
            self.rows[band + self.lower_bandwidth][i] = value
        elif isinstance(index, int):
            # Handle single index for setting a row
            self.rows[index] = value

    def to_full_matrix(self):
        full_matrix = [[0] * self.n for _ in range(self.n)]
        for i in range(self.n):
            for j in range(max(0, i - self.lower_bandwidth), min(self.n, i + self.upper_bandwidth + 1)):
                full_matrix[i][j] = self[i, j]
        return full_matrix

    def __str__(self):
        matrix_str = ""
        for row in self.rows:
            matrix_str += " ".join(str(elem) for elem in row) + "\n"
        return matrix_str
