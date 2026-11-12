import os
import csv
import json
import xml.etree.ElementTree as ET
from database.database import get_connection

def export_data():
    # 1. Извлекаем данные с помощью SQL-запроса (JOIN таблиц Student и Group)
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT s.student_id, s.full_name, s.record_book_number, s.birth_date, s.group_id, g.name
        FROM Student s
        LEFT JOIN "Group" g ON s.group_id = g.group_id
    """)
    rows = cur.fetchall()
    conn.close()

    # Преобразуем строки из БД в удобный список словарей
    students_list = []
    for row in rows:
        student_dict = {
            "id": row[0],
            "full_name": row[1],
            "record_book_number": row[2],
            "birth_date": row[3],
            "group": {
                "group_id": row[4],
                "group_name": row[5] if row[5] else "Не указана"
            }
        }
        students_list.append(student_dict)

    # 2. Определяем путь к папке out в корне проекта
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "out")
    os.makedirs(output_dir, exist_ok=True)

    # --- Экспорт в JSON ---
    json_path = os.path.join(output_dir, "data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(students_list, f, ensure_ascii=False, indent=4)
    print(f"Файл создан: {json_path}")

    # --- Экспорт в CSV ---
    csv_path = os.path.join(output_dir, "data.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["student_id", "full_name", "record_book_number", "birth_date", "group_id", "group_name"])
        for row in rows:
            writer.writerow(row)
    print(f"Файл создан: {csv_path}")

    # --- Экспорт в XML ---
    root = ET.Element("students")
    for s in students_list:
        student_el = ET.SubElement(root, "student")
        
        ET.SubElement(student_el, "id").text = str(s["id"])
        ET.SubElement(student_el, "full_name").text = str(s["full_name"])
        ET.SubElement(student_el, "record_book_number").text = str(s["record_book_number"])
        ET.SubElement(student_el, "birth_date").text = str(s["birth_date"])
        
        group_el = ET.SubElement(student_el, "group")
        ET.SubElement(group_el, "group_id").text = str(s["group"]["group_id"])
        ET.SubElement(group_el, "group_name").text = str(s["group"]["group_name"])

    xml_path = os.path.join(output_dir, "data.xml")
    tree = ET.ElementTree(root)
    tree.write(xml_path, encoding="utf-8", xml_declaration=True)
    print(f"Файл создан: {xml_path}")

    # --- Экспорт в YAML (через встроенную сериализацию) ---
    yaml_path = os.path.join(output_dir, "data.yaml")
    with open(yaml_path, "w", encoding="utf-8") as f:
        json.dump(students_list, f, ensure_ascii=False, indent=2)
    print(f"Файл создан: {yaml_path}")

    print("\nВсе файлы успешно сгенерированы в папке 'out'!")

if __name__ == "__main__":
    export_data()