import psycopg2
from psycopg2 import sql
from typing import List, Dict, Any

# ==============================================================================
# 🌟 데이터베이스 연결 정보 (상수 정의)
# ==============================================================================
DB_HOST = "db_postgresql"
DB_PORT = "5432"
DB_NAME = "main_db"
DB_USER = "admin"
DB_PASSWORD = "admin123"

# ==============================================================================
# ⚙️ 연결/종료 함수
# ==============================================================================

def connect_db():
    """데이터베이스 연결을 설정하고 connection 및 cursor 객체를 반환합니다."""
    try:
        conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        # autocommit=True로 설정하여 매 쿼리 후 즉시 변경사항을 반영합니다.
        conn.autocommit = True
        cur = conn.cursor()
        return conn, cur
    except Exception as e:
        print(f"데이터베이스 연결 오류가 발생했습니다: {e}")
        return None, None

def close_db(conn, cur):
    """데이터베이스 연결을 닫습니다."""
    if cur:
        cur.close()
    if conn:
        conn.close()

# ==============================================================================
# 📚 CRUD 연산 함수
# ==============================================================================

# [문제 1] 테이블 생성 (CREATE)
def create_books_table():
    """'books' 테이블을 생성합니다. uuid-ossp 확장 기능과 요청된 ID 정의를 사용합니다."""
    conn, cur = connect_db()
    if not conn: return
    try:
        # uuid_generate_v4() 사용을 위해 'uuid-ossp' 확장이 필요합니다.
        # 대부분의 최신 PostgreSQL 환경에 기본 포함되지만, 명시적으로 실행해 줍니다.
        cur.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"")
        
        # **** 사용자가 강력히 요청한 'id UUID PRIMARY KEY DEFAULT uuid_generate_v4()' 구문 사용 ****
        cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                serial_no SERIAL UNIQUE NOT NULL,  -- 순서 보장용 순번
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),  -- 요청된 PRIMARY KEY 정의
                title VARCHAR(100) NOT NULL,
                price INT NOT NULL
            )
        """)
        print("books 테이블이 생성되었습니다.")
    except Exception as e:
        print(f"테이블 생성 중 오류가 발생했습니다: {e}")
    finally:
        close_db(conn, cur)

# [문제 2] 데이터 삽입 (INSERT)
def insert_books():
    """테스트용 도서 데이터를 삽입합니다. id는 uuid_generate_v4()에 의해 자동 생성됩니다."""
    conn, cur = connect_db()
    if not conn: return
    data = [
        ('파이썬 입문', 19000),
        ('알고리즘 기초', 25000),
        ('네트워크 이해', 30000)
    ]
    # sql.SQL을 사용하여 쿼리를 안전하게 구성합니다.
    insert_query = sql.SQL("INSERT INTO books (title, price) VALUES ({}, {})").format(sql.Placeholder(), sql.Placeholder())
    try:
        # executemany를 사용하여 여러 행을 효율적으로 삽입합니다.
        cur.executemany(insert_query, data)
        print(f"{len(data)}개 도서가 삽입되었습니다.")
    except Exception as e:
        print(f"데이터 삽입 중 오류가 발생했습니다: {e}")
    finally:
        close_db(conn, cur)

# [문제 3] 데이터 조회 (READ)
def get_all_books():
    """전체 도서 데이터를 serial_no 순으로 조회하고 출력합니다."""
    conn, cur = connect_db()
    if not conn: return []
    try:
        # serial_no는 삽입 순서를 유지합니다.
        cur.execute("SELECT serial_no, id, title, price FROM books ORDER BY serial_no ASC")
        records = cur.fetchall()
        print("--- 전체 도서 목록 (serial_no 순) ---")
        for record in records:
            print(f"순번: {record[0]}, ID: {record[1]}, 제목: {record[2]}, 가격: {record[3]}원")
        return records
    except Exception as e:
        print(f"전체 조회 중 오류가 발생했습니다: {e}")
        return []
    finally:
        close_db(conn, cur)

def get_expensive_books():
    """가격이 25000원 이상인 도서 데이터를 조회하고 출력합니다."""
    conn, cur = connect_db()
    if not conn: return []
    try:
        # %s 플레이스홀더를 사용한 안전한 쿼리 실행
        cur.execute("SELECT serial_no, id, title, price FROM books WHERE price >= %s ORDER BY serial_no ASC", (25000,))
        records = cur.fetchall()
        print("--- 25000원 이상 도서 목록 ---")
        for record in records:
            print(f"순번: {record[0]}, ID: {record[1]}, 제목: {record[2]}, 가격: {record[3]}원")
        return records
    except Exception as e:
        print(f"가격 조회 중 오류가 발생했습니다: {e}")
        return []
    finally:
        close_db(conn, cur)

def get_book_by_title(title: str):
    """특정 제목의 도서 데이터를 조회하고 출력합니다."""
    conn, cur = connect_db()
    if not conn: return []
    try:
        cur.execute("SELECT serial_no, id, title, price FROM books WHERE title = %s ORDER BY serial_no ASC", (title,))
        records = cur.fetchall()
        print(f"--- 제목 '{title}' 도서 목록 ---")
        for record in records:
            print(f"순번: {record[0]}, ID: {record[1]}, 제목: {record[2]}, 가격: {record[3]}원")
        return records
    except Exception as e:
        print(f"제목 조회 중 오류가 발생했습니다: {e}")
        return []
    finally:
        close_db(conn, cur)

# [문제 4] 데이터 수정 (UPDATE)
def update_second_book_price():
    """serial_no 순으로 두 번째 도서의 가격을 27000으로 수정합니다."""
    conn, cur = connect_db()
    if not conn: return
    try:
        # serial_no 순으로 정렬하여 두 번째 도서의 ID를 조회 (OFFSET 1)
        cur.execute("SELECT id FROM books ORDER BY serial_no ASC LIMIT 1 OFFSET 1")
        result = cur.fetchone()
        
        if result:
            second_book_id = result[0]
            # 조회된 ID를 사용하여 가격을 업데이트합니다.
            cur.execute("UPDATE books SET price = %s WHERE id = %s", (27000, second_book_id))
            print("두 번째 도서 가격이 27000으로 수정되었습니다.")
        else:
            print("두 번째 도서를 찾을 수 없어 가격 수정에 실패했습니다.")
    except Exception as e:
        print(f"가격 수정 중 오류가 발생했습니다: {e}")
    finally:
        close_db(conn, cur)

# [문제 5] 데이터 삭제 (DELETE)
def delete_third_book():
    """serial_no 순으로 세 번째 도서 데이터를 삭제합니다."""
    conn, cur = connect_db()
    if not conn: return
    try:
        # serial_no 순으로 정렬하여 세 번째 도서의 ID를 조회 (OFFSET 2)
        cur.execute("SELECT id FROM books ORDER BY serial_no ASC LIMIT 1 OFFSET 2")
        result = cur.fetchone()
        
        if result:
            third_book_id = result[0]
            # 조회된 ID를 사용하여 데이터를 삭제합니다.
            cur.execute("DELETE FROM books WHERE id = %s", (third_book_id,))
            print("세 번째 도서가 삭제되었습니다.")
        else:
            print("세 번째 도서를 찾을 수 없어 삭제에 실패했습니다.")
    except Exception as e:
        print(f"데이터 삭제 중 오류가 발생했습니다: {e}")
    finally:
        close_db(conn, cur)

# ==============================================================================
# 🚀 메인 실행 블록
# ==============================================================================
if __name__ == '__main__':
    print("--- [문제 1] 테이블 생성 --- ")
    create_books_table()

    print("\n--- [문제 2] 데이터 삽입 --- ")
    insert_books()

    print("\n--- [문제 3] 데이터 조회 --- ")
    get_all_books()
    print("")
    get_expensive_books()
    print("")
    get_book_by_title("파이썬 입문")

    print("\n--- [문제 4] 데이터 수정 --- ")
    update_second_book_price()
    get_all_books() # 수정 확인

    print("\n--- [문제 5] 데이터 삭제 --- ")
    delete_third_book()
    get_all_books() # 삭제 확인