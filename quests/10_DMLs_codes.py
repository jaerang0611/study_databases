import psycopg2

# --- 데이터베이스 연결 정보 ---
# ※ 환경에 따라 db_host는 "localhost" 등으로 변경될 수 있습니다.
db_host = "db_postgresql" 
db_port = "5432"
db_name = "main_db"
db_user = "admin"
db_password = "admin123"

# --- 문제 2: 삽입할 데이터 ---
new_students = [
    ('홍길동', 23),
    ('이영희', 21),
    ('박철수', 26)
]

# --- SQL 문 정의 ---
# 1. 문제 1: 테이블 생성
sql_enable_uuid_extension = """
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
"""
sql_create_table = """
CREATE TABLE IF NOT EXISTS students ( 
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50),  
    age INT
);
"""
# 2. 문제 2: 데이터 삽입
sql_insert = """
INSERT INTO students (name, age) VALUES (%s, %s);
"""

# 3. 문제 3: SELECT 쿼리 정의
sql_select_all = "SELECT id, name, age FROM students;" 
sql_select_age_22_or_more = "SELECT id, name, age FROM students WHERE age >= 22;"
sql_select_name_hong = "SELECT id, name, age FROM students WHERE name = '홍길동';"

# 4. 문제 4: UPDATE 관련 쿼리 정의
sql_select_update_id = "SELECT id FROM students WHERE name = '이영희';"
sql_update_age = "UPDATE students SET age = %s WHERE id = %s;"

# 5. 문제 5: DELETE 관련 쿼리 정의
sql_select_delete_id = "SELECT id FROM students WHERE name = '박철수';"
sql_delete_student = "DELETE FROM students WHERE id = %s;"


conn = None 

try:
    # 1. PostgreSQL 데이터베이스에 연결합니다.
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        dbname=db_name,
        user=db_user,
        password=db_password
    )
    print("PostgreSQL 데이터베이스에 성공적으로 연결되었습니다.")

    conn.autocommit = False

    with conn.cursor() as cursor :
        # --- 문제 1 & 2: 테이블 생성 및 데이터 삽입 ---
        print("\n[문제 1 & 2] 테이블 생성 및 데이터 삽입을 시작합니다.")
        cursor.execute(sql_enable_uuid_extension)
        cursor.execute(sql_create_table)
        for name, age in new_students:
            cursor.execute(sql_insert, (name, age))
        print(f"✅ 'students' 테이블 준비 및 테스트 데이터 {len(new_students)}건 삽입 완료.")
        
        # --- 문제 4: UPDATE 연습 ---
        cursor.execute(sql_select_update_id)
        update_record = cursor.fetchone() 
        if update_record:
            update_uuid = update_record[0]
            cursor.execute(sql_update_age, (25, update_uuid))
            print(f"\n[문제 4] UPDATE 완료: '이영희' 학생의 나이를 25세로 수정했습니다.")
        
        # --- 문제 5: DELETE 연습 ---
        cursor.execute(sql_select_delete_id)
        delete_record = cursor.fetchone() 
        if delete_record:
            delete_uuid = delete_record[0]
            cursor.execute(sql_delete_student, (delete_uuid,))
            print(f"[문제 5] DELETE 완료: '박철수' 학생 데이터를 삭제했습니다.")
        
        # --- 문제 3: SELECT 쿼리 실행 (최종 확인) ---
        print("\n[문제 3] 최종 SELECT 쿼리 결과를 확인합니다.")
        
        print("\n--- 3-1. 전체 데이터 조회 ---")
        cursor.execute(sql_select_all)
        records = cursor.fetchall()
        print(f"총 {len(records)}건 조회 (박철수 삭제됨):")
        for r in records:
            print(f'ID: {str(r[0])[:8]}..., 이름: {r[1]}, 나이: {r[2]}')

    # 모든 변경 사항을 데이터베이스에 확정합니다.
    conn.commit()
    print("\n데이터베이스 변경 사항이 커밋되었습니다.")

except psycopg2.Error as e:
    # 오류 발생 시 롤백 및 오류 메시지 출력
    if conn:
        conn.rollback()
    print(f"\n❌ 데이터베이스 오류가 발생했습니다: {e}")

finally:
    if conn:
        conn.close()
        print("PostgreSQL 연결이 종료되었습니다.")
    
    # ----------------------------------------------------------------
    # --- 📌 문제 6: PRIMARY KEY 이해 문제 해설 출력 ---
    print("\n=======================================================")
    print("📌 [문제 6] PRIMARY KEY 이해 문제 해설")
    print("=======================================================")
    
    print("1. 🛑 어떤 에러가 발생하는가?")
    print("   -> 에러 유형: duplicate key value violates unique constraint와 같은 에러가 발생합니다.")
    
    print("\n2. 🤯 왜 발생하는가?")
    print("   -> 첫 번째 INSERT는 book_id에 '1'을 할당하며 성공합니다.")
    print("   -> 두 번째 INSERT는 이미 존재하는 동일한 book_id 값 '1'을 다시 삽입하려고 시도합니다.")
    print("   -> PRIMARY KEY는 값의 고유성(Uniqueness)을 강제하므로, 중복된 키 값 '1'을 허용하지 않아 에러가 발생합니다.")
    
    print("\n3. 📜 PRIMARY KEY 의 규칙")
    print("   * 고유성 (Uniqueness): PRIMARY KEY 값은 테이블 전체에서 중복될 수 없습니다.")
    print("   * NOT NULL: PRIMARY KEY 컬럼에 NULL 값을 허용하지 않습니다. 반드시 값을 가져야 합니다.")
    print("   * 단일성: 테이블당 오직 하나의 PRIMARY KEY만 정의할 수 있습니다.")
    print("=======================================================")