from src.repositories import student_repository

def add_student(full_name: str, record_book_number: str, birth_date: str, group_id: int):
    if not full_name or not full_name.strip():
        raise ValueError("ФИО студента не может быть пустым или состоять из пробелов!")
    
    if not record_book_number or not record_book_number.strip():
        raise ValueError("Номер зачетной книжки не может быть пустым!")
        
    student_repository.create(full_name.strip(), record_book_number.strip(), birth_date.strip(), group_id)

def delete_student(student_id: int):
    student = student_repository.get_by_id(student_id)
    if not student:
        raise Exception(f"Студент с ID {student_id} не найден!")
    student_repository.delete(student_id)