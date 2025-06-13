import tkinter as tk
from tkinter import ttk, messagebox
from gui.add_patient_window import AddPatientWindow
from gui.edit_patient_window import EditPatientWindow
from gui.search_window import SearchWindow

class MainWindow:
    def __init__(self, master, db):
        self.master = master
        self.db = db
        self.master.title("Глазная клиника - Учет пациентов")

        # Кнопки управления
        self.setup_buttons()
        
        # Таблица с пациентами
        self.setup_table()
        
        # Первоначальная загрузка данных
        self.update_table()

    def setup_buttons(self):
        frame_buttons = tk.Frame(self.master)
        frame_buttons.pack(pady=5)

        tk.Button(frame_buttons, text="Добавить", command=self.open_add_window).grid(row=0, column=0, padx=5)
        tk.Button(frame_buttons, text="Редактировать", command=self.open_edit_window).grid(row=0, column=1, padx=5)
        tk.Button(frame_buttons, text="Поиск", command=self.open_search_window).grid(row=0, column=2, padx=5)
        tk.Button(frame_buttons, text="Обновить", command=self.update_table).grid(row=0, column=3, padx=5)

    def setup_table(self):
        columns = ("fio", "gender", "age", "address", "diagnosis")
        self.tree = ttk.Treeview(self.master, columns=columns, show="headings")
        
        self.tree.heading("fio", text="ФИО")
        self.tree.heading("gender", text="Пол")
        self.tree.heading("age", text="Возраст")
        self.tree.heading("address", text="Адрес")
        self.tree.heading("diagnosis", text="Диагноз")
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def update_table(self):
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Загрузка данных из БД
        patients = self.db.get_all_patients()
        for patient in patients:
            self.tree.insert("", "end", values=(
                patient['fio'],
                patient['gender'],
                patient['age'],
                patient['address'],
                patient['diagnosis']
            ))

    def open_add_window(self):
        AddPatientWindow(self.master, self.db, self.update_table)

    def open_edit_window(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Внимание", "Выберите пациента для редактирования")
            return
        patient_id = self.tree.index(selected[0]) + 1  # ID начинаются с 1
        EditPatientWindow(self.master, self.db, patient_id, self.update_table)

    def open_search_window(self):
        SearchWindow(self.master, self.db, self.update_table)