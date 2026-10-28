from database.database import get_connection
from models.student import Student

def _map(row) -> Student:
    return Student(
        student_id=row[0],
        full_name=row[1],
        record_book_number=row[2],
        birth_date=row[3],
        group_id=row[4],
        group_name=row[5] if len(row) > 5 else None
    )

def get_all() -> list[Student]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.student_id, s.full_name, s.record_book_number, s.birth_date, s.group_id, g.name 
        FROM Student s
        JOIN "Group" g ON s.group_id = g.group_id
        ORDER BY s.full_name
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_id(student_id: int) -> Student | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT student_id, full_name, record_book_number, birth_date, group_id 
        FROM Student WHERE student_id = ?
    """, (student_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def create(full_name: str, record_book_number: str, birth_date: str, group_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Student (full_name, record_book_number, birth_date, group_id)
        VALUES (?, ?, ?, ?)
    """, (full_name, record_book_number, birth_date, group_id))
    conn.commit()
    conn.close()