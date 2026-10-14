-- 1. Удаление старых таблиц
DROP TABLE IF EXISTS ExamResult;
DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS Discipline;
DROP TABLE IF EXISTS "Group";

-- 2. Создание таблиц
CREATE TABLE "Group" (
    group_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    course INTEGER NOT NULL,
    specialty TEXT NOT NULL
);

CREATE TABLE Discipline (
    discipline_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    control_type TEXT NOT NULL
);

CREATE TABLE Student (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    record_book_number TEXT NOT NULL UNIQUE,
    birth_date TEXT,
    group_id INTEGER NOT NULL,
    FOREIGN KEY (group_id) REFERENCES "Group" (group_id) ON DELETE CASCADE
);

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

-- 3. Добавление тестовых данных
INSERT INTO "Group" (name, course, specialty) VALUES
    ('26-ИВТ-2-2', 1, 'Информатика и вычислительная техника'),
    ('25-ИВТ-1-1', 2, 'Информатика и вычислительная техника');

INSERT INTO Discipline (name, control_type) VALUES
    ('Информатика', 'Экзамен'),
    ('Высшая математика', 'Экзамен'),
    ('Программирование', 'Зачет');

INSERT INTO Student (full_name, record_book_number, birth_date, group_id) VALUES
    ('Алешин Е.В.', '26-ИВТ-001', '2008-05-13', 1),
    ('Кулибин И.Г.', '26-ИВТ-002', '2007-03-19', 1),
    ('Иванов И.А.', '25-ИВТ-003', '2008-04-15', 2);

INSERT INTO ExamResult (student_id, discipline_id, grade, exam_date, semester, is_retake) VALUES
    (1, 1, 5, '2026-01-20', 1, 0),
    (2, 1, 4, '2026-01-20', 1, 0),
    (1, 2, 4, '2026-01-24', 1, 0),
    (3, 3, 5, '2025-06-15', 2, 0);