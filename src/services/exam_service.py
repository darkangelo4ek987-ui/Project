from src.repositories import exam_repository, student_repository

def add_exam_result(student_id: int, discipline_id: int, grade: int, exam_date: str, semester: int, is_retake: int):
    # 1. Проверяем корректность оценки
    if grade not in [2, 3, 4, 5]:
        raise ValueError("Ошибка: Оценка должна быть в диапазоне от 2 до 5!")
    
    # 2. Проверяем, существует ли студент в базе
    student = student_repository.get_by_id(student_id)
    if not student:
        raise ValueError(f"Ошибка: Студент с ID {student_id} не найден в базе данных!")
        
    # 3. Сохраняем в базу данных через репозиторий
    exam_repository.create(student_id, discipline_id, grade, exam_date, semester, is_retake)