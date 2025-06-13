import tkinter as tk
from tkinter import messagebox

class SearchWindow:
    def __init__(self, master, patients, update_callback):
        self.top = tk.Toplevel(master)
        self.top.title("Поиск пациентов")
        self.patients = patients
        self.update_callback = update_callback

        self.search_criteria = tk.StringVar(value="fio")

        tk.Radiobutton(self.top, text="ФИО", variable=self.search_criteria, value="fio").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        tk.Radiobutton(self.top, text="Диагноз", variable=self.search_criteria, value="diagnosis").grid(row=1, column=0, sticky="w", padx=5, pady=5)

        tk.Label(self.top, text="Введите значение для поиска:").grid(row=2, column=0, padx=5, pady=5)
        self.search_entry = tk.Entry(self.top)
        self.search_entry.grid(row=2, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(self.top)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Найти", command=self.search).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Сбросить фильтр", command=self.reset_filter).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Отмена", command=self.on_close).pack(side=tk.LEFT, padx=5)

        self.top.protocol("WM_DELETE_WINDOW", self.on_close)
        self.original_patients = patients.copy()

    def search(self):
        criteria = self.search_criteria.get()
        value = self.search_entry.get().strip().lower()

        if not value:
            messagebox.showwarning("Внимание", "Введите значение для поиска")
            return

        if criteria == "fio":
            filtered = [p for p in self.original_patients if value in p['fio'].lower()]
        else:
            filtered = [p for p in self.original_patients if value in p['diagnosis'].lower()]

        if not filtered:
            messagebox.showinfo("Результат поиска", "Пациенты с такими параметрами не найдены.")
            return

        self.patients.clear()
        self.patients.extend(filtered)
        self.update_callback()
        self.on_close()

    def reset_filter(self):
        self.patients.clear()
        self.patients.extend(self.original_patients)
        self.update_callback()
        self.on_close()

    def on_close(self):
        self.top.destroy()