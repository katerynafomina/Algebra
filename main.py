from tkinter import Tk
from linear_system_gui import LinearSystemGUI
from vector_matrix import Matrix, Vector
from solver import LinearSystemSolver


# Приклад використання
matrix = Matrix([
    [2, 1, 0, 0],
    [0, 3, 4, 0],
    [0, 0, 5, 6],
    [0, 0, 0, 7]
])
vector = Vector([1, 2, 3, 4])
solver= LinearSystemSolver(matrix, vector)
solutions = solver.gauss_elimination(matrix, vector)

print("Розв’язок СЛАР:", solutions)


def main():
    root = Tk()
    app = LinearSystemGUI(root)
    app.master.mainloop()


if __name__ == "__main__":
    main()
