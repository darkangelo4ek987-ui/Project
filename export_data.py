import csv
import json
import os
import xml.etree.ElementTree as ET
from database.database import get_connection


def _escape_yaml_scalar(value) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)

    text = str(value)
    if text == "":
        return '""'

    # Если есть спецсимволы, двоеточия, переносы или ведущие/замыкающие пробелы — берём в кавычки
    special_chars = (":", "#", "{", "}", "[", "]", ",", "&", "*", "?", "|", "-", "<", ">", "=", "!", "%", "@", "`", '"', "'", "\n", "\r")
    if (
        text != text.strip()
        or text.lower() in ("true", "false", "null", "yes", "no", "~")
        or any(ch in text for ch in special_chars)
    ):
        escaped = text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r")
        return f'"{escaped}"'
    return text


def _to_yaml_lines(data, indent: int = 0) -> list[str]:
    pad = " " * indent
    lines: list[str] = []

    if isinstance(data, list):
        if not data:
            return [f"{pad}[]"]
        for item in data:
            if isinstance(item, dict):
                items = list(item.items())
                first_k, first_v = items[0]
                if isinstance(first_v, (dict, list)):
                    lines.append(f"{pad}- {first_k}:")
                    lines.extend(_to_yaml_lines(first_v, indent + 4))
                else:
                    lines.append(f"{pad}- {first_k}: {_escape_yaml_scalar(first_v)}")
                for k, v in items[1:]:
                    if isinstance(v, (dict, list)):
                        lines.append(f"{pad}  {k}:")
                        lines.extend(_to_yaml_lines(v, indent + 4))
                    else:
                        lines.append(f"{pad}  {k}: {_escape_yaml_scalar(v)}")
            elif isinstance(item, list):
                lines.append(f"{pad}-")
                lines.extend(_to_yaml_lines(item, indent + 2))
            else:
                lines.append(f"{pad}- {_escape_yaml_scalar(item)}")
    elif isinstance(data, dict):
        if not data:
            return [f"{pad}{{}}"]
        for k, v in data.items():
            if isinstance(v, (dict, list)):
                lines.append(f"{pad}{k}:")
                lines.extend(_to_yaml_lines(v, indent + 2))
            else:
                lines.append(f"{pad}{k}: {_escape_yaml_scalar(v)}")
    else:
        lines.append(f"{pad}{_escape_yaml_scalar(data)}")

    return lines


def _build_nested_records(raw_rows: list[tuple], field_mapping: list[tuple[str, str | None]]) -> list[dict]:
    """
    field_mapping — список кортежей (имя_колонки_в_выборке, имя_вложенного_объекта_или_None).
    Если второй элемент None — поле кладётся в корень записи.
    Если задано имя (например, 'group') — поле кладётся во вложенный словарь с этим ключом.
    """
    records: list[dict] = []
    for row in raw_rows:
        record: dict = {}
        for idx, (col_name, nested_group) in enumerate(field_mapping):
            val = row[idx]
            if nested_group:
                record.setdefault(nested_group, {})[col_name] = val
            else:
                record[col_name] = val
        records.append(record)
    return records


def _append_xml_value(parent: ET.Element, tag: str, value) -> None:
    el = ET.SubElement(parent, tag)
    if isinstance(value, dict):
        for k, v in value.items():
            _append_xml_value(el, k, v)
    elif isinstance(value, list):
        for item in value:
            _append_xml_value(el, "item", item)
    else:
        el.text = "" if value is None else str(value)


def export_records(
    records: list[dict],
    flat_headers: list[str],
    flat_rows: list[tuple],
    output_dir: str,
    root_tag: str = "records",
    item_tag: str = "record",
) -> None:
    """Универсальный экспорт подготовленных записей в JSON, CSV, XML и YAML."""
    os.makedirs(output_dir, exist_ok=True)

    # 1. JSON
    json_path = os.path.join(output_dir, "data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=4)

    # 2. CSV
    csv_path = os.path.join(output_dir, "data.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(flat_headers)
        for row in flat_rows:
            writer.writerow(["" if v is None else v for v in row])

    # 3. XML (с отступами вниз через ET.indent)
    xml_path = os.path.join(output_dir, "data.xml")
    root = ET.Element(root_tag)
    for rec in records:
        item_el = ET.SubElement(root, item_tag)
        for k, v in rec.items():
            _append_xml_value(item_el, k, v)
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)
    tree.write(xml_path, encoding="utf-8", xml_declaration=True)

    # 4. YAML (нативный YAML с отступами и списками)
    yaml_path = os.path.join(output_dir, "data.yaml")
    yaml_content = "\n".join(_to_yaml_lines(records)) + "\n"
    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write(yaml_content)


def run_export_for_query(
    sql_query: str,
    field_mapping: list[tuple[str, str | None]],
    output_dir: str,
    root_tag: str = "students",
    item_tag: str = "student",
) -> None:
    """Выполняет переданный SQL-запрос как параметр и выгружает данные во все форматы."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql_query)
        rows = cur.fetchall()
    finally:
        conn.close()

    flat_headers = [col_name for col_name, _ in field_mapping]
    records = _build_nested_records(rows, field_mapping)
    export_records(
        records=records,
        flat_headers=flat_headers,
        flat_rows=rows,
        output_dir=output_dir,
        root_tag=root_tag,
        item_tag=item_tag,
    )


def main() -> None:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(base_dir, "out")

    # Параметры таблицы/запроса и структуры полей вынесены отдельно от логики форматов:
    # при смене таблицы меняются только эти параметры, а не код сериализации.
    sql = """
        SELECT
            s.student_id,
            s.full_name,
            s.record_book_number,
            s.birth_date,
            s.group_id,
            g.name
        FROM Student s
        LEFT JOIN "Group" g ON s.group_id = g.group_id
    """
    fields = [
        ("id", None),
        ("full_name", None),
        ("record_book_number", None),
        ("birth_date", None),
        ("group_id", "group"),
        ("group_name", "group"),
    ]

    run_export_for_query(
        sql_query=sql,
        field_mapping=fields,
        output_dir=out_dir,
        root_tag="students",
        item_tag="student",
    )
    print(f"Готово! Файлы обновлены в папке: {out_dir}")


if __name__ == "__main__":
    main()