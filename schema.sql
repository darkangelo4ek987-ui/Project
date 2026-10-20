-- =========================================================
-- 1. УДАЛЕНИЕ СТАРЫХ ТАБЛИЦ (в обратном порядке)
-- =========================================================
DROP TABLE IF EXISTS ExamResult;
DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS Discipline;
DROP TABLE IF EXISTS "Group";
DROP TABLE IF EXISTS "User";
DROP TABLE IF EXISTS UserRole;

-- =========================================================
-- 2. СОЗДАНИЕ ТАБЛИЦ
-- =========================================================

-- Таблица ролей пользователей (Администратор, Сотрудник деканата)
CREATE TABLE UserRole (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Таблица пользователей системы (сотрудники, авторизация)
CREATE TABLE "User" (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    patronymic TEXT,
    password_hash TEXT NOT NULL,
    user_role INTEGER NOT NULL,
    FOREIGN KEY (user_role) REFERENCES UserRole (role_id) ON DELETE CASCADE
);

-- Таблица учебных групп
CREATE TABLE "Group" (
    group_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    course INTEGER NOT NULL,
    specialty TEXT NOT NULL
);

-- Таблица дисциплин
CREATE TABLE Discipline (
    discipline_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    control_type TEXT NOT NULL
);

-- Таблица студентов
CREATE TABLE Student (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    record_book_number TEXT NOT NULL UNIQUE,
    birth_date TEXT,
    group_id INTEGER NOT NULL,
    FOREIGN KEY (group_id) REFERENCES "Group" (group_id) ON DELETE CASCADE
);

-- Таблица результатов экзаменов
CREATE TABLE ExamResult (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    discipline_id INTEGER NOT NULL,
    grade INTEGER,
    exam_date TEXT NOT NULL,
    semester INTEGER NOT NULL,
    is_retake INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (student_id) REFERENCES Student (student_id) ON DELETE CASCADE,
    FOREIGN KEY (discipline_id) REFERENCES Discipline (discipline_id) ON DELETE CASCADE
);

-- =========================================================
-- 3. НАПОЛНЕНИЕ ТЕСТОВЫМИ ДАННЫМИ
-- =========================================================

-- Роли пользователей
INSERT INTO UserRole (name) VALUES
    ('Admin'),
    ('DeaneryStaff');

-- Пользователи системы (без лишнего balance)
INSERT INTO "User" (name, surname, patronymic, password_hash, user_role) VALUES
    ('Егор', 'Алешин', 'Викторович', 'hash_pass_123', 1),
    ('Валерия', 'Кулясова', 'Павловна', 'hash_pass_456', 2);

-- Группы
INSERT INTO "Group" (name, course, specialty) VALUES
    ('26-ИВТ-2-2', 1, 'Информатика и вычислительная техника'),
    ('25-ИВТ-1-1', 2, 'Информатика и вычислительная техника');

-- Дисциплины
INSERT INTO Discipline (name, control_type) VALUES
    ('Информатика', 'Экзамен'),
    ('Высшая математика', 'Экзамен'),
    ('Программирование', 'Зачет');

-- Студенты
INSERT INTO Student (full_name, record_book_number, birth_date, group_id) VALUES
    ('Алешин Е.В.', '26-ИВТ-001', '2008-05-13', 1),
    ('Кулибин И.Г.', '26-ИВТ-002', '2007-03-19', 1),
    ('Иванов И.А.', '25-ИВТ-003', '2008-04-15', 2);

-- Результаты экзаменов
INSERT INTO ExamResult (student_id, discipline_id, grade, exam_date, semester, is_retake) VALUES
    (1, 1, 5, '2026-01-20', 1, 0),
    (2, 1, 4, '2026-01-20', 1, 0),
    (1, 2, 4, '2026-01-24', 1, 0),
    (3, 3, 5, '2025-06-15', 2, 0);