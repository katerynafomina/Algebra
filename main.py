from tkinter import Tk
from linear_system_gui import LinearSystemGUI
from solver import LinearSystemSolver
from vector_matrix import *

def main():

    # root = Tk()
    # app = LinearSystemGUI(root)
    # app.master.mainloop()

    solver = LinearSystemSolver.from_file("matrix1.txt")
    print("Original matrix:")
    print(solver.matrix)
    print("Original vector:")
    print(solver.vector)

    solution, upper_triangular_matrix = solver.gaussian_elimination(solver.matrix, solver.vector)
    solution_rounded = Vector([round(x, 2) for x in solution.elements])
    upper_triangular_matrix_rounded = Matrix([[round(x, 2) for x in row] for row in upper_triangular_matrix.rows])
    inverse_matrix_obj = solver.inverse_matrix(solver.matrix)

    print("Solution:", solution_rounded)
    print("Upper triangular matrix:")
    print('\n'.join([' '.join(map(str, row)) for row in upper_triangular_matrix_rounded.rows]))
    print("Inverse matrix:")
    print(inverse_matrix_obj)



if __name__ == "__main__":
    main()
