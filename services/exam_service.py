from repositories import exam_repository, student_repository

def add_exam_result(student_id: int, discipline_id: int, grade: int, exam_date: str, semester: int, is_retake: int):
    if grade not in [2, 3, 4, 5]:
        raise Exception("Оценка должна быть в диапазоне от 2 до 5!")
    
    if not student_repository.get_by_id(student_id):
        raise Exception("Ошибка: указанный студент не найден в базе данных!")

    exam_repository.create(student_id, discipline_id, grade, exam_date, semester, is_retake)