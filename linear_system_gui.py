from typing import List
from vector_matrix import Vector, Matrix
import tkinter as tk
from tkinter import filedialog, messagebox
from solver import LinearSystemSolver

class LinearSystemGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Linear System Solver")

        self.matrix_entries = []
        self.vector_entries = []
        self.matrix_rows = 0
        self.matrix_columns = 0
        self.vector_len = 0

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

        self.vector_or_matrix_var1 = tk.StringVar()
        self.vector_or_matrix_var1.set("Vector")

        self.vector_or_matrix_operand1 = tk.OptionMenu(self.buttons_frame, self.vector_or_matrix_var1, "Vector", "Matrix")
        self.vector_or_matrix_operand1.grid(row=1, column=1, padx=5, pady=5)

        self.operation_var = tk.StringVar()
        self.operation_var.set("Vector")

        self.vector_or_matrix_var2 = tk.StringVar()
        self.vector_or_matrix_var2.set("Vector")

        self.vector_or_matrix_operand2 = tk.OptionMenu(self.buttons_frame, self.vector_or_matrix_var2, "Vector",
                                                       "Matrix")
        self.vector_or_matrix_operand2.grid(row=1, column=2, padx=5, pady=5)

        self.get_norm_type = tk.StringVar()
        self.get_norm_type.set("Module")
        self.get_norm_type_operand = tk.OptionMenu(self.buttons_frame, self.get_norm_type, "Module", "Euclidean")
        self.get_norm_type_operand.grid(row=1, column=3, padx=5, pady=5)

        self.gaussian_button = tk.Button(self.buttons_frame, text="Gaussian Method", command=self.display_gaussian_results)
        self.gaussian_button.grid(row=0, column=4, padx=5, pady=5)

        self.checkResult = tk.Button(self.buttons_frame, text="check results", command=self.check_results)
        self.checkResult.grid(row=1, column=4, padx=5, pady=5)


        self.result_label = tk.Label(self.master, text="")
        self.result_label.pack(pady=10)

    def check_results(self):
        try:
            solver = LinearSystemSolver.from_file(".\matrix1.txt")
            solution, upper_triangular_matrix = solver.gaussian_elimination(solver.matrix, solver.vector)
            solution_rounded = Vector([round(x, 2) for x in solution.elements])
            upper_triangular_matrix_rounded = Matrix(
                [[round(x, 2) for x in row] for row in upper_triangular_matrix.rows])
            result = solver.matrix*solution - solver.vector
            print(result)
            print(result.max_norm)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            print(e)




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

        for i in range(self.matrix_rows):
            row_entries = []
            for j in range(self.matrix_columns):
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
                                  text="Vector:" if self.vector_or_matrix_var2.get() == "Vector" else "Matrix:")
        operand1_label.grid()

        if self.vector_or_matrix_var1.get() == "Vector":
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

        operand2_label = tk.Label(operand2_frame, text="")
        operand2_label.grid()

        operand2_entries = []
        if self.vector_or_matrix_var2.get() == "Vector":
            for i in range(len(self.vector_entries)):
                entry = tk.Entry(operand2_frame, width=8)
                entry.grid(row=0, column=i, padx=5, pady=5)
                operand2_entries.append(entry)
        else:
            operand2_entries = []
            for i in range(self.matrix_rows):
                row_entries = []
                for j in range(self.matrix_columns):
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
            if self.vector_or_matrix_var1.get() == "Vector" and self.vector_or_matrix_var2.get() == "Vector":
                operand1 = Vector([float(entry.get()) for entry in operand1_entries])
                operand2 = Vector([float(entry.get()) for entry in operand2_entries])
            elif self.vector_or_matrix_var1.get() == "Vector" and self.vector_or_matrix_var2.get() == "Matrix":
                operand1 = Vector([float(entry.get()) for entry in operand1_entries])
                operand2 = Matrix([[float(entry.get()) for entry in row] for row in operand2_entries])
            elif self.vector_or_matrix_var1.get() == "Matrix" and self.vector_or_matrix_var2.get() == "Vector":
                operand1 = Matrix([[float(entry.get()) for entry in row] for row in operand1_entries])
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
                norm_type = self.get_norm_type.get()
                if norm_type == "Euclidean":
                    result = operand1.euclidean_norm()
                else:
                    result = operand1.max_norm()

            # Check the type of result and format it accordingly
            if isinstance(result, (int, float)):
                self.result_label.config(text=f"Result: {result}")
            elif isinstance(result, Vector) or isinstance(result, Matrix):
                self.result_label.config(text=f"Result: {result}")
            else:
                raise ValueError("Invalid result type")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            print(e)

    # filename = filedialog.askopenfilename(initialdir="/", title="Select File",
    #
    def load_data(self):
        filename = ".\matrix1.txt"
        if filename:
            try:
                solver = LinearSystemSolver.from_file(filename)
                matrix_data = solver.matrix.rows
                vector_data = solver.vector.elements

                # Convert data to floats
                matrix_data = [[float(value) for value in row] for row in matrix_data]
                vector_data = [float(value) for value in vector_data]

                # Update matrix dimensions
                self.matrix_rows = len(matrix_data)
                self.matrix_columns = len(matrix_data[0])

                # Ensure that matrix_entries is not empty
                if not self.matrix_entries:
                    self.create_input_widgets()

                # Populate matrix entries
                for i, row in enumerate(matrix_data):
                    for j, value in enumerate(row):
                        self.matrix_entries[i][j].delete(0, tk.END)
                        self.matrix_entries[i][j].insert(0, value)

                # Populate vector entries
                for i, value in enumerate(vector_data):
                    self.vector_entries[i].delete(0, tk.END)
                    self.vector_entries[i].insert(0, value)

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while loading data: {str(e)}")
                print(e)

    def display_gaussian_elimination_results(self, matrix, vector):
        try:
            solution, upper_triangular_matrix = LinearSystemSolver.gaussian_elimination(matrix, vector)
            solution_rounded = Vector([round(x, 2) for x in solution.elements])
            upper_triangular_matrix_rounded = Matrix([[round(x, 2) for x in row] for row in upper_triangular_matrix.rows])

            result_window = tk.Toplevel(self.master)
            result_window.title("Gaussian Elimination Results")

            solution_label = tk.Label(result_window, text=f"Solution: {solution_rounded}")
            solution_label.pack(pady=5)

            upper_triangular_label = tk.Label(result_window, text="Upper Triangular Matrix:")
            upper_triangular_label.pack(pady=5)

            upper_triangular_text = tk.Text(result_window, height=len(upper_triangular_matrix.rows), width=len(upper_triangular_matrix.rows[0]) * 8)
            upper_triangular_text.pack(pady=5)
            for row in upper_triangular_matrix_rounded.rows:
                upper_triangular_text.insert(tk.END, ' '.join(map(str, row)) + '\n')

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while performing Gaussian elimination: {str(e)}")
            print(e)

    def display_inverse_matrix(self, matrix):
        try:
            inverse_matrix_obj = LinearSystemSolver.inverse_matrix(matrix)

            result_window = tk.Toplevel(self.master)
            result_window.title("Inverse Matrix")

            inverse_matrix_label = tk.Label(result_window, text="Inverse Matrix:")
            inverse_matrix_label.pack(pady=5)

            inverse_matrix_text = tk.Text(result_window, height=len(inverse_matrix_obj.rows), width=len(inverse_matrix_obj.rows[0]) * 8)
            inverse_matrix_text.pack(pady=5)
            for row in inverse_matrix_obj.rows:
                inverse_matrix_text.insert(tk.END, ' '.join(map(str, row)) + '\n')

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while calculating the inverse matrix: {str(e)}")
            print(e)

    def display_gaussian_results(self):
        try:
            solver = LinearSystemSolver.from_file(".\matrix1.txt")
            solution, upper_triangular_matrix = solver.gaussian_elimination(solver.matrix, solver.vector)
            solution_rounded = Vector([round(x, 2) for x in solution.elements])
            upper_triangular_matrix_rounded = Matrix([[round(x, 2) for x in row] for row in upper_triangular_matrix.rows])

            result_window = tk.Toplevel(self.master)
            result_window.title("Gaussian Elimination Results")

            solution_label = tk.Label(result_window, text=f"Solution: {solution_rounded}")
            solution_label.pack(pady=5)

            upper_triangular_label = tk.Label(result_window, text="Upper Triangular Matrix:")
            upper_triangular_label.pack(pady=5)

            upper_triangular_text = tk.Text(result_window, height=len(upper_triangular_matrix.rows), width=len(upper_triangular_matrix.rows[0]) * 8)
            upper_triangular_text.pack(pady=5)
            for row in upper_triangular_matrix_rounded.rows:
                upper_triangular_text.insert(tk.END, ' '.join(map(str, row)) + '\n')

            inverse_matrix_button = tk.Button(result_window, text="Inverse Matrix", command=lambda: self.display_inverse_matrix(solver.matrix))
            inverse_matrix_button.pack(pady=5)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while performing Gaussian elimination: {str(e)}")
            print(e)

