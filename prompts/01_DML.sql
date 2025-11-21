CREATE TABLE students (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    age INT
);

INSERT INTO students (id, name, age) VALUES (1, '홍길동', 23);
INSERT INTO students (id, name, age) VALUES (2, '이영희', 21);
INSERT INTO students (id, name, age) VALUES (3, '박철수', 26);

SELECT * FROM students;

SELECT * FROM students
WHERE age >= 22;

SELECT * FROM students
WHERE name = '홍길동';

UPDATE students
SET age = 25
WHERE id = 2;

DELETE FROM students
WHERE id = 3;

CREATE TABLE books (
    book_id INT PRIMARY KEY,
    title VARCHAR(100),
    price INT
);

SELECT * FROM books;

-- 1. 첫 번째 INSERT (book_id = 1)
INSERT INTO books (book_id, title, price)
VALUES (1, '책 A', 10000);

-- 2. 두 번째 INSERT (book_id를 2로 변경하여 중복 회피)
INSERT INTO books (book_id, title, price)
VALUES (2, '책 B', 15000);