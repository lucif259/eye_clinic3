import tkinter as tk
from tkinter import ttk, messagebox
from gui.add_patient_window import AddPatientWindow
from gui.edit_patient_window import EditPatientWindow
from gui.search_window import SearchWindow
from copy import deepcopy

class MainWindow:
    def __init__(self, master, patients):
        self.master = master
        self.master.title("Глазная клиника - Учет пациентов")

        # Храним исходные данные и текущие данные отдельно
        self.original_patients = deepcopy(patients)
        self.patients = deepcopy(patients)

        # Кнопки управления
        frame_buttons = tk.Frame(master)
        frame_buttons.pack(pady=5)

        self.add_button = tk.Button(frame_buttons, text="Добавить пациента", command=self.open_add_window)
        self.add_button.grid(row=0, column=0, padx=5)

        self.edit_button = tk.Button(frame_buttons, text="Редактировать", command=self.open_edit_window)
        self.edit_button.grid(row=0, column=1, padx=5)

        self.search_button = tk.Button(frame_buttons, text="Поиск", command=self.open_search_window)
        self.search_button.grid(row=0, column=2, padx=5)

        self.update_button = tk.Button(frame_buttons, text="Обновить список", command=self.reset_patients)
        self.update_button.grid(row=0, column=3, padx=5)

        # Таблица с пациентами
        columns = ("fio", "gender", "age", "address", "diagnosis")
        self.tree = ttk.Treeview(master, columns=columns, show="headings")
        self.tree.heading("fio", text="ФИО")
        self.tree.heading("gender", text="Пол")
        self.tree.heading("age", text="Возраст")
        self.tree.heading("address", text="Адрес")
        self.tree.heading("diagnosis", text="Диагноз")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.update_table()

        # Для отслеживания открытых окон
        self.add_window = None
        self.edit_window = None
        self.search_window = None

    def update_table(self):
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Заполнение таблицы данными
        for patient in self.patients:
            self.tree.insert("", "end", values=(
                patient['fio'],
                patient['gender'],
                patient['age'],
                patient['address'],
                patient['diagnosis']
            ))

    def open_add_window(self):
        if self.add_window is None or not self.add_window.winfo_exists():
            self.add_window = AddPatientWindow(self.master, self.patients, self.update_table).top
            self.add_window.protocol("WM_DELETE_WINDOW", self._on_close_add)

    def _on_close_add(self):
        self.add_window = None

    def open_edit_window(self):
        if self.edit_window is None or not self.edit_window.winfo_exists():
            selected = self.tree.selection()
            if not selected:
                messagebox.showinfo("Внимание", "Выберите пациента для редактирования")
                return
            patient_index = self.tree.index(selected[0])
            self.edit_window = EditPatientWindow(self.master, self.patients, patient_index, self.update_table).top
            self.edit_window.protocol("WM_DELETE_WINDOW", self._on_close_edit)

    def _on_close_edit(self):
        self.edit_window = None

    def open_search_window(self):
        if self.search_window is None or not self.search_window.winfo_exists():
            self.search_window = SearchWindow(self.master, self.patients, self.update_table).top
            self.search_window.protocol("WM_DELETE_WINDOW", self._on_close_search)

    def _on_close_search(self):
        self.search_window = None

    def reset_patients(self):
        # Возвращаем исходный список пациентов
        self.patients.clear()
        self.patients.extend(deepcopy(self.original_patients))
        self.update_table()