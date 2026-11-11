from src.repositories import exam_repository, student_repository

def add_exam_result(student_id: int, discipline_id: int, grade: int, exam_date: str, semester: int, is_retake: int):
    # Жесткая валидация оценки
    if grade not in [2, 3, 4, 5]:
        raise ValueError("Ошибка: Оценка должна быть целым числом в диапазоне от 2 до 5!")
    
    if not student_repository.get_by_id(student_id):
        raise Exception(f"Ошибка: Студент с ID {student_id} не найден в базе данных!")

    exam_repository.create(student_id, discipline_id, grade, exam_date, semester, is_retake)

def delete_exam_result(result_id: int):
    # Проверяем, существует ли такой результат перед удалением (или просто удаляем)
    exam_repository.delete(result_id)

def add_exam_result(student_id: int, discipline_id: int, grade: int, exam_date: str, semester: int, is_retake: int):
    # 1. Проверяем корректность оценки
    if grade not in [2, 3, 4, 5]:
        raise ValueError("Ошибка: Оценка должна быть в диапазоне от 2 до 5!")
    
    # 2. Проверяем, существует ли студент в базе
    if not student_repository.get_by_id(student_id):
        raise ValueError("Ошибка: указанный студент не найден в базе данных!")
        
    # 3. Добавляем в репозиторий, только если все проверки прошли успешно
    exam_repository.create(student_id, discipline_id, grade, exam_date, semester, is_retake)