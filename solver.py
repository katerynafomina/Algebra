from vector_matrix import Vector, Matrix, BandedMatrix
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
        for i in range(n):
            if matrix.rows[i][i] < sum(matrix.rows[i][j] for j in range(n) if j != i):
                raise ValueError("Matrix is not diagonally dominant")
            
        for i in range(n):
            if vector*matrix*vector<=0:
                raise ValueError("Matrix is not positive definite")

        while iterations < max_iterations:
            x_new = x[:]
            for i in range(n):
                sum_upper = sum(matrix.rows[i][j] * x_new[j] for j in range(i + 1, n))
                sum_lower = sum(matrix.rows[i][j] * x[j] for j in range(i))
                x_new[i] = (vector.elements[i] - sum_upper - sum_lower) / matrix.rows[i][i]
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
    def convert_to_banded(matrix, lower_bandwidth, upper_bandwidth):
        n = len(matrix)
        banded_rows = [[0] * n for _ in range(lower_bandwidth + upper_bandwidth + 1)]

        for i in range(n):
            for j in range(max(0, i - lower_bandwidth), min(n, i + upper_bandwidth + 1)):
                banded_rows[j - i + lower_bandwidth][i] = matrix[i][j]

        return BandedMatrix(lower_bandwidth, upper_bandwidth, banded_rows)

    @staticmethod
    def gauss_elimination_str(matrix, vector):
        # Determine the maximum lower and upper bandwidths
        lower_bandwidth = max(len([elem for elem in row[:i] if elem != 0]) for i, row in enumerate(matrix))
        upper_bandwidth = max(len([elem for elem in row[i + 1:] if elem != 0]) for i, row in enumerate(matrix))

        # Convert matrix to banded form
        banded_matrix = LinearSystemSolver.convert_to_banded(matrix, lower_bandwidth, upper_bandwidth)
        banded_matrix_res = LinearSystemSolver.convert_to_banded(matrix, lower_bandwidth, upper_bandwidth)
        print(banded_matrix)
        print(banded_matrix_res)
        n = banded_matrix.n

        # Forward elimination
        for i in range(n):
            # Find the maximum element in the column for pivoting
            max_row = i
            for k in range(i + 1, min(i + lower_bandwidth + 1, n)):
                if abs(banded_matrix[k, i]) > abs(banded_matrix[max_row, i]):
                    max_row = k

            # Swap rows if necessary so that the maximum element is on the diagonal
            if i != max_row:
                for m in range(-upper_bandwidth, lower_bandwidth + 1):
                    if i + m >= 0 and i + m < n:
                        banded_matrix[i + m, i], banded_matrix[i + m, max_row] = banded_matrix[i + m, max_row], \
                                                                                 banded_matrix[i + m, i]
                vector[i], vector[max_row] = vector[max_row], vector[i]

            # Find the pivot element
            pivot = banded_matrix[i, i]
            if pivot == 0:
                raise ValueError("Matrix does not have a unique solution")

            # Eliminate elements below the pivot
            for j in range(i + 1, min(i + lower_bandwidth + 1, n)):
                if banded_matrix[j, i] != 0:
                    factor = banded_matrix[j, i] / pivot
                    for k in range(i, min(i + upper_bandwidth + 1, n)):
                        banded_matrix[j, k] -= factor * banded_matrix[i, k]
                    vector[j] -= factor * vector[i]

        # Back substitution
        solutions = [0] * n
        for i in range(n - 1, -1, -1):
            solutions[i] = vector[i]
            for j in range(i + 1, min(i + upper_bandwidth + 1, n)):
                solutions[i] -= banded_matrix[i, j] * solutions[j]
            solutions[i] /= banded_matrix[i, i]

        return solutions, banded_matrix_res

    @staticmethod
    def find_path_length(matrix, i, j):
        """
        Знаходить довжину шляху від вершини i до вершини j у графі, що відповідає матриці системи лінійних алгебраїчних рівнянь.

        :param matrix: Матриця системи лінійних алгебраїчних рівнянь, яка представляє граф
        :param i: Початкова вершина шляху
        :param j: Кінцева вершина шляху
        :return: Довжина шляху від вершини i до вершини j або -1, якщо шлях не знайдено
        """
        # Ініціалізуємо чергу для обробки вершин
        queue = [(i, 0)]
        visited = set()  # Множина відвіданих вершин
        while queue:
            current_node, distance = queue.pop(0)
            if current_node == j:
                return distance  # Знайдено шлях, повертаємо його довжину
            visited.add(current_node)
            # Перевіряємо всі з'єднані вершини
            for neighbor, weight in enumerate(matrix[current_node]):
                if weight != 0 and neighbor not in visited:
                    queue.append((neighbor, distance + 1))
        return -1  # Шлях не знайдено

    @staticmethod
    def gibbs_algorithm(matrix, startVertex):
        def build_level_structure(matrix, start_vertex):
            levels = {start_vertex: 0}
            current_level = [start_vertex]
            next_level = []
            level = 1
            level_dict = {0: [start_vertex]}

            while current_level:
                for vertex in current_level:
                    for neighbor in matrix.neighbors(vertex):
                        if neighbor not in levels:
                            levels[neighbor] = level
                            next_level.append(neighbor)
                            if level not in level_dict:
                                level_dict[level] = []
                            level_dict[level].append(neighbor)
                current_level = next_level
                next_level = []
                level += 1

            # Повертаємо рівні у відсортованому порядку
            sorted_levels = {}
            for lvl in sorted(level_dict.keys()):
                for vertex in level_dict[lvl]:
                    sorted_levels[vertex] = lvl

            return sorted_levels

        def eccentricity(matrix, start_vertex):
            levels = build_level_structure(matrix, start_vertex)
            print(f"Рівні для вершини {start_vertex}: {levels}")
            return max(levels.values())

        # 1. Вибираємо стартову вершину (рекомендовано з малим степенем)
        start_vertex = startVertex
        print(f"Початкова стартова вершина: {start_vertex}")

        while True:
            # 2. Будуємо структуру рівнів для стартової вершини
            levels = build_level_structure(matrix, start_vertex)
            print(f"Рівні для стартової вершини {start_vertex}: {levels}")

            # Аналізуємо вершини найвищого рівня
            highest_level_vertices = [v for v, lvl in levels.items() if lvl == max(levels.values())]
            print(f"Вершини на найвищому рівні: {highest_level_vertices}")

            # Для кожної з них будуємо їхні структури рівнів
            max_eccentric_vertex = None
            max_eccentricity = -1
            for vertex in highest_level_vertices:
                vertex_eccentricity = eccentricity(matrix, vertex)
                print(f"Ексцентриситет для вершини {vertex}: {vertex_eccentricity}")
                if vertex_eccentricity > max_eccentricity:
                    max_eccentricity = vertex_eccentricity
                    max_eccentric_vertex = vertex

            # 3. Порівнюємо ексцентриситети вибраної та стартової вершин
            start_eccentricity = eccentricity(matrix, start_vertex)
            print(f"Ексцентриситет для стартової вершини {start_vertex}: {start_eccentricity}")

            if start_eccentricity == max_eccentricity:
                print(f"Знайдена псевдопериферійна вершина: {start_vertex}")
                return start_vertex  # Псевдопериферійна вершина знайдена
            else:
                # Перевіряємо, чи є вершина з максимальним ексцентриситом
                # серед вершин найвищого рівня, відмінною від поточної стартової вершини
                if start_vertex != max_eccentric_vertex:
                    print(f"Змінюємо стартову вершину з {start_vertex} на {max_eccentric_vertex}")
                    start_vertex = max_eccentric_vertex  # Приймаємо нову вершину за стартову
                else:
                    # Якщо такої вершини немає, це означає, що поточна вершина - псевдопериферійна
                    print(f"Знайдена псевдопериферійна вершина: {start_vertex}")
                    return start_vertex

    @staticmethod
    def cuthill_mckee(matrix, startVertex):
        n = len(matrix.rows)
        visited = [False] * n
        permutation = []

        start_vertex = LinearSystemSolver.gibbs_algorithm(matrix, startVertex)
        permutation.append(start_vertex)
        visited[start_vertex] = True

        queue = [start_vertex]

        while queue:
            current_vertex = queue.pop(0)
            neighbors = [v for v in matrix.neighbors(current_vertex) if not visited[v]]
            neighbors.sort(key=lambda x: matrix.degree(x))

            for neighbor in neighbors:
                if not visited[neighbor]:
                    permutation.append(neighbor)
                    visited[neighbor] = True
                    queue.append(neighbor)

        # Додаємо невідвідані вершини
        for i in range(n):
            if not visited[i]:
                permutation.append(i)
                visited[i] = True

        matrix.reorder(permutation)
        return matrix, permutation