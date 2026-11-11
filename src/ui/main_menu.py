from src.ui import auth_ui
from src.repositories import student_repository, exam_repository
from src.services import exam_service, student_service

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
                    print(f"ID: {s.student_id} | ФИО: {s.full_name} | Зачетка: {s.record_book_number} | Группа: {s.group_name}")
            
            elif choice == "2":
                if current_user.user_role != 1:
                    raise Exception("Недостаточно прав! Доступно только сотрудникам.")
                
                print("\n--- Добавление оценки ---")
                s_id = int(input("ID студента: ").strip())
                d_id = int(input("ID дисциплины: ").strip())
                grade = int(input("Оценка (2-5): ").strip())
                date = input("Дата экзамена (ГГГГ-ММ-ДД): ").strip()
                sem = int(input("Семестр: ").strip())
                retake = int(input("Пересдача (0 - нет, 1 - да): ").strip())
                
                exam_service.add_exam_result(s_id, d_id, grade, date, sem, retake)
                print("Успешно добавлено!")
                
            elif choice == "3":
                results = exam_repository.get_all()
                print("\n--- Результаты экзаменов ---")
                for r in results:
                    print(f"ID записи: {r.result_id} | Студент ID: {r.student_id} | Дисциплина ID: {r.discipline_id} | Оценка: {r.grade}")
            
            elif choice == "4":
                if current_user.user_role != 1:
                    raise Exception("Недостаточно прав!")
                r_id = int(input("Введите ID результата экзамена для удаления: ").strip())
                exam_service.delete_exam_result(r_id)
                print("Результат экзамена успешно удален из базы данных!")

            elif choice == "5":
                if current_user.user_role != 1:
                    raise Exception("Недостаточно прав!")
                s_id = int(input("Введите ID студента для удаления: ").strip())
                student_service.delete_student(s_id)
                print("Студент успешно удален из базы данных!")
                    
            elif choice == "0":
                print("Выход. До свидания!")
                break
            else:
                print("Неверный пункт меню. Попробуйте снова.")
                
        except ValueError:
            print("[Ошибка валидации]: Пожалуйста, вводите корректные числовые значения (ID, оценки, семестр)!")
        except Exception as e:
            print(f"[Ошибка]: {e}")