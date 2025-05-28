import tkinter as tk
from tkinter import messagebox, ttk


class EditPatientWindow:
    def __init__(self, master, patients, patient_id, update_callback):
        self.top = tk.Toplevel(master)
        self.top.title("Редактировать данные пациента")
        self.patients = patients
        self.patient_id = patient_id
        self.update_callback = update_callback

        self.patient = self.patients[self.patient_id]

        # Создаем и размещаем элементы формы
        tk.Label(self.top, text="ФИО:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.fio_entry = tk.Entry(self.top)
        self.fio_entry.grid(row=0, column=1, padx=5, pady=5)
        self.fio_entry.insert(0, self.patient['fio'])

        tk.Label(self.top, text="Пол:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.gender_var = tk.StringVar(value=self.patient['gender'])
        tk.Radiobutton(self.top, text="Мужской", variable=self.gender_var, value="Мужской").grid(row=1, column=1,
                                                                                                 sticky="w")
        tk.Radiobutton(self.top, text="Женский", variable=self.gender_var, value="Женский").grid(row=1, column=1,
                                                                                                 sticky="e")

        tk.Label(self.top, text="Возраст:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.age_spinbox = tk.Spinbox(self.top, from_=0, to=120)
        self.age_spinbox.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.age_spinbox.delete(0, tk.END)
        self.age_spinbox.insert(0, str(self.patient['age']))

        tk.Label(self.top, text="Адрес:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.address_entry = tk.Entry(self.top)
        self.address_entry.grid(row=3, column=1, padx=5, pady=5)
        self.address_entry.insert(0, self.patient['address'])

        tk.Label(self.top, text="Диагноз:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.diagnosis_combobox = ttk.Combobox(self.top,
                                               values=["Миопия", "Катаракта", "Глаукома", "Астигматизм", "Другое"])
        self.diagnosis_combobox.grid(row=4, column=1, padx=5, pady=5)
        self.diagnosis_combobox.set(self.patient['diagnosis'])

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

            # Обновляем данные пациента
            self.patient['fio'] = fio
            self.patient['gender'] = gender
            self.patient['age'] = int(age)
            self.patient['address'] = address
            self.patient['diagnosis'] = diagnosis

            self.update_callback()
            self.top.destroy()

            messagebox.showinfo("Успех", "Данные пациента успешно обновлены")

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))