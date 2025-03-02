import re
import csv

def parse_foreign_table_statements(file_path, output_csv):
    # 정규식 패턴 개선: 개행 포함 처리 + WHERE 절 포함
    pattern = (
        r"from\s+foreign\s+table\s*\(\s*"         # 'from foreign table (' 시작
        r"(select[\s\S]+?from[\s\S]+?)"           # SELECT ~ FROM 구문, 개행 포함
        r"(\s+where[\s\S]*?)?"                   # 선택적 WHERE 절, 개행 포함
        r"\)\s*@([\w]+)"                         # ') @dblinkname'
    )

    # 결과 저장 리스트
    results = []

    # 파일 읽기
    with open(file_path, 'r') as file:
        sql_content = file.read()

    # 정규식 매칭
    matches = re.finditer(pattern, sql_content, re.IGNORECASE)
    for match in matches:
        full_statement = match.group(0).strip()  # 전체 foreign table 구문
        query = match.group(1).strip()          # SELECT ~ FROM 구문
        where_clause = match.group(2).strip() if match.group(2) else "None"  # WHERE 절
        dblink = match.group(3).strip()         # DB Link 이름

        # 테이블 이름 추출 (첫 번째 FROM 뒤에 오는 단어)
        table_match = re.search(r"from\s+([\w\.\#\$\{\}]+)", query, re.IGNORECASE)
        table = table_match.group(1) if table_match else "Unknown"

        # 결과 저장
        results.append({
            "Path": file_path,
            "File Name": file_path.split("/")[-1],
            "DB Link": dblink,
            "Table": table,
            "Where Clause": where_clause,
            "Full Statement": full_statement
        })

    # CSV 저장
    with open(output_csv, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=["Path", "File Name", "DB Link", "Table", "Where Clause", "Full Statement"]
        )
        writer.writeheader()
        writer.writerows(results)

    print(f"Parsed results saved to {output_csv}")

# 실행
parse_foreign_table_statements('input.sql', 'output.csv')
