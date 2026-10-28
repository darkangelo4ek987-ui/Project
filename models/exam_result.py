from dataclasses import dataclass

@dataclass
class ExamResult:
    result_id: int
    student_id: int
    discipline_id: int
    grade: int | None
    exam_date: str
    semester: int
    is_retake: int
    # Вычисляемые поля для удобного вывода в интерфейсе
    student_name: str | None = None
    discipline_name: str | None = None