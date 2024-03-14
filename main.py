from tkinter import Tk
from linear_system_gui import LinearSystemGUI
from solver import LinearSystemSolver

def main():
    root = Tk()
    app = LinearSystemGUI(root)
    app.master.mainloop()

    # Після закриття вікна програми:
    solver = LinearSystemSolver.from_file("matrix1.txt")
    print("Original matrix:")
    print(solver.matrix)
    print("Original vector:")
    print(solver.vector)

    solution = solver.gauss_elimination()
    print("Solution:")
    print(solution)

    upper, lower = solver.decompose_matrix()
    print("Upper triangular matrix:")
    print(upper)
    print("Lower triangular matrix:")
    print(lower)

    inverse = solver.inverse_matrix()
    print("Inverse matrix:")
    print(inverse)


if __name__ == "__main__":
    main()
