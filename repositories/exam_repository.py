from database.database import get_connection
from models.exam_result import ExamResult

def _map(row) -> ExamResult:
    return ExamResult(
        result_id=row[0],
        student_id=row[1],
        discipline_id=row[2],
        grade=row[3],
        exam_date=row[4],
        semester=row[5],
        is_retake=row[6]
    )

def get_all() -> list[ExamResult]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT result_id, student_id, discipline_id, grade, exam_date, semester, is_retake
        FROM ExamResult
        ORDER BY exam_date DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def create(student_id: int, discipline_id: int, grade: int, exam_date: str, semester: int, is_retake: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO ExamResult (student_id, discipline_id, grade, exam_date, semester, is_retake)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (student_id, discipline_id, grade, exam_date, semester, is_retake))
    conn.commit()
    conn.close()