import os
from dotenv import load_dotenv

load_dotenv()  # загружает переменные из .env

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'eye_clinic_db'),
    'port': os.getenv('DB_PORT', '3306')
}