import sqlite3
import os

def get_connection():
    # Путь к файлу database.db в корне проекта
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database.db")
    return sqlite3.connect(db_path)