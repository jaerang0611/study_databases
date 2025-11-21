```
아래 문제에 대한 PostgreSQL 쿼리문을 만들어 줘.
```

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

INSERT INTO books (book_id, title, price)
VALUES (1, '책 A', 10000);

INSERT INTO books (book_id, title, price)
VALUES (2, '책 B', 15000);