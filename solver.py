from vector_matrix import Vector, Matrix
class LinearSystemSolver:
    def __init__(self, matrix, vector):
        self.matrix = matrix
        self.vector = vector
        self.upper_triangular = None
        self.lower_triangular = None

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
    

    @staticmethod
    def gaussian_elimination(matrix, vector):
        A = [row[:] for row in matrix.rows]
        b = vector.elements[:]
        n = len(A)

        upper_triangular = [row[:] for row in A]
        lower_triangular = [[0] * n for _ in range(n)]

        for i in range(n):
            lower_triangular[i][i] = 1.0

            max_index = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_index][i]):
                    max_index = j

            A[i], A[max_index] = A[max_index], A[i]
            b[i], b[max_index] = b[max_index], b[i]

            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]

        decomp_matrix=A
            

        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = b[i]
            for j in range(i + 1, n):
                x[i] -= A[i][j] * x[j]
            x[i] /= A[i][i]

        return Vector(x), Matrix(decomp_matrix)
    
    @staticmethod
    def inverse_matrix(matrix):
        n = len(matrix.rows)
        inverse = Matrix([[0] * n for _ in range(n)])
        
        for i in range(n):
            column = Vector([1 if j == i else 0 for j in range(n)])
            inverted_column, _ = LinearSystemSolver.gaussian_elimination(matrix, column)

            for j in range(len(inverted_column)):
                inverse.rows[j][i] = inverted_column.elements[j]

        for i in range(n):
            for j in range(n):
                inverse.rows[i][j] = round(inverse.rows[i][j], 2)

        return inverse

    
    # def inverse_matrix(self):
    #     # Compute the inverse matrix using the lower and upper triangular matrices
    #     n = len(self.matrix.rows)
    #     identity = Matrix([[1 if i == j else 0 for j in range(n)] for i in range(n)])
    #     inverted_matrix = []

    #     for j in range(n):
    #         column = [identity.rows[i][j] for i in range(n)]
    #         inverted_column = self.__solve_column(self.lower_triangular, self.upper_triangular, column)
    #         inverted_matrix.append(inverted_column.elements)

    #     return Matrix(inverted_matrix)

    # def __solve_column(self, lower_triangular, upper_triangular, column):
    #     # Internal method to solve one column using forward and backward substitution
    #     n = len(lower_triangular)
    #     y = [0] * n
    #     x = [0] * n

    #     # Forward substitution (Ly = b)
    #     for i in range(n):
    #         y[i] = column[i]
    #         for j in range(i):
    #             y[i] -= lower_triangular[i][j] * y[j]
    #         y[i] /= lower_triangular[i][i]

    #     # Backward substitution (Ux = y)
    #     for i in range(n - 1, -1, -1):
    #         x[i] = y[i]
    #         for j in range(i + 1, n):
    #             x[i] -= upper_triangular[i][j] * x[j]
    #         x[i] /= upper_triangular[i][i]

    #     return Vector(x)
