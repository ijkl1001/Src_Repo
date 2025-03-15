import re
import sys

def extract_tables_from_sql(sql_file_path):
    try:
        # SQL 파일 읽기
        with open(sql_file_path, "r", encoding="utf-8") as file:
            sql_text = file.read()

        # 정규식 패턴: FROM, JOIN, INTO, UPDATE, DELETE 뒤에 오는 테이블명 추출
        pattern = r'\b(?:FROM|JOIN|INTO|UPDATE|DELETE)\s+([\w.]+)'

        # 테이블명 추출 (대소문자 구분 없이)
        tables = set(re.findall(pattern, sql_text, re.IGNORECASE))

        # 결과 출력
        if tables:
            print("\n참조된 테이블 목록:")
            for table in sorted(tables):
                print(table)
        else:
            print("\n테이블을 찾을 수 없습니다.")

    except FileNotFoundError:
        print("❌ SQL 파일을 찾을 수 없습니다. 올바른 경로를 입력하세요.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    # 아규먼트 개수 확인 (파일 경로가 제공되었는지)
    if len(sys.argv) < 2:
        print("❌ 사용법: python script.py <SQL 파일 경로>")
        sys.exit(1)  # 프로그램 종료

    # 아규먼트에서 파일 경로 가져오기
    sql_file_path = sys.argv[1]

    # 테이블 추출 실행
    extract_tables_from_sql(sql_file_path)
