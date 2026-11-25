import re
from datetime import datetime
from src.ui import auth_ui
from src.repositories import student_repository, exam_repository
from src.services import exam_service, student_service


def _read_strict_int(
    prompt: str,
    field_name: str,
    min_val: int = 1,
    max_val: int | None = None,
) -> int:
    while True:
        raw = input(prompt).strip()
        if not re.fullmatch(r"\d+", raw):
            print(f"[Ошибка ввода ({field_name})]: введите целое число только из цифр.")
            continue

        value = int(raw)
        if value < min_val:
            print(f"[Ошибка ввода ({field_name})]: значение должно быть не меньше {min_val}.")
            continue

        if max_val is not None and value > max_val:
            print(f"[Ошибка ввода ({field_name})]: значение должно быть не больше {max_val}.")
            continue

        return value


def _read_strict_choice(prompt: str, field_name: str, allowed: tuple[str, ...]) -> str:
    while True:
        raw = input(prompt).strip()
        if raw in allowed:
            return raw
        print(f"[Ошибка ввода ({field_name})]: допустимы только значения {', '.join(allowed)}.")


def _read_strict_date(prompt: str, field_name: str = "Дата экзамена") -> str:
    while True:
        raw = input(prompt).strip()
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw):
            print(f"[Ошибка ввода ({field_name})]: используйте строгий формат ГГГГ-ММ-ДД (например, 2026-05-20).")
            continue

        try:
            parsed = datetime.strptime(raw, "%Y-%m-%d")
        except ValueError:
            print(f"[Ошибка ввода ({field_name})]: некорректная календарная дата.")
            continue

        if not (2000 <= parsed.year <= 2100):
            print(f"[Ошибка ввода ({field_name})]: год должен быть в пределах от 2000 до 2100.")
            continue

        return raw


def _read_existing_student_id() -> int:
    while True:
        s_id = _read_strict_int("ID студента: ", "ID студента", min_val=1)
        if student_repository.get_by_id(s_id):
            return s_id
        print(f"[Ошибка ввода (ID студента)]: студент с ID {s_id} не найден в базе данных.")


def _read_existing_discipline_id() -> int:
    while True:
        d_id = _read_strict_int("ID дисциплины: ", "ID дисциплины", min_val=1)
        if exam_repository.discipline_exists(d_id):
            return d_id
        print(f"[Ошибка ввода (ID дисциплины)]: дисциплина с ID {d_id} не найдена в базе данных.")


def run():
    current_user = auth_ui.login()
    if not current_user:
        return

    while True:
        print(f"\n===== УЧЕТ РЕЗУЛЬТАТОВ ЭКЗАМЕНОВ (Роль ID: {current_user.user_role}) =====")
        print("1. Посмотреть список студентов")
        print("2. Добавить результат экзамена (Сотрудники)")
        print("3. Просмотреть все результаты экзаменов")
        print("4. Удалить результат экзамена по ID (Сотрудники)")
        print("5. Удалить студента по ID (Сотрудники)")
        print("0. Выход")

        choice = input("Выберите пункт меню: ").strip()

        try:
            if choice == "1":
                students = student_repository.get_all()
                print("\n--- Список студентов ---")
                for s in students:
                    print(
                        f"ID: {s.student_id} | ФИО: {s.full_name} | "
                        f"Зачетка: {s.record_book_number} | Группа: {s.group_name}"
                    )

            elif choice == "2":
                if current_user.user_role != 1:
                    raise PermissionError("Недостаточно прав! Доступно только сотрудникам.")

                print("\n--- Добавление оценки ---")
                s_id = _read_existing_student_id()
                d_id = _read_existing_discipline_id()
                grade = _read_strict_int("Оценка (2-5): ", "Оценка", min_val=2, max_val=5)
                date = _read_strict_date("Дата экзамена (ГГГГ-ММ-ДД): ", "Дата экзамена")
                sem = _read_strict_int("Семестр (1-2): ", "Семестр", min_val=1, max_val=2)
                retake = int(_read_strict_choice("Пересдача (0 - нет, 1 - да): ", "Пересдача", ("0", "1")))

                exam_service.add_exam_result(s_id, d_id, grade, date, sem, retake)
                print("Успешно добавлено!")

            elif choice == "3":
                results = exam_repository.get_all()
                print("\n--- Результаты экзаменов ---")
                for r in results:
                    print(
                        f"ID записи: {r.result_id} | Студент ID: {r.student_id} | "
                        f"Дисциплина ID: {r.discipline_id} | Оценка: {r.grade}"
                    )

            elif choice == "4":
                if current_user.user_role != 1:
                    raise PermissionError("Недостаточно прав!")
                r_id = _read_strict_int(
                    "Введите ID результата экзамена для удаления: ",
                    "ID результата экзамена",
                    min_val=1,
                )
                exam_service.delete_exam_result(r_id)
                print("Результат экзамена успешно удален из базы данных!")

            elif choice == "5":
                if current_user.user_role != 1:
                    raise PermissionError("Недостаточно прав!")
                s_id = _read_strict_int(
                    "Введите ID студента для удаления: ",
                    "ID студента",
                    min_val=1,
                )
                student_service.delete_student(s_id)
                print("Студент успешно удален из базы данных!")

            elif choice == "0":
                print("Выход. До свидания!")
                break
            else:
                print("Неверный пункт меню. Введите цифру от 0 до 5.")

        except ValueError as e:
            print(f"[Ошибка валидации]: {e}")
        except Exception as e:
            print(f"[Ошибка]: {e}")