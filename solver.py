from vector_matrix import Vector, Matrix
class LinearSystemSolver:
    def __init__(self, matrix, vector):
        self.matrix = matrix
        self.vector = vector
        # self.upper_triangular = None
        # self.lower_triangular = None

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


        lower_triangular = [[0] * n for _ in range(n)]

        for i in range(n):
            #  Ініціалізація діагонального елементу нижньотрикутної матриці
            lower_triangular[i][i] = 1.0

            # Вибір головного елементу та перестановка рядків
            max_index = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_index][i]):
                    max_index = j

            A[i], A[max_index] = A[max_index], A[i]
            b[i], b[max_index] = b[max_index], b[i]

            # Елімінація елементів під діагональним  елементом
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]

        decomp_matrix = A

        x = [0] * n
        for i in range(n - 1, -1, -1):
            #  Обернена підстановка для знаходження розв'язку
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

    @staticmethod
    def seidel_method(matrix, vector, tolerance=1e-6, max_iterations=10000):
        n = len(matrix.rows)
        x = [0] * n  # Initial guess
        iterations = 0

        while iterations < max_iterations:
            x_new = x[:]
            for i in range(n):
                sum_ax = sum(matrix.rows[i][j] * x_new[j] for j in range(n) if j != i)
                x_new[i] = (vector.elements[i] - sum_ax) / matrix.rows[i][i]

            # Calculate the residual norm
            residual = matrix * Vector(x_new) - vector
            norm_residual = residual.max_norm()

            if norm_residual < tolerance:
                return Vector(x_new), iterations + 1

            x = x_new
            iterations += 1

        # If we reached max_iterations without converging, raise an error or return a status indicating failure
        raise ValueError("Seidel method did not converge within the maximum number of iterations")

    @staticmethod
    def gauss_elimination(matrix, vector):
        n = len(matrix)

        # Прямий хід
        for i in range(n):
            # Знаходимо головний елемент рядка
            pivot = matrix[i][i]
            if pivot == 0:
                raise ValueError("Матриця не має унікального розв’язку")

            # Проходимо по усіх рядках нижче поточного
            for j in range(i + 1, n):
                # Якщо елемент не нульовий, виконуємо операції над стрічками
                if matrix[j][i] != 0:
                    factor = matrix[j][i] / pivot
                    for k in range(i, n):
                        matrix[j][k] -= factor * matrix[i][k]
                    vector[j] -= factor * vector[i]

        # Зворотний хід (обернена підстановка)
        solutions = [0] * n
        for i in range(n - 1, -1, -1):
            solutions[i] = vector[i]
            for j in range(i + 1, n):
                solutions[i] -= matrix[i][j] * solutions[j]
            solutions[i] /= matrix[i][i]

        return solutions


