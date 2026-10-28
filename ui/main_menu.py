from ui import auth_ui
from repositories import student_repository, exam_repository
from services import exam_service

def run():
    current_user = auth_ui.login()
    if not current_user:
        return

    while True:
        print("\n===== УЧЕТ РЕЗУЛЬТАТОВ ЭКЗАМЕНОВ =====")
        print("1. Посмотреть список студентов")
        print("2. Добавить результат экзамена")
        print("3. Просмотреть все результаты экзаменов")
        print("0. Выход")
        
        choice = input("Выберите пункт меню: ").strip()
        
        try:
            if choice == "1":
                students = student_repository.get_all()
                print("\n--- Список студентов ---")
                for s in students:
                    print(f"ID: {s.student_id} | ФИО: {s.full_name} | Зачетка: {s.record_book_number} | Группа: {s.group_name}")
            
            elif choice == "2":
                print("\n--- Добавление оценки ---")
                s_id = int(input("ID студента: "))
                d_id = int(input("ID дисциплины: "))
                grade = int(input("Оценка (2-5): "))
                date = input("Дата экзамена (ГГГГ-ММ-ДД): ")
                sem = int(input("Семестр: "))
                retake = int(input("Пересдача (0 - нет, 1 - да): "))
                
                exam_service.add_exam_result(s_id, d_id, grade, date, sem, retake)
                print("Результат экзамена успешно добавлен!")
                
            elif choice == "3":
                results = exam_repository.get_all()
                print("\n--- Результаты экзаменов ---")
                for r in results:
                    print(f"Студент ID: {r.student_id} | Дисциплина ID: {r.discipline_id} | Оценка: {r.grade} | Семестр: {r.semester}")
                    
            elif choice == "0":
                print("Выход из программы. До свидания!")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")
        except Exception as e:
            print(f"[Ошибка]: {e}")