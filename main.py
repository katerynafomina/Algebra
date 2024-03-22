from tkinter import Tk
from linear_system_gui import LinearSystemGUI
from solver import LinearSystemSolver
from vector_matrix import *

def main():
    root = Tk()
    app = LinearSystemGUI(root)
    app.master.mainloop()


if __name__ == "__main__":
    main()
