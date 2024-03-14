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
    
    def gauss_elimination(self):
        # Copy the matrix to avoid modifications to the original matrix
        A = [row[:] for row in self.matrix.rows]
        b = self.vector.elements[:]
        n = len(A)

        for i in range(n):
            # Find the maximum element in the column to choose the pivot element
            max_index = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_index][i]):
                    max_index = j
            # Swap rows
            A[i], A[max_index] = A[max_index], A[i]
            b[i], b[max_index] = b[max_index], b[i]

            # Gaussian elimination
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]

        # Back substitution to find the solution
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = b[i]
            for j in range(i + 1, n):
                x[i] -= A[i][j] * x[j]
            x[i] /= A[i][i]

        return Vector(x)
    
    def decompose_matrix(self):
        # Decompose the matrix into upper and lower triangular matrices
        upper_triangular = []
        lower_triangular = []

        for i in range(len(self.matrix.rows)):
            upper_row = [0] * i + self.matrix.rows[i][i:]
            lower_row = self.matrix.rows[i][:i] + [0] * (len(self.matrix.rows) - i - 1) + [1]

            upper_triangular.append(upper_row)
            lower_triangular.append(lower_row)

        upper_matrix = Matrix(upper_triangular)
        lower_matrix = Matrix(lower_triangular)

        return upper_matrix, lower_matrix

    def inverse_matrix(self):
        # Compute the inverse matrix using Gaussian elimination
        identity = Matrix([[1 if i == j else 0 for j in range(len(self.matrix.rows))] for i in range(len(self.matrix.rows))])
        augmented_matrix = Matrix([self.matrix.rows[i] + identity.rows[i] for i in range(len(self.matrix.rows))])

        # Solve the system of linear equations for each column of the augmented matrix
        inverted_columns = []
        for j in range(len(self.matrix.rows)):
            column = [augmented_matrix.rows[i][j] for i in range(len(self.matrix.rows))]
            inverted_column = self.__solve_column(augmented_matrix, column)
            inverted_columns.append(inverted_column.elements)

        # Convert column lists into rows to form the inverse matrix
        inverted_rows = [[inverted_columns[i][j] for i in range(len(self.matrix.rows))] for j in range(len(self.matrix.rows))]
        inverted_matrix = Matrix(inverted_rows)

        return inverted_matrix

    def __solve_column(self, augmented_matrix, column):
        # Internal method to solve one column
        solver = LinearSystemSolver(augmented_matrix, Vector(column))
        return solver.gauss_elimination()
