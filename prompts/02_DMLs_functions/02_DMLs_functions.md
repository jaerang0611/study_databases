```
{
  "request_type": "Generate Python Code for PostgreSQL CRUD Operations",
  "code_format_instructions": {
    "language": "Python",
    "required_libraries": ["psycopg2"],
    "structure": "Single executable file structure.",
    "priority": "All constants (DB info), functions, and the main execution block (if __name__ == '__main__':) MUST be sequentially included in the same file without external dependencies or separate files."
  },
  "db_connection_info": {
    "DB_HOST": "db_postgresql",
    "DB_PORT": "5432",
    "DB_NAME": "main_db",
    "DB_USER": "admin",
    "DB_PASSWORD": "admin123"
  },
  "constants_definition": [
    "DB_HOST = \"db_postgresql\"",
    "DB_PORT = \"5432\"",
    "DB_NAME = \"main_db\"",
    "DB_USER = \"admin\"",
    "DB_PASSWORD = \"admin123\""
  ],
  "imports": [
    "import psycopg2",
    "from psycopg2 import sql",
    "from typing import List, Dict, Any"
  ],
  "python_functions": [
    {
      "function_name": "connect_db",
      "description": "데이터베이스 연결을 설정하고 connection 및 cursor 객체를 반환합니다.",
      "code_logic": [
        "def connect_db():",
        "    try:",
        "        conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)",
        "        conn.autocommit = True",
        "        cur = conn.cursor()",
        "        return conn, cur",
        "    except Exception as e:",
        "        print(f\"데이터베이스 연결 오류가 발생했습니다: {e}\")",
        "        return None, None"
      ]
    },
    {
      "function_name": "close_db",
      "description": "데이터베이스 연결을 닫습니다.",
      "code_logic": [
        "def close_db(conn, cur):",
        "    if cur:",
        "        cur.close()",
        "    if conn:",
        "        conn.close()"
      ]
    },
    {
      "function_name": "create_books_table",
      "problem_number": 1,
      "description": "문제 1: 'books' 테이블을 생성합니다. 요청된 'id UUID PRIMARY KEY DEFAULT uuid_generate_v4()' 구문을 반드시 사용해야 합니다. 순서 보장을 위해 serial_no를 Unique 컬럼으로 추가합니다.",
      "code_logic": [
        "def create_books_table():",
        "    conn, cur = connect_db()",
        "    if not conn: return",
        "    try:",
        "        # **** 경고: 이 테이블 생성 쿼리에서 'uuid_generate_v4()' 함수는 절대 'gen_random_uuid()'로 변경되어서는 안 됩니다. **** ",
        "        # cur.execute(\"CREATE EXTENSION IF NOT EXISTS \\\"uuid-ossp\\\"\") # uuid_generate_v4() 사용을 위해 필요할 수 있음.",
        "        cur.execute(\"\"\"",
        "            CREATE TABLE IF NOT EXISTS books (",
        "                serial_no SERIAL UNIQUE NOT NULL,  -- 순서 보장용 순번",
        "                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),  -- **** 사용자가 강력히 요청한 PRIMARY KEY 정의 (변경 불가) **** ",
        "                title VARCHAR(100) NOT NULL,",
        "                price INT NOT NULL",
        "            )",
        "        \"\"\")",
        "        print(\"books 테이블이 생성되었습니다.\")",
        "    except Exception as e:",
        "        print(f\"테이블 생성 중 오류가 발생했습니다: {e}\")",
        "    finally:",
        "        close_db(conn, cur)"
      ]
    },
    {
      "function_name": "insert_books",
      "problem_number": 2,
      "description": "문제 2: 테스트용 도서 데이터를 삽입합니다. id는 자동 UUID이므로 제외됩니다.",
      "code_logic": [
        "def insert_books():",
        "    conn, cur = connect_db()",
        "    if not conn: return",
        "    data = [",
        "        ('파이썬 입문', 19000),",
        "        ('알고리즘 기초', 25000),",
        "        ('네트워크 이해', 30000)",
        "    ]",
        "    insert_query = sql.SQL(\"INSERT INTO books (title, price) VALUES ({}, {})\").format(sql.Placeholder(), sql.Placeholder())",
        "    try:",
        "        cur.executemany(insert_query, data)",
        "        print(f\"{len(data)}개 도서가 삽입되었습니다.\")",
        "    except Exception as e:",
        "        print(f\"데이터 삽입 중 오류가 발생했습니다: {e}\")",
        "    finally:",
        "        close_db(conn, cur)"
      ]
    },
    {
      "function_name": "get_all_books",
      "problem_number": 3,
      "description": "문제 3: 전체 조회 함수",
      "code_logic": [
        "def get_all_books():",
        "    conn, cur = connect_db()",
        "    if not conn: return []",
        "    try:",
        "        cur.execute(\"SELECT serial_no, id, title, price FROM books ORDER BY serial_no ASC\")",
        "        records = cur.fetchall()",
        "        print(\"--- 전체 도서 목록 (serial_no 순) ---\")",
        "        for record in records:",
        "            print(f\"순번: {record[0]}, ID: {record[1]}, 제목: {record[2]}, 가격: {record[3]}원\")",
        "        return records",
        "    except Exception as e:",
        "        print(f\"전체 조회 중 오류가 발생했습니다: {e}\")",
        "        return []",
        "    finally:",
        "        close_db(conn, cur)"
      ]
    },
    {
      "function_name": "get_expensive_books",
      "problem_number": 3,
      "description": "문제 3: 가격이 25000원 이상인 데이터 조회 함수",
      "code_logic": [
        "def get_expensive_books():",
        "    conn, cur = connect_db()",
        "    if not conn: return []",
        "    try:",
        "        cur.execute(\"SELECT serial_no, id, title, price FROM books WHERE price >= %s ORDER BY serial_no ASC\", (25000,))",
        "        records = cur.fetchall()",
        "        print(\"--- 25000원 이상 도서 목록 ---\")",
        "        for record in records:",
        "            print(f\"순번: {record[0]}, ID: {record[1]}, 제목: {record[2]}, 가격: {record[3]}원\")",
        "        return records",
        "    except Exception as e:",
        "        print(f\"가격 조회 중 오류가 발생했습니다: {e}\")",
        "        return []",
        "    finally:",
        "        close_db(conn, cur)"
      ]
    },
    {
      "function_name": "get_book_by_title",
      "problem_number": 3,
      "description": "문제 3: title 이 “파이썬 입문”인 데이터 조회 함수",
      "parameters": ["title: str"],
      "code_logic": [
        "def get_book_by_title(title: str):",
        "    conn, cur = connect_db()",
        "    if not conn: return []",
        "    try:",
        "        cur.execute(\"SELECT serial_no, id, title, price FROM books WHERE title = %s ORDER BY serial_no ASC\", (title,))",
        "        records = cur.fetchall()",
        "        print(f\"--- 제목 '{title}' 도서 목록 ---\")",
        "        for record in records:",
        "            print(f\"순번: {record[0]}, ID: {record[1]}, 제목: {record[2]}, 가격: {record[3]}원\")",
        "        return records",
        "    except Exception as e:",
        "        print(f\"제목 조회 중 오류가 발생했습니다: {e}\")",
        "        return []",
        "    finally:",
        "        close_db(conn, cur)"
      ]
    },
    {
      "function_name": "update_second_book_price",
      "problem_number": 4,
      "description": "문제 4: 저장된 순서(serial_no 기준)에서 두 번째 도서의 가격을 27000으로 수정합니다.",
      "code_logic": [
        "def update_second_book_price():",
        "    conn, cur = connect_db()",
        "    if not conn: return",
        "    try:",
        "        # serial_no 순으로 정렬하여 두 번째 도서의 ID를 조회 (OFFSET 1)",
        "        cur.execute(\"SELECT id FROM books ORDER BY serial_no ASC LIMIT 1 OFFSET 1\")",
        "        result = cur.fetchone()",
        "        if result:",
        "            second_book_id = result[0]",
        "            cur.execute(\"UPDATE books SET price = %s WHERE id = %s\", (27000, second_book_id))",
        "            print(\"두 번째 도서 가격이 27000으로 수정되었습니다.\")",
        "        else:",
        "            print(\"두 번째 도서를 찾을 수 없어 가격 수정에 실패했습니다.\")",
        "    except Exception as e:",
        "        print(f\"가격 수정 중 오류가 발생했습니다: {e}\")",
        "    finally:",
        "        close_db(conn, cur)"
      ]
    },
    {
      "function_name": "delete_third_book",
      "problem_number": 5,
      "description": "문제 5: 저장된 순서(serial_no 기준)에서 세 번째 도서 데이터를 삭제합니다.",
      "code_logic": [
        "def delete_third_book():",
        "    conn, cur = connect_db()",
        "    if not conn: return",
        "    try:",
        "        # serial_no 순으로 정렬하여 세 번째 도서의 ID를 조회 (OFFSET 2)",
        "        cur.execute(\"SELECT id FROM books ORDER BY serial_no ASC LIMIT 1 OFFSET 2\")",
        "        result = cur.fetchone()",
        "        if result:",
        "            third_book_id = result[0]",
        "            cur.execute(\"DELETE FROM books WHERE id = %s\", (third_book_id,))",
        "            print(\"세 번째 도서가 삭제되었습니다.\")",
        "        else:",
        "            print(\"세 번째 도서를 찾을 수 없어 삭제에 실패했습니다.\")",
        "    except Exception as e:",
        "        print(f\"데이터 삭제 중 오류가 발생했습니다: {e}\")",
        "    finally:",
        "        close_db(conn, cur)"
      ]
    }
  ],
  "main_execution": {
    "section": "if __name__ == '__main__':",
    "steps": [
      "print(\"--- [문제 1] 테이블 생성 --- \")",
      "create_books_table()",
      "print(\"\\n--- [문제 2] 데이터 삽입 --- \")",
      "insert_books()",
      "print(\"\\n--- [문제 3] 데이터 조회 --- \")",
      "get_all_books()",
      "get_expensive_books()",
      "get_book_by_title(\"파이썬 입문\")",
      "print(\"\\n--- [문제 4] 데이터 수정 --- \")",
      "update_second_book_price()",
      "get_all_books()",
      "print(\"\\n--- [문제 5] 데이터 삭제 --- \")",
      "delete_third_book()",
      "get_all_books()"
    ]
  }
}
```