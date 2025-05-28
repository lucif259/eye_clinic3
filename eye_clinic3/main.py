import tkinter as tk
from data.patients_data import patients
from gui.main_window import MainWindow

def main():
    root = tk.Tk()
    app = MainWindow(root, patients)
    root.mainloop()

if __name__ == "__main__":
    main()