import sqlite3

def init_database():
    # Создаем/подключаем файл базы данных в корне проекта
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Включаем поддержку внешних ключей в SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Читаем SQL-скрипт из schema.sql
    with open('schema.sql', 'r', encoding='utf-8') as f:
        sql_script = f.read()

    # Выполняем создание таблиц и добавление данных
    cursor.executescript(sql_script)

    conn.commit()
    conn.close()
    print("База данных успешно создана и заполнена тестовыми данными!")

if __name__ == '__main__':
    init_database()