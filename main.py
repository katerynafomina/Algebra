from tkinter import Tk
from linear_system_gui import LinearSystemGUI

def main():
    root = Tk()
    app = LinearSystemGUI(root)
    app.master.mainloop()

if __name__ == "__main__":
    main()
