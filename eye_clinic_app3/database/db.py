import mysql.connector
from mysql.connector import Error
import os

class Database:
    def __init__(self):
        self.connection = self.connect()  # Инициализация подключения
    
    def connect(self):
        """Метод для установки соединения с MySQL"""
        try:
            return mysql.connector.connect(
                host='127.0.0.1',  # Используем IP вместо localhost
                user='root',       # Явно указываем пользователя
                password='root',       # Ваш пароль (если установлен)
                port=3306,         # Явно указываем порт
                auth_plugin='mysql_native_password',  # Важно для MySQL 8.0+
                database='eye_clinic_db'  # Добавляем имя базы данных
            )
        except Error as e:
            print(f"Ошибка подключения: {e}")
            raise  # Прерываем выполнение при ошибке подключения

    def add_patient(self, patient_data):
        """Добавление нового пациента в БД"""
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO patients (fio, gender, age, address, diagnosis)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                patient_data['fio'],
                patient_data['gender'],
                patient_data['age'],
                patient_data['address'],
                patient_data['diagnosis']
            ))
            self.connection.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Ошибка при добавлении пациента: {e}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()

    def get_all_patients(self):
        """Получение списка всех пациентов"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM patients")
            return cursor.fetchall()
        except Error as e:
            print(f"Ошибка при получении пациентов: {e}")
            return []
        finally:
            if 'cursor' in locals():
                cursor.close()

    def __del__(self):
        """Закрытие соединения при уничтожении объекта"""
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.connection.close()