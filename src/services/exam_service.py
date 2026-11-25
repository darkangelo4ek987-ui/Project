from src.repositories import exam_repository, student_repository


def add_exam_result(student_id: int, discipline_id: int, grade: int, exam_date: str, semester: int, is_retake: int):
    # 1. Проверяем корректность входных данных
    if grade not in [2, 3, 4, 5]:
        raise ValueError("Ошибка: Оценка должна быть в диапазоне от 2 до 5!")

    if semester not in (1, 2):
        raise ValueError("Ошибка: Семестр должен быть равен 1 или 2!")

    if is_retake not in (0, 1):
        raise ValueError("Ошибка: Пересдача должна быть 0 (нет) или 1 (да)!")

    # 2. Проверяем, существуют ли студент и дисциплина в базе
    student = student_repository.get_by_id(student_id)
    if not student:
        raise ValueError(f"Ошибка: Студент с ID {student_id} не найден в базе данных!")

    if not exam_repository.discipline_exists(discipline_id):
        raise ValueError(f"Ошибка: Дисциплина с ID {discipline_id} не найдена в базе данных!")

    # 3. Сохраняем в базу данных через репозиторий
    exam_repository.create(student_id, discipline_id, grade, exam_date, semester, is_retake)


def delete_exam_result(exam_id: int, role_id: int | None = None) -> None:
    if role_id is not None and role_id not in (1, 2):
        raise PermissionError("Недостаточно прав для удаления результата экзамена")

    if not isinstance(exam_id, int) or exam_id <= 0:
        raise ValueError("ID результата экзамена должен быть положительным числом")

    deleted = exam_repository.delete_by_id(exam_id)
    if deleted is False:
        raise ValueError(f"Запись с ID {exam_id} не найдена")