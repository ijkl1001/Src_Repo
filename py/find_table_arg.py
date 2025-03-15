import re
import argparse

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
    # 아규먼트 파서 설정
    parser = argparse.ArgumentParser(description="SQL 파일에서 참조된 테이블 목록 추출")
    parser.add_argument("sql_file", help="분석할 SQL 파일 경로")

    # 아규먼트 파싱
    args = parser.parse_args()

    # 테이블 추출 실행
    extract_tables_from_sql(args.sql_file)
