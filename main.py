from tkinter import Tk
from linear_system_gui import LinearSystemGUI
from vector_matrix import Matrix, Vector
from solver import LinearSystemSolver

def test_find_path_length():
    # Визначення матриці суміжності для графа
    matrix_data = [
        [0, 1, 0, 0, 0],
        [1, 0, 1, 1, 0],
        [0, 1, 0, 1, 1],
        [0, 1, 1, 0, 1],
        [0, 0, 1, 1, 0]
    ]

    # Створення об'єкту Matrix на основі матриці суміжності
    adjacency_matrix = Matrix(matrix_data)

    # Тестові випадки
    tests = [
        (0, 2, 2),  # Існує шлях довжиною 2 від вершини 0 до вершини 2
        (0, 4, 3),  # Існує шлях довжиною 3 від вершини 0 до вершини 4
        (3, 4, 1),  # Існує шлях довжиною 1 від вершини 3 до вершини 4
        (0, 0, 0),  # Шлях від вершини до самої себе має довжину 0
        (0, 5, -1)  # Вершини 5 не існує, отже шлях не знайдено
    ]

    # Запуск тестів
    for i, j, expected_length in tests:
        result = LinearSystemSolver.find_path_length(adjacency_matrix, i, j)
        assert result == expected_length, f"Test failed for {i} -> {j}: expected {expected_length}, got {result}"
        print(f"Test passed for {i} -> {j}: {result}")


# Виконання тестів
test_find_path_length()

# Приклад використання алгоритму Гібса
# рядки - вершини графа, стовпці - сусіди вершини
matrix_data = [
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
    [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
    [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1],
    [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1]
]

adjacency_matrix = Matrix(matrix_data)
pseudoperipheral_vertex = LinearSystemSolver.gibbs_algorithm(adjacency_matrix, 9)
print(f"Pseudoperipheral vertex: {pseudoperipheral_vertex}")

new_matrix, permutation = LinearSystemSolver.cuthill_mckee(adjacency_matrix, 4)
print("New Matrix:")
print(new_matrix)



print("Permutation:", permutation)


def main():
    root = Tk()
    app = LinearSystemGUI(root)
    app.master.mainloop()


if __name__ == "__main__":
    main()
