import tkinter as tk
from tkinter import messagebox


class AddPatientWindow:
    def __init__(self, master, patients_list, update_callback):
        self.top = tk.Toplevel(master)
        self.top.title("Добавить пациента")
        self.patients_list = patients_list
        self.update_callback = update_callback

        # Создаем и размещаем элементы формы
        tk.Label(self.top, text="ФИО:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.fio_entry = tk.Entry(self.top)
        self.fio_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.top, text="Пол:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.gender_var = tk.StringVar(value="Мужской")
        tk.Radiobutton(self.top, text="Мужской", variable=self.gender_var, value="Мужской").grid(row=1, column=1,
                                                                                                 sticky="w")
        tk.Radiobutton(self.top, text="Женский", variable=self.gender_var, value="Женский").grid(row=1, column=1,
                                                                                                 sticky="e")

        tk.Label(self.top, text="Возраст:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.age_spinbox = tk.Spinbox(self.top, from_=0, to=120)
        self.age_spinbox.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.top, text="Адрес:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.address_entry = tk.Entry(self.top)
        self.address_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.top, text="Диагноз:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.diagnosis_combobox = tk.ttk.Combobox(self.top,
                                                  values=["Миопия", "Катаракта", "Глаукома", "Астигматизм", "Другое"])
        self.diagnosis_combobox.grid(row=4, column=1, padx=5, pady=5)
        self.diagnosis_combobox.set("Миопия")

        # Кнопки управления
        btn_frame = tk.Frame(self.top)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Сохранить", command=self.save_patient).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Отмена", command=self.top.destroy).pack(side=tk.LEFT, padx=5)

    def save_patient(self):
        try:
            # Получаем данные из формы
            fio = self.fio_entry.get().strip()
            gender = self.gender_var.get()
            age = self.age_spinbox.get()
            address = self.address_entry.get().strip()
            diagnosis = self.diagnosis_combobox.get().strip()

            # Валидация данных
            if not all([fio, gender, age, address, diagnosis]):
                raise ValueError("Все поля должны быть заполнены")

            if not age.isdigit() or int(age) < 0 or int(age) > 120:
                raise ValueError("Возраст должен быть числом от 0 до 120")

            # Создаем нового пациента
            new_patient = {
                'fio': fio,
                'gender': gender,
                'age': int(age),
                'address': address,
                'diagnosis': diagnosis
            }

            # Используем метод add_patient из Database вместо append
            self.patients_list.add_patient(new_patient)
            self.update_callback()
            self.top.destroy()

            messagebox.showinfo("Успех", "Пациент успешно добавлен")

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))