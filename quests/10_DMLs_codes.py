import psycopg2
import sys
from typing import List, Tuple, Any, Optional

# PostgreSQL 연결 설정 (Common Configuration)
DB_HOST = "db_postgresql"
DB_PORT = "5432"
DB_NAME = "main_db"
DB_USER = "admin"
DB_PASSWORD = "admin123"

# 테스트용 삽입 데이터 (요구사항에 명시된 데이터만 사용)
TEST_BOOK_DATA = [
    ["파이썬 입문", 19000],
    ["알고리즘 기초", 25000],
    ["네트워크 이해", 30000]
]

def get_connection():
    """데이터베이스 연결 객체를 생성하고 반환합니다."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except psycopg2.Error as e:
        print(f"데이터베이스 연결 오류: {e}", file=sys.stderr)
        return None

def print_books_results(results: List[Tuple]) -> None:
    """
    조회 결과를 보기 좋게 출력하는 헬퍼 함수입니다.
    UUID는 문자열로 변환한 후 앞 8자리만 슬라이싱하여 출력합니다.
    """
    if not results:
        print("  |-- (결과 없음) --|")
        return

    # 헤더 출력
    header = ["UUID (8자리)", "Title", "Price"]
    print("-" * 50)
    print(f"| {header[0]:<12} | {header[1]:<15} | {header[2]:<8} |")
    print("-" * 50)

    # 데이터 출력
    for row in results:
        # row: (id: UUID, title: str, price: int)
        book_id_str = str(row[0]) # UUID 객체를 문자열로 변환
        short_id = book_id_str[:8] # 앞 8자리 슬라이싱
        title = row[1]
        price = row[2]
        
        # 형식에 맞게 출력
        print(f"| {short_id:<12} | {title:<15} | {price:8,} |")
    
    print("-" * 50)

# ----------------------------------------------------------------------
# 문제 1: 테이블 생성 (CREATE)
# ----------------------------------------------------------------------

def create_books_table():
    """
    UUID 생성을 위한 'uuid-ossp' 확장 생성 및 'books' 테이블을 생성합니다.
    id: UUID PRIMARY KEY DEFAULT uuid_generate_v4()
    title: VARCHAR(100)
    price: INT
    """
    conn = get_connection()
    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            # 1. UUID 생성을 위해 'uuid-ossp' 확장을 먼저 생성합니다. (IF NOT EXISTS 사용)
            cur.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
            
            # 2. books 테이블 생성
            cur.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    title VARCHAR(100) NOT NULL,
                    price INT NOT NULL
                );
            """)
            conn.commit()
            print("=> [문제 1] books 테이블이 생성되었습니다.")
    except psycopg2.Error as e:
        print(f"테이블 생성 오류: {e}", file=sys.stderr)
        conn.rollback()
    finally:
        conn.close()

# ----------------------------------------------------------------------
# 문제 2: 대량 데이터 삽입 (INSERT)
# ----------------------------------------------------------------------

def insert_books(books_data: List[List[Any]]) -> None:
    """
    다수의 책 데이터를 executemany를 사용하여 효율적이고 안전하게 삽입합니다.
    id는 자동 생성됩니다.
    """
    conn = get_connection()
    if conn is None:
        return

    # SQL: id는 제외하고 title, price만 삽입
    sql = "INSERT INTO books (title, price) VALUES (%s, %s);"
    
    try:
        with conn.cursor() as cur:
            # executemany를 사용하여 일괄 삽입
            cur.executemany(sql, books_data)
            count = cur.rowcount
            conn.commit()
            print(f"=> [문제 2] {count}개 도서가 삽입되었습니다.")
    except psycopg2.Error as e:
        print(f"데이터 삽입 오류: {e}", file=sys.stderr)
        conn.rollback()
    finally:
        conn.close()

# ----------------------------------------------------------------------
# 문제 3: 데이터 조회 (READ)
# ----------------------------------------------------------------------

def get_all_books() -> List[Tuple]:
    """전체 도서 데이터를 조회합니다."""
    conn = get_connection()
    if conn is None:
        return []

    results = []
    sql = "SELECT id, title, price FROM books ORDER BY price DESC;"
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            results = cur.fetchall()
            print(f"=> [문제 3-1] 전체 도서 {len(results)}권을 조회했습니다.")
            print_books_results(results)
    except psycopg2.Error as e:
        print(f"전체 조회 오류: {e}", file=sys.stderr)
    finally:
        conn.close()
    return results

def get_expensive_books() -> List[Tuple]:
    """가격이 25000원 이상인 도서를 조회합니다."""
    conn = get_connection()
    if conn is None:
        return []

    results = []
    # 매개변수화된 쿼리를 사용하여 가격 조건 명시
    sql = "SELECT id, title, price FROM books WHERE price >= %s ORDER BY price DESC;"
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (25000,)) # 튜플 형태로 전달
            results = cur.fetchall()
            print(f"=> [문제 3-2] 가격이 25000원 이상인 도서 {len(results)}권을 조회했습니다.")
            print_books_results(results)
    except psycopg2.Error as e:
        print(f"고가 도서 조회 오류: {e}", file=sys.stderr)
    finally:
        conn.close()
    return results

def get_book_by_title(title: str) -> List[Tuple]:
    """title이 일치하는 도서를 조회합니다."""
    conn = get_connection()
    if conn is None:
        return []

    results = []
    # 매개변수화된 쿼리 사용
    sql = "SELECT id, title, price FROM books WHERE title = %s;"
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (title,))
            results = cur.fetchall()
            print(f"=> [문제 3-3] 제목이 '{title}'인 도서 {len(results)}권을 조회했습니다.")
            print_books_results(results)
    except psycopg2.Error as e:
        print(f"제목으로 도서 조회 오류: {e}", file=sys.stderr)
    finally:
        conn.close()
    return results

# ----------------------------------------------------------------------
# 문제 4: 데이터 갱신 (UPDATE)
# ----------------------------------------------------------------------

def update_second_book_price(new_price: int = 27000) -> None:
    """
    저장된 순서에서 두 번째 도서의 가격을 갱신합니다.
    UUID를 먼저 가져온 후 해당 ID로 업데이트를 수행합니다.
    """
    conn = get_connection()
    if conn is None:
        return

    # 1. 두 번째 도서의 ID를 가져옵니다. (ORDER BY는 명시되지 않았으므로 임의의 순서로 가져옴)
    # 안전성을 위해 title로 ORDER BY를 사용하겠습니다.
    select_id_sql = "SELECT id FROM books ORDER BY title ASC LIMIT 1 OFFSET 1;"
    
    try:
        with conn.cursor() as cur:
            # ID 조회
            cur.execute(select_id_sql)
            book_id_result = cur.fetchone()
            
            if book_id_result:
                target_id = book_id_result[0]
                
                # 2. 해당 ID를 사용하여 가격 갱신 (매개변수화된 쿼리 사용)
                update_sql = "UPDATE books SET price = %s WHERE id = %s;"
                cur.execute(update_sql, (new_price, target_id))
                
                conn.commit()
                if cur.rowcount > 0:
                    print(f"=> [문제 4] 두 번째 도서 (ID: {str(target_id)[:8]}...) 가격이 {new_price:,}으로 수정되었습니다.")
                else:
                    print("=> [문제 4] 업데이트 대상 도서를 찾지 못했습니다.", file=sys.stderr)
            else:
                print("=> [문제 4] 업데이트할 두 번째 도서를 찾지 못했습니다.", file=sys.stderr)
                
    except psycopg2.Error as e:
        print(f"데이터 갱신 오류: {e}", file=sys.stderr)
        conn.rollback()
    finally:
        conn.close()

# ----------------------------------------------------------------------
# 문제 5: 데이터 삭제 (DELETE)
# ----------------------------------------------------------------------

def delete_third_book() -> None:
    """
    저장된 순서에서 세 번째 도서 데이터를 삭제합니다.
    UUID를 먼저 가져온 후 해당 ID로 삭제를 수행합니다.
    """
    conn = get_connection()
    if conn is None:
        return

    # 1. 세 번째 도서의 ID를 가져옵니다. (ORDER BY는 명시되지 않았으므로 임의의 순서로 가져옴)
    # 안전성을 위해 title로 ORDER BY를 사용하겠습니다.
    select_id_sql = "SELECT id FROM books ORDER BY title ASC LIMIT 1 OFFSET 2;"
    
    try:
        with conn.cursor() as cur:
            # ID 조회
            cur.execute(select_id_sql)
            book_id_result = cur.fetchone()
            
            if book_id_result:
                target_id = book_id_result[0]
                
                # 2. 해당 ID를 사용하여 삭제 (매개변수화된 쿼리 사용)
                delete_sql = "DELETE FROM books WHERE id = %s;"
                cur.execute(delete_sql, (target_id,))
                
                conn.commit()
                if cur.rowcount > 0:
                    print(f"=> [문제 5] 세 번째 도서 (ID: {str(target_id)[:8]}...) 가 삭제되었습니다.")
                else:
                    print("=> [문제 5] 삭제 대상 도서를 찾지 못했습니다.", file=sys.stderr)
            else:
                print("=> [문제 5] 삭제할 세 번째 도서를 찾지 못했습니다.", file=sys.stderr)
                
    except psycopg2.Error as e:
        print(f"데이터 삭제 오류: {e}", file=sys.stderr)
        conn.rollback()
    finally:
        conn.close()

# ----------------------------------------------------------------------
# 메인 실행 엔트리 포인트 (Execution Entry Point)
# ----------------------------------------------------------------------

def main():
    """모든 함수를 순서대로 호출하여 기능을 테스트합니다."""
    
    print("=============================================")
    print("   PostgreSQL Books CRUD 기능 테스트 시작")
    print("=============================================")
    
    # [1] 테이블 생성
    create_books_table()
    
    # 테이블이 이미 존재할 경우, 테스트를 위해 기존 데이터를 정리합니다.
    # 이 부분은 명시된 요구사항은 아니지만, 반복 테스트의 일관성을 위해 추가합니다.
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("TRUNCATE books RESTART IDENTITY;")
                conn.commit()
                print("=> [준비] 기존 데이터베이스 'books' 테이블의 내용을 모두 비웠습니다.")
        except psycopg2.Error as e:
            print(f"[정리 오류] {e}", file=sys.stderr)
        finally:
            conn.close()
            
    print("\n--- [초기 삽입] ---")
    # [2] 대량 데이터 삽입
    insert_books(TEST_BOOK_DATA)

    print("\n--- [초기 데이터 조회 (CRUD: R)] ---")
    # [3-1] 전체 조회 (초기 데이터 확인)
    get_all_books()
    
    # [3-2] 가격 조건 조회
    get_expensive_books()
    
    # [3-3] 제목 조건 조회 (테스트 데이터 중 하나 사용)
    get_book_by_title("알고리즘 기초")
    
    print("\n--- [데이터 갱신 및 삭제 (CRUD: U, D)] ---")
    # [4] 두 번째 도서 가격 갱신 (UPDATE)
    update_second_book_price(27000)

    # [5] 세 번째 도서 삭제 (DELETE)
    delete_third_book()

    print("\n--- [최종 결과 조회] ---")
    # [3-1] 전체 조회 (최종 결과 확인)
    get_all_books()

    print("\n=============================================")
    print("   PostgreSQL Books CRUD 기능 테스트 완료")
    print("=============================================")

if __name__ == '__main__':
    main()