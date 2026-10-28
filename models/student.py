from dataclasses import dataclass

@dataclass
class Student:
    student_id: int
    full_name: str
    record_book_number: str
    birth_date: str | None
    group_id: int
    group_name: str | None = None  # Вычисляемое поле (название группы)