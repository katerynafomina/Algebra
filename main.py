from tkinter import Tk
from linear_system_gui import LinearSystemGUI
from solver import LinearSystemSolver

def main():
    # root = Tk()
    # app = LinearSystemGUI(root)
    # app.master.mainloop()

    solver = LinearSystemSolver.from_file("matrix1.txt")
    print("Original matrix:")
    print(solver.matrix)
    print("Original vector:")
    print(solver.vector)

# Приклад використання:
# solver = LinearSystemSolver()
# matrix = Matrix([[2, 1, -1], [2, 3, 0], [9, -1, 5]])
    # vector = Vector([1, 2, 3])
    solution, upper_triangular_matrix = solver.gaussian_elimination(solver.matrix, solver.vector)
    print("Solution:", solution)
    print("Upper triangular matrix:")
    print('\n'.join([' '.join(map(str, row)) for row in upper_triangular_matrix.rows]))
    # solution, matrix, m= solver.gauss_elimination()
    # print("Solution:")
    # print(solution)  # Округлити до двох знаків після коми
    # print("Upper triangular matrix:")
    # print(matrix)
    # print("Upper triangular matrix:")
    # print(m)

    # inverse = solver.inverse_matrix()
    # print("Inverse matrix:")
    # print(inverse.round(2))  # Округлити до двох знаків після коми


if __name__ == "__main__":
    main()
