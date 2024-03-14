from vector_matrix import Vector, Matrix

class LinearSystemSolver:
    def __init__(self, matrix, vector):
        self.matrix = matrix
        self.vector = vector

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'r') as file:
            matrix = []
            vector = []
            for line in file:
                if line.strip():  # Check if the line is not empty
                    values = [float(x) for x in line.split()]
                    matrix.append(values[:-1])
                    vector.append(values[-1])
        return cls(Matrix(matrix), Vector(vector))
