import tkinter as tk
from tkinter import filedialog, messagebox
from functools import partial

class LinearSystemSolver:
    def __init__(self, matrix, vector):
        self.matrix = matrix
        self.vector = vector

    # def solve(self):
    #     # Gaussian elimination with partial pivoting
    #     n = len(self.matrix.rows)
    #     augmented_matrix = Matrix([self.matrix.rows[i] + [self.vector.elements[i]] for i in range(n)])
    #
    #     for i in range(n):
    #         # Partial pivoting
    #         max_row = max(range(i, n), key=lambda x: abs(augmented_matrix.rows[x][i]))
    #         augmented_matrix.rows[i], augmented_matrix.rows[max_row] = augmented_matrix.rows[max_row], augmented_matrix.rows[i]
    #
    #         # Elimination
    #         for j in range(i + 1, n):
    #             factor = augmented_matrix.rows[j][i] / augmented_matrix.rows[i][i]
    #             for k in range(i, n + 1):
    #                 augmented_matrix.rows[j][k] -= factor * augmented_matrix.rows[i][k]
    #
    #     # Back substitution
    #     solution = [0] * n
    #     for i in range(n - 1, -1, -1):
    #         solution[i] = augmented_matrix.rows[i][n]
    #         for j in range(i + 1, n):
    #             solution[i] -= augmented_matrix.rows[i][j] * solution[j]
    #         solution[i] /= augmented_matrix.rows[i][i]
    #
    #     return Vector(solution)

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

class Vector:
    def __init__(self, elements):
        self.elements = elements

    def __add__(self, other):
        if isinstance(other, Vector) and len(self.elements) == len(other.elements):
            return Vector([x + y for x, y in zip(self.elements, other.elements)])
        raise ValueError("Vectors must be of the same length")

    def __sub__(self, other):
        if isinstance(other, Vector) and len(self.elements) == len(other.elements):
            return Vector([x - y for x, y in zip(self.elements, other.elements)])
        raise ValueError("Vectors must be of the same length")

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector([x * other for x in self.elements])
        raise ValueError("Multiplication is only supported with scalar")

    def euclidean_norm(self):
        return sum(x**2 for x in self.elements) ** 0.5

    def max_norm(self):
        return max(abs(x) for x in self.elements)


class Matrix:
    def __init__(self, rows):
        self.rows = rows

    def __add__(self, other):
        if isinstance(other, Matrix) and len(self.rows) == len(other.rows) and len(self.rows[0]) == len(other.rows[0]):
            return Matrix([[x + y for x, y in zip(row1, row2)] for row1, row2 in zip(self.rows, other.rows)])
        raise ValueError("Matrices must have the same dimensions")

    def __sub__(self, other):
        if isinstance(other, Matrix) and len(self.rows) == len(other.rows) and len(self.rows[0]) == len(other.rows[0]):
            return Matrix([[x - y for x, y in zip(row1, row2)] for row1, row2 in zip(self.rows, other.rows)])
        raise ValueError("Matrices must have the same dimensions")

    def __mul__(self, other):
        if isinstance(other, Matrix) and len(self.rows[0]) == len(other.rows):
            return Matrix([[sum(a * b for a, b in zip(row1, col)) for col in zip(*other.rows)] for row1 in self.rows])
        elif isinstance(other, Vector) and len(self.rows[0]) == len(other.elements):
            return Vector([sum(a * b for a, b in zip(row, other.elements)) for row in self.rows])
        raise ValueError("Invalid multiplication")

    def euclidean_norm(self):
        return max(row.euclidean_norm() for row in self.rows)

    def max_norm(self):
        return max(row.max_norm() for row in self.rows)


class LinearSystemGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Linear System Solver")

        self.matrix_entries = []
        self.vector_entries = []

        self.create_input_widgets()

        self.load_button = tk.Button(self.master, text="Load Data", command=self.load_data)
        self.load_button.pack(pady=10)

        self.buttons_frame = tk.Frame(self.master)
        self.buttons_frame.pack()

        self.add_button = tk.Button(self.buttons_frame, text="Add", command=self.open_operand_window_add)
        self.add_button.grid(row=0, column=0, padx=5, pady=5)

        self.subtract_button = tk.Button(self.buttons_frame, text="Subtract", command=self.open_operand_window_subtract)
        self.subtract_button.grid(row=0, column=1, padx=5, pady=5)

        self.multiply_button = tk.Button(self.buttons_frame, text="Multiply", command=self.open_operand_window_multiply)
        self.multiply_button.grid(row=0, column=2, padx=5, pady=5)

        self.norm_button = tk.Button(self.buttons_frame, text="Norm", command=self.open_operand_window_norm)
        self.norm_button.grid(row=0, column=3, padx=5, pady=5)

        self.vector_or_matrix_var = tk.StringVar()
        self.vector_or_matrix_var.set("Vector")

        self.vector_or_matrix_menu = tk.OptionMenu(self.buttons_frame, self.vector_or_matrix_var, "Vector", "Matrix")
        self.vector_or_matrix_menu.grid(row=1, column=0, padx=5, pady=5)

        self.operation_var = tk.StringVar()
        self.operation_var.set("Add")

        self.operation_menu = tk.OptionMenu(self.buttons_frame, self.operation_var, "Add", "Subtract", "Multiply", "Norm")
        self.operation_menu.grid(row=1, column=1, padx=5, pady=5)

        self.result_label = tk.Label(self.master, text="")
        self.result_label.pack(pady=10)

    def open_operand_window_add(self):
        self.open_operand_window("Add")

    def open_operand_window_subtract(self):
        self.open_operand_window("Subtract")

    def open_operand_window_multiply(self):
        self.open_operand_window("Multiply")

    def open_operand_window_norm(self):
        self.open_operand_window("Norm")

    def create_input_widgets(self):
        matrix_frame = tk.Frame(self.master)
        matrix_frame.pack()

        vector_frame = tk.Frame(self.master)
        vector_frame.pack()

        for i in range(3):  # Adjust this number according to the size of the matrix and vector
            row_entries = []
            for j in range(3):  # Adjust this number according to the size of the matrix
                entry = tk.Entry(matrix_frame, width=8)
                entry.grid(row=i, column=j, padx=5, pady=5)
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)

            entry = tk.Entry(vector_frame, width=8)
            entry.grid(row=i, column=0, padx=5, pady=5)
            self.vector_entries.append(entry)

    def open_operand_window(self, operation):
        operand_window = tk.Toplevel(self.master)
        operand_window.title(operation + " Operands")

        label1 = tk.Label(operand_window, text="First Operand:")
        label1.grid(row=0, column=0, padx=5, pady=5)

        operand1_frame = tk.Frame(operand_window)
        operand1_frame.grid(row=0, column=1, padx=5, pady=5)

        label2 = tk.Label(operand_window, text="Second Operand:")
        label2.grid(row=1, column=0, padx=5, pady=5)

        operand2_frame = tk.Frame(operand_window)
        operand2_frame.grid(row=1, column=1, padx=5, pady=5)

        # Use grid() for all widgets inside operand1_frame
        operand1_label = tk.Label(operand1_frame,
                                  text="Vector:" if self.vector_or_matrix_var.get() == "Vector" else "Matrix:")
        operand1_label.grid()

        if self.vector_or_matrix_var.get() == "Vector":
            operand1_entries = []
            for i in range(len(self.vector_entries)):
                entry = tk.Entry(operand1_frame, width=8)
                entry.grid(row=0, column=i, padx=5, pady=5)
                entry.insert(0, self.vector_entries[i].get())
                operand1_entries.append(entry)
        else:
            operand1_entries = []
            for i in range(len(self.matrix_entries)):
                row_entries = []
                for j in range(len(self.matrix_entries[0])):
                    entry = tk.Entry(operand1_frame, width=8)
                    entry.grid(row=i, column=j, padx=5, pady=5)
                    entry.insert(0, self.matrix_entries[i][j].get())
                    row_entries.append(entry)
                operand1_entries.append(row_entries)

        operand2_label = tk.Label(operand2_frame, text="Enter manually:")
        operand2_label.grid()

        operand2_entries = []
        if self.vector_or_matrix_var.get() == "Vector":
            for i in range(len(self.vector_entries)):
                entry = tk.Entry(operand2_frame, width=8)
                entry.grid(row=0, column=i, padx=5, pady=5)
                operand2_entries.append(entry)
        else:
            operand2_entries = []
            for i in range(3):  # You need to adjust these values according to the size of the matrix
                row_entries = []
                for j in range(3):  # You need to adjust these values according to the size of the matrix
                    entry = tk.Entry(operand2_frame, width=8)
                    entry.grid(row=i, column=j, padx=5, pady=5)
                    row_entries.append(entry)
                operand2_entries.append(row_entries)

        result_button = tk.Button(operand_window, text="Result",
                                  command=lambda: self.perform_operation_with_operands(operation, operand1_entries,
                                                                                       operand2_entries))
        result_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        operand_window.mainloop()

    def perform_operation_with_operands(self, operation, operand1_entries, operand2_entries):
        try:
            if self.vector_or_matrix_var.get() == "Vector":
                operand1 = Vector([float(entry.get()) for entry in operand1_entries])
                operand2 = Vector([float(entry.get()) for entry in operand2_entries])
            else:
                operand1 = Matrix([[float(entry.get()) for entry in row] for row in operand1_entries])
                operand2 = Matrix([[float(entry.get()) for entry in row] for row in operand2_entries])

            if operation == "Add":
                result = operand1 + operand2
            elif operation == "Subtract":
                result = operand1 - operand2
            elif operation == "Multiply":
                result = operand1 * operand2
            elif operation == "Norm":
                norm_type = self.get_norm_type()
                if norm_type == "Euclidean":
                    result = operand1.euclidean_norm() if isinstance(operand1, Vector) else operand1.euclidean_norm()
                else:
                    result = operand1.max_norm() if isinstance(operand1, Vector) else operand1.max_norm()

            self.result_label.config(text=f"Result: {result.elements}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def load_data(self):
        # filename = filedialog.askopenfilename(initialdir="/", title="Select File",
        #                                       filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        filename = ".\matrix1.txt"
        if filename:
            try:
                solver = LinearSystemSolver.from_file(filename)
                matrix_data = solver.matrix.rows
                vector_data = solver.vector.elements

                # Populate matrix entries
                for i, row in enumerate(matrix_data):
                    for j, value in enumerate(row):
                        self.matrix_entries[i][j].delete(0, tk.END)
                        self.matrix_entries[i][j].insert(0, value)

                # Populate vector entries
                for i, value in enumerate(vector_data):
                    self.vector_entries[i].delete(0, tk.END)
                    self.vector_entries[i].insert(0, value)

                messagebox.showinfo("Success", "Data loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while loading data: {str(e)}")


def main():
    root = tk.Tk()
    app = LinearSystemGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
