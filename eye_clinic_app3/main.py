import tkinter as tk
from database.db import Database
from gui.main_window import MainWindow

def main():
    # Инициализация базы данных
    db = Database()
    
    # Создание и запуск GUI
    root = tk.Tk()
    app = MainWindow(root, db)
    root.mainloop()

if __name__ == "__main__":
    main()